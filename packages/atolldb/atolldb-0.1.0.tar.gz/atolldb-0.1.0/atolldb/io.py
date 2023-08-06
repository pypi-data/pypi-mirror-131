#!/usr/bin/env python
# coding=utf-8


import io
import warnings
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from threading import BoundedSemaphore, Timer
from loguru import logger
from retrying import retry
from functools import partial

import attr

from pandas import DataFrame
from Bio import Entrez, SeqIO
from more_itertools import chunked
from path import Path
from uplink import Consumer, get
from lxml import etree

import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

EMAIL = "contact@nicolas-cellier.net"
NCBI_TOKEN = "8e5d87a2fa835a059834ac1e6d52b1e92008"

logger.disable(__name__)


def retry_if_request_error(exception):
    """Return True if we should retry (in this case when it's an Entrez.HTTPError), False otherwise"""
    return isinstance(exception, Entrez.HTTPError)


def write_fasta(row, fasta_path):
    fasta_path = Path(fasta_path)
    fasta_path.makedirs_p()
    record = row.sequence
    SeqIO.write(
        record,
        fasta_path / "%s-%i-%i.fasta" % (row.accession.strip(), row.start, row.end),
        format="fasta",
    )


def write_genbank(row, fasta_path):
    fasta_path = Path(fasta_path)
    fasta_path.makedirs_p()
    record = row.sequence
    SeqIO.write(
        record,
        fasta_path / "%s-%i-%i.gb" % (row.accession.strip(), row.start, row.end),
        format="genbank",
    )


def parse_paidb_genbank(html):
    parser = etree.HTMLParser()
    tree = etree.parse(io.StringIO(html), parser)
    gb_txt = tree.xpath("/html/body/pre/font")[0].text
    gb_seq = next(SeqIO.parse(io.StringIO(gb_txt), "genbank"))
    return gb_seq


class PAIDBFetcher(Consumer):
    """A Python Client for the paidb genbank flat_file."""

    @get("view_pai_from_genome.php?pa={accession}")
    def _get_genbank(self, accession):
        pass

    @retry()
    def get_genbank(self, accession):
        response = self._get_genbank(accession)
        return parse_paidb_genbank(response.text)


