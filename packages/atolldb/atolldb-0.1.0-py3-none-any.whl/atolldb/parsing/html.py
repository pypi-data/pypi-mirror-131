#!/usr/bin/env python
# coding=utf-8

"""
>>> for island in parse_iceberg_files("data/inputs/iceberg/"):
...     print(island)

>>> for island in parse_paidb_files("../data/inputs/PAIDB_PAI.html", "../data/inputs/PAIDB-PAI_pages/"):
...     print(island)
"""


import json
from itertools import chain
from functools import partial
from typing import List, Optional, Sequence, Tuple
import warnings

from bs4 import BeautifulSoup, SoupStrainer

from path import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..io import PAIDBFetcher, EntrezFetcher
from ..island import Island, other_to_accession

paidb_fetcher = PAIDBFetcher("http://www.paidb.re.kr")
ncbi_fetcher = EntrezFetcher()
table_subset = SoupStrainer("table")


def extract_references(file: str) -> List[str]:
    """

    Args:
        file (str): html page where the reference lies and which will be parsed.

    Returns:
        List[str]: the references, separated by a coma.
    """
    with open(file) as f:
        page_file = f.read()
    # Puzzling, but the references are kept in a table with only one row and one col.
    page_tables = BeautifulSoup(page_file, "lxml", parse_only=table_subset).select(
        "table"
    )
    # The part that contain the references are in italic, and they seems to only exist the
    # PUBMED and the one that are in "direct submission". This is a bit "raw" but should work.
    references = [ref.text.strip().split(" ") for ref in page_tables[1].findAll("i")]
    references = [
        "PMID:{}".format(ref[ref.index("PUBMED") + 1])
        for ref in references
        if "PUBMED" in ref
    ]
    return references


def from_paidb_cells(cells: Sequence, reference_pages_folder: str) -> Island:
    """Extract the From a html table row that come from a paidb web page and put it into an Island container

    Args:
        cells (Sequence): sequence that contain bs4 parsed cells.
        pages_folder (str): path where lie the reference pages.

    Returns:
        Island
    """
    cells = [cell.text.strip() for cell in cells]

    organism = cells[2]
    insertion = cells[4]
    accession = other_to_accession(cells[5])

    other = {"function": cells[3]}

    if insertion == "-":
        insertion = ""

    if accession.split("_")[-1][0] in ["P", "R"]:
        version = accession.split("_")[-1]
        accession = "_".join(accession.split("_")[:-1])
        page = "page_*_%s.html" % "_".join([accession, version])
    else:
        version = ""
        page = "page_*_%s.html" % accession

    island = Island(
        accession=accession,
        version=version,
        organism=organism,
        insertion=insertion,
        other=other,
        detection="paidb",
    )
    island.reference = ", ".join(
        extract_references(Path(reference_pages_folder).files(page)[0])
    )
    return island


def row_to_islands(row, reference_pages_folder):
    cells = row.findAll("td")
    if cells:
        island = from_paidb_cells(cells, reference_pages_folder)
        return island


def parse_paidb_files(main_page: str, sub_pages: str):
    """ Create a generator that will parse some PAIDB pages and will yield
    the correspondant Islands.

    Args:
        main_page (str): The main page to parse.
        sub_pages (str): The sub-pages that contain the references.

    Yield: Island
    """
    with open(main_page, "r") as f:
        # The islands are displaid in table that have a white border color.
        tables = BeautifulSoup(f, "lxml", parse_only=table_subset).find_all(
            bordercolordark="white"
        )
    # Each row of this table contain an island of the same organism familly
    with ThreadPoolExecutor() as e:
        islands = list(
            e.map(
                partial(row_to_islands, reference_pages_folder=sub_pages),
                chain(*[species.findAll(valign="top") for species in tables]),
            )
        )
        # Each row of this table contain an island of the same organism familly
    islands_pai = [island for island in islands if island.version]
    islands_ncbi = [island for island in islands if not island.version]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with ThreadPoolExecutor(max_workers=2) as e:
            islands_pai_seqs = list(
                e.map(
                    paidb_fetcher.get_genbank,
                    [
                        "%s_%s" % (island.accession, island.version)
                        for island in islands_pai
                    ],
                )
            )
        _, islands_ncbi_seqs = zip(
            *ncbi_fetcher.accession_to_fasta(
                [island.accession for island in islands_ncbi]
            )
        )
    for island, seq in chain(
        zip(islands_pai, islands_pai_seqs), zip(islands_ncbi, islands_ncbi_seqs)
    ):
        island.sequence = seq
        island.seq_len = len(island.sequence.seq)
        yield island


# if accession.split("_")[-1][0] in ["P", "R"]:
#     seq = paidb_fetcher.get_genbank(accession)
# else:
#     seq = ncbi_fetcher.accession_to_fasta([accession])[0][1]


def get_coordinate(info: dict) -> Tuple[int, int]:
    """ Extract the island coordinates (start / end) from the raw ICEberg data.

    Args:
        info (dict): the data extracted from the ICEberg page

    Returns:
        Tuple[Optional[int], Optional[int]]: if the coordinate is found, return start / end as integer.
    """
    try:
        # The key is not stable in the different pages : can be "coordinate", "Gene coordinate"...
        coord = [coord for key, coord in info.items() if "coordinate" in key.lower()][0]
        start, end = map(int, coord.split(".."))
        return start, end
    except IndexError:
        return 0, 0


def iceberg_page_to_island(file: str) -> Optional[Island]:
    """Extract the data from one ICEberg web page, and return the corresponding Island

    Args:
        file (str): the ICEberg web page to parse.

    Returns:
        Island
    """
    with open(file, "r") as f:
        html_tables = BeautifulSoup(f, "lxml").select("table")
    if len(html_tables) <= 5:
        return None

    table = html_tables[0].select("td")
    references = html_tables[4].select("a")
    references = ",".join(
        [ref.text.strip().replace("PudMed", "PMID") for ref in references]
    )

    info_list = [col.text.strip() for col in table]
    info = dict(zip(info_list[::2], info_list[1::2]))

    start, end = get_coordinate(info)
    organism = info["Organism"]
    accession = other_to_accession(info["Nucleotide Sequence"])
    insertion = info["Insertion site"]
    if insertion == "-":
        insertion = ""
    other = dict(name=info["Name"], family=info["Family"], function=info["Function"])
    other_json = json.dumps(
        {key: value for key, value in other.items() if value != "-"}
    )

    island = Island(
        detection="ICEberg",
        start=start,
        end=end,
        organism=organism,
        accession=accession,
        insertion=insertion,
        reference=references,
        other=other_json,
    )
    return island


def parse_iceberg_files(path):
    """ Create a generator that will parse some ICEberg pages and will yield
    the correspondant Islands.

    Args:
        path (str): The place where lie the ICEberg pages.

    Yield: Island
    """
    path = Path(path)
    for file in path.files("*.html"):
        island = iceberg_page_to_island(file)
        if island:
            yield island