@attr.s
class EntrezFetcher:
    email = attr.ib(type=str, default=EMAIL)
    api_key = attr.ib(type=str, default=NCBI_TOKEN)
    batch_size = attr.ib(type=int, default=200)
    request_limit = attr.ib(type=int, default=None)

    # request limit is set for request / PERIOD sec
    PERIOD = 1

    def __attrs_post_init__(self):
        self.request_limit = self.request_limit or (
            8 if self.api_key is not None else 2
        )
        self.request_limiter = BoundedSemaphore(self.request_limit)
        self.reset_limit()
        Entrez.email = self.email
        Entrez.api_key = self.api_key

    def reset_limit(self):
        for _ in range(self.request_limit):
            try:
                self.request_limiter.release()
            except ValueError:
                break
        self.timer = Timer(self.PERIOD, self.reset_limit)
        self.timer.daemon = True
        self.timer.start()

    @staticmethod
    def split_seq(raw_fasta, rettype):
        yield from SeqIO.parse(io.StringIO(raw_fasta), rettype)

    def _process_by_batch(self, accession_numbers, routine):
        accession_numbers = set(accession_numbers)
        batch_size = max(
            min(self.batch_size, len(accession_numbers) // self.request_limit), 1
        )
        chunks = chunked(accession_numbers, batch_size)
        if self.request_limit == 1:
            return list(chain(*map(routine, chunks)))
        with ThreadPoolExecutor(max_workers=self.request_limit) as e:
            return list(chain(*e.map(routine, chunks)))

    @logger.catch
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=300000,
        stop_max_attempt_number=20,
        retry_on_exception=retry_if_request_error,
    )
    def _accession_to_seq(self, accession_numbers, rettype="fasta"):
        if isinstance(accession_numbers, str):
            accession_numbers = [accession_numbers]
        logger.debug("get fasta for %i accession numbers" % len(accession_numbers))
        self.request_limiter.acquire()
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", module="Bio.Entrez")
                seqs = Entrez.efetch(
                    "nuccore",
                    id=",".join(accession_numbers),
                    rettype=rettype,
                )
                seqs.flush()
            res = list(zip(accession_numbers, self.split_seq(seqs.read(), rettype)))
            logger.debug("%i seq retrieved." % len(accession_numbers))
            return res
        finally:
            try:
                self.request_limiter.release()
            except ValueError:
                pass

    @logger.catch
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=300000,
        stop_max_attempt_number=20,
        retry_on_exception=retry_if_request_error,
    )
    def _accession_to_summary(self, accession_numbers):
        if isinstance(accession_numbers, str):
            accession_numbers = [accession_numbers]
        while True:
            logger.debug("get docsum for %i accession numbers" % len(accession_numbers))
            self.request_limiter.acquire()
            try:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", module="Bio.Entrez")
                    summaries = Entrez.parse(
                        Entrez.esummary(db="nuccore", id=",".join(accession_numbers)),
                        validate=True,
                    )
                    return list(zip(accession_numbers, summaries))
            except Entrez.HTTPError:
                logger.exception("Entrez HTTP exception")
                raise
            except RuntimeError as e:
                splitted_msg = str(e).split()
                try:
                    uid = splitted_msg[splitted_msg.index("uid") + 1]
                    logger.debug(
                        "Invalid accession number: %s, removed from the list." % uid
                    )
                    accession_numbers.remove(uid)
                    if not accession_numbers:
                        return []
                except ValueError:
                    raise e
            finally:
                try:
                    self.request_limiter.release()
                except ValueError:
                    pass

    @logger.catch
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=300000,
        stop_max_attempt_number=20,
        retry_on_exception=retry_if_request_error,
    )
    def _taxid_to_taxonomy(self, taxids):
        if isinstance(taxids, str):
            taxids = [taxids]
        while True:
            logger.debug("get docsum for %i accession numbers" % len(taxids))
            self.request_limiter.acquire()
            try:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", module="Bio.Entrez")
                    summaries = Entrez.parse(
                        Entrez.efetch(id=",".join(taxids), db="taxonomy", retmode="xml")
                    )
                    return list(zip(taxids, summaries))
            except Entrez.HTTPError:
                logger.exception("Entrez HTTP exception")
                raise
            except RuntimeError as e:
                splitted_msg = str(e).split()
                try:
                    uid = splitted_msg[splitted_msg.index("uid") + 1]
                    logger.debug("Invalid taxid: %s, removed from the list." % uid)
                    taxids.remove(uid)
                    if not taxids:
                        return []
                except ValueError:
                    raise e
            finally:
                try:
                    self.request_limiter.release()
                except ValueError:
                    pass

    def accession_to_fasta(self, accession_numbers):
        return self._process_by_batch(
            accession_numbers, routine=partial(self._accession_to_seq, rettype="fasta")
        )

    def accession_to_genbank(self, accession_numbers):
        return self._process_by_batch(
            accession_numbers, routine=partial(self._accession_to_seq, rettype="gb")
        )

    def accession_to_summary(self, accession_numbers):
        accession_numbers, summaries = zip(
            *self._process_by_batch(
                accession_numbers, routine=self._accession_to_summary
            )
        )
        summaries_df = DataFrame(summaries, index=accession_numbers)
        return summaries_df

    def taxid_to_taxonomy(self, taxids):
        taxids, taxons = zip(
            *self._process_by_batch(taxids, routine=self._taxid_to_taxonomy)
        )

        def format_taxons(taxon):
            taxid = taxon["TaxId"]
            lineage = taxon["Lineage"]
            name = taxon["ScientificName"]
            lineage_id = ";".join([linex["TaxId"] for linex in taxon["LineageEx"]])
            ranks = ";".join([linex["Rank"] for linex in taxon["LineageEx"]])
            return dict(
                taxid=int(taxid),
                scientific_name=name,
                lineage=lineage,
                lineage_id=lineage_id,
                ranks=ranks,
            )

        taxonomy = DataFrame([format_taxons(taxon) for taxon in taxons])
        return taxonomy.set_index("taxid")

    def accession_to_taxonomy(self, accession_numbers):
        summaries = self.accession_to_summary(accession_numbers)
        taxids = summaries["TaxId"].astype(str)
        taxonomy = self.taxid_to_taxonomy(taxids)
        taxonomy = summaries[["Caption", "TaxId"]].merge(
            taxonomy, how="left", left_on="TaxId", right_on="taxid"
        )
        return taxonomy.rename(columns={"Caption": "accession", "TaxId": "taxid"})
