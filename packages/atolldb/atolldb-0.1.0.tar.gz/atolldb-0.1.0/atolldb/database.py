#!/usr/bin/env python
# coding=utf-8


import operator
import warnings
from functools import partial
from typing import Callable, Dict, Iterable, Optional, Sequence, Tuple, Union
import datetime
from contextlib import contextmanager

import numpy as np
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from cachetools import cachedmethod
from pandas import DataFrame
from path import Path
from tables import PerformanceWarning
from tqdm import tqdm

from .io import EntrezFetcher, write_fasta
from .island import Island
from .utils import genome_to_island_sequence, relpath_or_none, filter_not_seq_len

RecordOrPath = Union[SeqRecord, Path]

warnings.filterwarnings("ignore", category=PerformanceWarning)
pd.options.mode.chained_assignment = None


class AtollDatabase:
    ISLANDS_FILENAME = "islands.hdf"
    FASTA_DIRNAME = "fasta_files"
    __RESERVED_KEYS__ = ["update", "post_process", "dropped"]

    def __init__(
        self,
        path: str,
        fasta_files_path: Optional[str] = None,
        fetcher: Optional[EntrezFetcher] = None,
        progress=tqdm,
        fresh=False,
    ):
        """AtollDatabase, on-disk database that store islands data that come from different
        sources on disk and allow to easily manipulate, modify and update them.

        It gives access to the islands as a pandas.DataFrame as well as a list of atoll.Island.

        Args:
            path (str): path to the atoll folder.
            fasta_files_path (Optional[str]): path to the fasta files. If None, it will be `path / fasta_files`
        (and destroyed as the same time as the database).
            fasta_files_path (Optional[FastaFetcher]): an instance of FastaFetcher. If None, one will be created.
        It is strongly recommended to furnish one with your `email` and `api_key`. That way, you will be allowed
        to run up to 10 concurrent request and speed up the fasta fetching.
            fresh (bool, optional): Defaults to False. if True, recreate the database from scratch.
        """
        self._path = path
        self._fasta_dir = fasta_files_path or self.path / self.FASTA_DIRNAME
        self.fetcher = fetcher or EntrezFetcher()
        self.progress = progress

        if fresh:
            Path(self.path).rmtree_p()

        self._init_db()
        self._islands_cache = None
        self._merged_cache = None
        self._raw_islands_cache: Dict[Tuple[str], str] = {}
        self._island_seq_path_cache: Dict[Tuple[str, int, int], str] = {}
        self._genome_path_cache: Dict[Tuple[str], str] = {}
        self._genbank_path_cache: Dict[Tuple[str], str] = {}

    def _init_db(self):
        """Create the folders that compose the database."""
        Path(self.path).mkdir_p()
        self.fasta_dir.mkdir_p()
        self.parsed_sequences_dir.mkdir_p()
        self.ncbi_genome_dir.mkdir_p()
        self.ncbi_island_seq_dir.mkdir_p()

    def clean_cache(self):
        """Clean the cache and ensure that the islands mirror the on-disk data."""

        self._islands_cache = None
        with self.store as store:
            try:
                store.remove("merged_islands")
            except KeyError:
                pass

    @property
    def islands(self) -> DataFrame:
        """Return the islands that live on-disk as a DataFrame.

        Returns:
            DataFrame
        """
        if self._islands_cache is None:
            self._islands_cache = self._get_islands()

        return self._islands_cache

    @property
    def islands_with_taxons(self) -> DataFrame:
        """Return the islands that live on-disk as a DataFrame.

        Returns:
            DataFrame
        """
        taxonomy = self.taxonomy
        islands = self.islands
        islands = islands.set_axis(
            pd.MultiIndex.from_product([islands.columns, [""]]), axis=1, inplace=False
        )
        return islands.merge(taxonomy, left_on="taxid", right_index=True, how="left")

    @property
    def islands_with_fpath(self) -> DataFrame:
        """Return the islands that live on-disk as a DataFrame, with the
        relative path to the relevant fasta files.

        Returns:
            DataFrame
        """
        return self.get_fasta_paths(self.islands)

    @property
    def shape(self) -> Tuple[int, int]:
        """Return the shape of the underlying dataframe

        Returns:
            tuple(int, int)
        """
        return self.islands.shape

    @property
    def __len__(self) -> int:
        return self.islands.__len__

    @property
    @contextmanager
    def store(self) -> pd.HDFStore:
        """Return the HDFStore containing the persistant data

        Returns:
            HDFStore
        """
        store = pd.HDFStore(self.islands_file)
        try:
            yield store
        finally:
            store.close()

    @property
    def post_processes(self) -> Sequence[str]:
        with self.store as store:
            keys = store.keys()
        return [
            key.strip("/").split("/")[1]
            for key in keys
            if key.strip("/").split("/")[0] == "post_processes"
        ]

    @property
    def sources(self) -> Sequence[str]:
        with self.store as store:
            keys = store.keys()
        return [
            key.strip("/").split("/")[1]
            for key in keys
            if key.strip("/").split("/")[0] == "sources"
        ]

    # Retrieve the data and add some info to it (as fasta file path).

    def _get_islands(self):
        """Read the islands stored in the different sources and
        apply the update to it."""
        # (if the data become really large, this could be prohibitif to reload the dataframe each time).
        if not self.sources:
            return DataFrame()

        # retrieve every "original" data from the different sources
        df = self.raw_islands.drop(self.dropped.index)
        # if the user has updated some island, load this update and overwrite these rows
        update_df = self.updated_islands
        post_processes_df = self.post_processed_cols
        df = df.merge(
            post_processes_df,
            how="left",
            left_index=True,
            right_index=True,
            validate="one_to_one",
        )
        df.update(update_df)
        df.last_updated = pd.to_datetime(df.last_updated).astype("datetime64[s]")
        # docsum = self._retrieve_docsum(df)
        # df = df.merge(docsum, "left", left_on="accession", right_index=True)
        self._islands = df
        return self._islands

    @property
    def docsum(self):
        return self._retrieve_docsum()

    @property
    def taxids(self):
        return self._retrieve_docsum()["taxid"]

    @property
    def taxonomy(self):
        return self._retrieve_taxonomy()

    def _from_multi_index(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        df.index = ["%s-%i" % (source, index) for source, index in df.index]
        return df

    def _to_multi_index(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        indexes = [index.split("-") for index in df.index]

        df.index = pd.MultiIndex.from_tuples(
            [(source, int(index)) for source, index in indexes],
            names=("source", "index"),
        )
        return df

    def _insert_path_to_df(self, df):
        seq_paths = list(self.extract_sequences_path(df))
        extracted_paths = list(self.get_extracted_fasta(df))
        paths = [
            {
                "ncbi_genome_path": relpath_or_none(self.fasta_dir, genome_path),
                "ncbi_island_seq_path": relpath_or_none(
                    self.fasta_dir, island_seq_path
                ),
                "extracted_island_seq_path": relpath_or_none(
                    self.fasta_dir, extracted_path
                ),
            }
            for (genome_path, island_seq_path), extracted_path in zip(
                seq_paths, extracted_paths
            )
        ]

        paths_df = pd.DataFrame(paths, dtype="str")
        paths_df.index = df.index
        return pd.concat([df, paths_df], axis=1)

    def get_fasta_paths(self, islands: DataFrame) -> DataFrame:
        df = self._insert_path_to_df(islands)
        return df

    # Routine to access to fasta files, full genome as well as island sequences.

    @cachedmethod(operator.attrgetter("_genome_path_cache"))
    def get_genome_path(self, accession: str) -> str:
        path = self.ncbi_genome_dir / ("%s.fasta" % accession)
        if path.exists():
            return path
        return ""

    @cachedmethod(operator.attrgetter("_island_seq_path_cache"))
    def get_island_seq_path(self, accession: str, start: int, end: int) -> str:
        path = self.ncbi_island_seq_dir / (
            "%s-%i-%i-extracted.fasta" % (accession, start, end)
        )
        if path.exists():
            return path
        return ""

    @cachedmethod(operator.attrgetter("_genbank_path_cache"))
    def get_genbank_path(self, accession: str) -> str:
        path = self.ncbi_genome_dir / ("%s.gb" % accession)
        if path.exists():
            return path
        return ""

    def extract_sequences_path(self, islands: DataFrame = None):
        if islands is None:
            islands = self.islands
        for accession, start, end in islands[["accession", "start", "end"]].values:
            genome_file = self.get_genome_path(accession)
            island_seq_file = self.get_island_seq_path(accession, start, end)
            yield genome_file, island_seq_file

    def get_extracted_fasta(self, islands=None):
        if islands is None:
            islands = self.islands
        _islands = islands.reset_index()
        extracted_fasta = (
            self.fasta_dir.rstrip("/")
            + "/"
            + "atoll_parsing/"
            + _islands.source
            + "/"
            + _islands.accession
            + "-"
            + _islands.start.astype(str)
            + "-"
            + _islands.end.astype(str)
            + ".fasta"
        )
        extracted_fasta.index = islands.index
        extracted_fasta.loc[
            ~extracted_fasta.apply(lambda path: Path(path).exists())
        ] = ""
        # extracted_fasta = extracted_fasta.apply(lambda path: relpath_or_none(self.fasta_dir, path))
        return extracted_fasta

    def merge_extracted_ncbi_fasta_paths(self, islands=None):
        """Merge two different souurce of fasta : if there is a sequence that
        have been provided by the parser, get this one, and fallback on NCBI data
        if any.
        """
        if islands is None:
            islands = self.islands
        # cannot use path.py to join the paths : numpy vectorized concatenation is way faster
        # (and we have to work with > 1E5 rows).
        extracted_fasta = self.get_extracted_fasta(islands)
        not_extracted = extracted_fasta.loc[~extracted_fasta.apply(bool)].index
        not_extracted_fasta_paths = list(
            self.get_island_sequences(islands.loc[not_extracted], path_only=True)
        )
        extracted_fasta.loc[not_extracted] = not_extracted_fasta_paths
        extracted_fasta.name = "path"
        return extracted_fasta

    def _write_genome_record(self, accession, record):
        SeqIO.write(record, self.ncbi_genome_dir / ("%s.fasta" % accession), "fasta")
        try:
            # TODO: we can use a specialized cache structure that expose a cleaning logic.
            del self._genome_path_cache[(accession,)]
        except KeyError:
            pass

    def _write_island_seq_record(self, accession, start, end, record):
        SeqIO.write(
            record,
            self.ncbi_island_seq_dir
            / ("%s-%i-%i-extracted.fasta" % (accession, start, end)),
            format="fasta",
        )
        try:
            # TODO: we can use a specialized cache structure that expose a cleaning logic.
            del self._island_seq_path_cache[(accession, start, end)]
        except KeyError:
            pass

    def _write_genbank_record(self, accession, record):
        record.annotations['molecule_type'] = 'dna'
        SeqIO.write(record, self.ncbi_genome_dir / ("%s.gb" % accession), "genbank")
        try:
            # TODO: we can use a specialized cache structure that expose a cleaning logic.
            del self._genbank_path_cache[(accession,)]
        except KeyError:
            pass

    def _split_island_seq_from_genome(self, accession, start, end):
        genome = SeqIO.read(self.get_genome_path(accession), format="fasta")
        island_sequence = genome_to_island_sequence(genome, start, end)
        return island_sequence

    def import_fasta_from_ncbi(self, islands: DataFrame = None):
        """import_fasta_from_ncbi

        Args:
            islands (DataFrame, optional): Defaults to None. if any, use these islands to fetch the fasta files. Otherwise, use all the database islands.
        """
        if islands is None:
            islands = self.islands

        # filter the accession number that have not been fetched already.
        accessions = [
            accession
            for accession in islands.accession
            if accession and not self.get_genome_path(accession)
        ]

        for accession, record in self.fetcher.accession_to_fasta(accessions):
            self._write_genome_record(accession, record)

        # extract the island sequence from its bound and the full genome.
        for accession, start, end in islands[["accession", "start", "end"]].values:
            if not accession:
                continue
            island_seq_file = self.get_island_seq_path(accession, start, end)
            # filter to only have sequences that havent been extracted.
            if island_seq_file:
                continue
            try:
                island_sequence = self._split_island_seq_from_genome(accession, start, end)
                if island_sequence:
                    self._write_island_seq_record(accession, start, end, island_sequence)
            except FileNotFoundError:
                pass

    def import_genbanks_from_ncbi(self, islands: DataFrame = None):
        """import_fasta_from_ncbi

        Args:
            islands (DataFrame, optional): Defaults to None. if any, use these islands to fetch the fasta files. Otherwise, use all the database islands.
        """
        if islands is None:
            islands = self.islands

        # filter the accession number that have not been fetched already.
        accessions = [
            accession
            for accession in islands.accession
            if accession and not self.get_genbank_path(accession)
        ]

        for accession, record in self.fetcher.accession_to_genbank(accessions):
            self._write_genbank_record(accession, record)


    def get_island_sequences(
        self, islands: DataFrame = None, path_only=False
    ) -> RecordOrPath:
        """Generate the island sequences. If they have not been retrieved from ncbi yet, do it. You can access to the path of the
        fasta files instead of the sequence records.

        Warning: this is a generator (as the sequences can be heavy).
        Use `records = list(get_island_sequences())` to retrieve it as a list.

        Args:
            islands (DataFrame, optional): Defaults to None. if any, use these islands to fetch the fasta files. Otherwise, use all the database islands.
            path_only (bool, optional): Defaults to False. if True, return the path to the fasta files instead of the SeqRecord.

        Yield:
            RecordOrPath

        TODO:
            Sometime, we have the sequences from the source as well as the sequences from the NCBI. It should yield
                Tuple[Seq_1, Seq_2] with Seq_i being the ith sequence available (with some order of priority).
        """

        if islands is None:
            islands = self.islands
        self.import_fasta_from_ncbi(islands)
        for (_, row) in islands.iterrows():
            accession, start, end = row.accession, row.start, row.end
            island_seq_file = self.get_island_seq_path(accession, start, end)
            if not island_seq_file:
                continue
            if path_only:
                yield island_seq_file
            else:
                yield SeqIO.read(island_seq_file, format="fasta")

    def get_genomes(
        self, islands: Optional[DataFrame] = None, path_only=False
    ) -> RecordOrPath:
        """Generate the full genome sequences. If they have not been retrieved from ncbi yet, do it. You can access to the path of the
        fasta files instead of the sequence records.

        Warning: this is a generator (as the sequences can be heavy).
        Use `records = list(get_island_sequences())` to retrieve it as a list.

        Args:
            islands (DataFrame, optional): Defaults to None. if any, use these islands to fetch the fasta files. Otherwise, use all the database islands.
            path_only (bool, optional): Defaults to False. if True, return the path to the fasta files instead of the SeqRecord.

        Yield:
            RecordOrPath
        """
        if islands is None:
            islands = self.islands
        self.import_fasta_from_ncbi(islands)
        for (_, row) in islands.iterrows():
            accession = row.accession
            genome_file = self.get_genome_path(accession)
            if path_only:
                yield genome_file
            else:
                yield SeqIO.read(genome_file, format="fasta")

    def get_genbanks(
        self, islands: Optional[DataFrame] = None, path_only=False
    ) -> RecordOrPath:
        """Generate the full genome sequences. If they have not been retrieved from ncbi yet, do it. You can access to the path of the
        fasta files instead of the sequence records.

        Warning: this is a generator (as the sequences can be heavy).
        Use `records = list(get_island_sequences())` to retrieve it as a list.

        Args:
            islands (DataFrame, optional): Defaults to None. if any, use these islands to fetch the fasta files. Otherwise, use all the database islands.
            path_only (bool, optional): Defaults to False. if True, return the path to the fasta files instead of the SeqRecord.

        Yield:
            RecordOrPath
        """
        if islands is None:
            islands = self.islands
        self.import_genbanks_from_ncbi(islands)
        for (_, row) in islands.iterrows():
            accession = row.accession
            genome_file = self.get_genbank_path(accession)
            if path_only:
                yield genome_file
            else:
                yield SeqIO.read(genome_file, format="genbank")

    # Representation routines (the DB should behave as the underlying dataframe.)

    def __repr__(self):
        return self.islands.__repr__()

    def _repr_html_(self):
        return self.islands._repr_html_()

    def _repr_latex_(self):
        return self.islands._repr_latex_()

    # All the paths of the on-disk data

    @property
    def islands_file(self) -> Path:
        return Path(self.path) / self.ISLANDS_FILENAME

    @property
    def ncbi_genome_dir(self) -> Path:
        return self.fasta_dir / "ncbi_genome"

    @property
    def ncbi_island_seq_dir(self) -> Path:
        return self.fasta_dir / "ncbi_island_sequence"

    @property
    def parsed_sequences_dir(self) -> Path:
        return self.fasta_dir / "atoll_parsing"

    @property
    def path(self) -> Path:
        return Path(self._path)

    @property
    def fasta_dir(self) -> Path:
        return Path(self._fasta_dir)

    # Routine that allow to access to the underlying data in a partial way

    def by_source(self, source: str) -> DataFrame:
        """Returns:
        DataFrame: A dataframe that contain the original data (that come directly from the sources).
        """
        return self.islands[self.islands.index.get_level_values("source") == source]

    @cachedmethod(operator.attrgetter("_raw_islands_cache"))
    def _retrieve_raw_source(self, name):
        if name not in self.sources:
            return self._to_multi_index(DataFrame(columns=Island.columns()))
        with self.store as store:
            raw_sources = self._to_multi_index(store["/sources/%s" % name])
        return raw_sources

    @property
    def raw_islands(self) -> DataFrame:
        """Returns:
        DataFrame: A dataframe that contain the original data (that come directly from the sources).
        """
        if not self.sources:
            return self._to_multi_index(DataFrame(columns=Island.columns()))
        return pd.concat([self._retrieve_raw_source(name) for name in self.sources])

    # Routine that allow to add / update / remove data on-disk

    def add_source(
        self,
        parser: Iterable[Island],
        name: str,
        force=False,
        **kwargs: Dict[str, Union[str, Callable]]
    ):
        """Add a source to the database. The source can be any iterable that yield an Island.
        The name is mandatory and can be any string but `update` which is a reserved name.

        If an other source exists with the same name, that function will do nothing and return None
        unless `force` is True. In that case, the previous source will be overwritten.

        Args:
            parser (Iterable[Island]):
            name (str): the name of the source.
            force (bool, optional): Defaults to False. if True, overwrite a source with the same name.
            **kwargs (Union[str, Callable]): Every extra named parameters can be use to overwrite a column of
              the source. It can be either a simple value (and all the row will have that value), or a
              callable that will take a row of the islands DataFrame and return the value of this column for each row.

        Raises:
            KeyError: raised if a reserved name is provided.

        Examples:
            Add all the row of the Islander Database

            >>> from atoll import AtollDB
            >>> from atoll.parsing.sql import parse_islander_db
            >>> atollDB = AtollDB("./atoll_db/")
            >>> atollDB.add_source(parse_islander_db("./islander.db"), name="islander")

            Same, but overwrite the type_ column with a single value

            >>> atollDB.add_source(parse_islander_db("./islander.db"), name="islander_overwritted", type_="test_value")
            >>> atollDB.by_source("islander_overwritten").iloc[0].type_
            'test_value'
        """
        if name in self.sources and not force:
            warnings.warn(
                "Source %s already added. Use force=True to overwrite." % name,
                category=UserWarning,
            )
            return None

        islands = Island.to_df(self.progress(parser))

        # drop the "true" duplicates that comme from a possible double parsing
        # of the same line
        islands = islands.drop_duplicates(
            subset=[col for col in islands.columns if col != "sequence"]
        )

        # get the islands with sequences, write it in a dedicated place
        with_sequences = islands[
            (islands.accession != "")
            & (islands.sequence.apply(lambda island: not isinstance(island, str)))
        ]
        parsed_seqs_dir = self.parsed_sequences_dir / name
        parsed_seqs_dir.mkdir_p()
        with_sequences.apply(
            partial(write_fasta, fasta_path=parsed_seqs_dir), axis=1
        )
        islands = islands.drop("sequence", axis=1)

        islands.index = ["%s-%i" % (name, i) for i in range(len(islands))]
        for key in set(Island.columns()).intersection(kwargs.keys()):
            value = kwargs[key]
            if callable(value):
                value = islands.apply(value, axis=1)
            islands[key] = value
        with self.store as store:
            if "/sources/%s" % name in store.keys() and force:
                store.remove(name)
            store.put("/sources/%s" % name, islands)
        self.clean_cache()
        to_drop = self._to_multi_index(
            islands.loc[islands.apply(filter_not_seq_len, axis=1)]
        )
        self.drop_islands(to_drop, why="automatic drop line at source addition.")
        self.clean_cache()

    def merge_islands(self, islands=None):
        if islands is None:
            islands = self.islands

        islands = islands.reset_index().drop("last_updated", axis=1)

        grp = islands.sort_values(["accession", "start", "end"]).groupby(
            ["accession", "start", "end"]
        )

        def join_if_not_unique(values):
            unik_values = set([value for value in values if value])
            return ";".join(map(str, unik_values))

        def join_keeping_all(values):
            return ";".join(map(str, values))

        aggregate_cols = {
            col: join_keeping_all
            if col in ["index", "source", "detection"]
            else join_if_not_unique
            for col in islands.columns
        }
        merged_islands = grp.agg(aggregate_cols).drop(
            ["accession", "start", "end"], axis=1
        )
        merged_islands["duplicates"] = grp.organism.size()
        return merged_islands

    @property
    def merged_islands(self):
        try:
            with self.store as store:
                merged = store["merged_islands"]
        except KeyError:
            merged = self.merge_islands()
            with self.store as store:
                store.put("merged_islands", merged)
        return merged

    def remove_source(self, name: str):
        """Remove a source

        Args:
            name (str): the name of the source
        """
        with self.store as store:
            keys = store.keys()
        if "/sources/%s" % name in keys:
            with self.store as store:
                store.remove(name)
            self.clean_cache()
            return
        warnings.warn("Source does not exist, did nothing.")

    def _retrieve_docsum(self, islands=None, use_cache=True):
        if use_cache:
            try:
                with self.store as store:
                    cached_taxids = store["summaries"]
            except KeyError:
                cached_taxids = pd.DataFrame()
        else:
            cached_taxids = pd.DataFrame()
        if islands is None:
            islands = self.islands
        to_retrieve = islands.loc[~islands.accession.isin(cached_taxids.index)]
        if not len(to_retrieve):
            return cached_taxids
        summaries = self.fetcher.accession_to_summary(to_retrieve.accession)
        summaries = summaries[["TaxId", "Length"]].rename(
            columns={"TaxId": "taxid", "Length": "ncbi_ref_len"}
        )
        unretrieved_acc = to_retrieve.loc[
            ~to_retrieve.accession.isin(summaries.index)
        ].accession
        summaries = summaries.reindex(to_retrieve.accession.unique())
        summaries.loc[unretrieved_acc, "taxid"] = 0
        summaries.loc[unretrieved_acc, "ncbi_ref_len"] = 0
        merged_summaries = pd.concat([cached_taxids, summaries]).sort_index()
        with self.store as store:
            store.put("summaries", merged_summaries)
        return merged_summaries

    def _retrieve_taxonomy(self, taxids=None, use_cache=True):
        if taxids is None:
            taxids = self._retrieve_docsum().taxid
        taxids = taxids[taxids != 0]
        if use_cache:
            try:
                cached_taxonomy = pd.read_csv(
                    self.path / "taxonomy.csv", index_col=0, header=[0, 1]
                )
                cached_taxonomy = cached_taxonomy[
                    ~cached_taxonomy.index.duplicated()
                ].rename(columns=lambda col: col if "Unnamed" not in col else "")
            except FileNotFoundError:
                cached_taxonomy = pd.DataFrame()

        else:
            cached_taxonomy = pd.DataFrame()

        to_retrieve = taxids.loc[~taxids.isin(cached_taxonomy.index)]

        if not len(to_retrieve):
            return cached_taxonomy

        taxonomy = self.fetcher.taxid_to_taxonomy(map(str, to_retrieve))
        if not set(taxonomy.index).difference(cached_taxonomy.index):
            return cached_taxonomy

        ranks_order = [
            "base",
            "superkingdom",
            "phylum",
            "subphylum",
            "class",
            "subclass",
            "order",
            "suborder",
            "family",
            "subfamily",
            "tribe",
            "genus",
            "species group",
            "species subgroup",
            "species",
            "subspecies",
        ]
        columns = pd.MultiIndex.from_product([ranks_order[::-1], ("id", "name")])

        def merge_lineage(row):
            ids = str(row.lineage_id).split(";")
            lineage = str(row.lineage).split(";")
            ranks = str(row.ranks).split(";")
            ranks[0] = "base"
            data = {}
            for rank, lineage_id, lineage_name in zip(ranks, ids, lineage):
                if rank == "no rank":
                    continue
                data[(rank, "id")] = int(lineage_id)
                data[(rank, "name")] = lineage_name.strip()
            return pd.Series(data)

        def custom_fillna(col):
            if col.name[1] == "id":
                return col.fillna(0).astype(int)
            if col.name[1] == "name":
                return col.fillna("")

        lineage = (
            taxonomy.apply(merge_lineage, axis=1)
            .reindex(columns=columns)
            .apply(custom_fillna)
        )
        taxonomy_with_lineage = taxonomy.set_axis(
            pd.MultiIndex.from_product([taxonomy.columns, [""]]), axis=1, inplace=False
        ).merge(lineage, left_index=True, right_index=True)[
            ["scientific_name", *ranks_order[::-1], "lineage", "lineage_id", "ranks"]
        ]
        merged_taxonomy = pd.concat(
            [cached_taxonomy, taxonomy_with_lineage]
        ).sort_index()
        merged_taxonomy = merged_taxonomy[~merged_taxonomy.index.duplicated()]
        merged_taxonomy.to_csv(self.path / "taxonomy.csv")
        return merged_taxonomy

    def add_post_process(
        self,
        post_process: Union[Callable, Sequence],
        name: str,
        islands: Optional[DataFrame] = None,
        force=False,
    ):
        """Add a post process to the database.

        Args:
            post_process (Union[Callable, Sequence]): the post process.
                If a callable is provided,it should have take a row of the db as input, and return a serie.
                The method will use islands.apply(post_process, axis=1).
                Otherwise, you have to supply a Sequence that will be used to generate a DataFrame
                with the same index as the islands parameter.

            name (str): the name of the post-process.

            islands (Optional[DataFrame], optional): Defaults to None.
                The islands where the post-process is applied. Used to work on a subset of
                the database. If not provided, the full database is used.
            force (bool, optional): Defaults to False. Use that parameter to overide the already
            existing post-process.
        """
        if name == "all":
            raise ValueError("`all` is a reserved name.")
        with self.store as store:
            keys = store.keys()
        if "/post_processes/%s" % name in keys and not force:
            warnings.warn(
                "Post Process already added. Use force=True to overwrite.",
                category=UserWarning,
            )
            return None

        if islands is None:
            islands = self.islands

        if callable(post_process):
            post_process_df = pd.DataFrame(islands.apply(post_process, axis=1))
        else:
            post_process_df = pd.DataFrame(post_process)

        post_process_df.index = self._from_multi_index(islands).index
        if post_process_df.shape[1] == 1:
            post_process_df.columns = [name]
        else:
            post_process_df.columns = [
                "%s_%s" % (name, col) for col in post_process_df.columns
            ]
        with self.store as store:
            store.put("post_processes/%s" % name, post_process_df)
        self.clean_cache()

    def remove_post_process(self, name: str):
        """Remove a post process. You can clean all the post-processes
        with name="all".

        Args:
            name (str): the post process to remove (or "all" to wipe out
            all the post-processes).
        """
        try:
            if name == "all":
                node = "post_processes"
            else:
                node = "post_processes/%s" % name
            with self.store as store:
                store.remove(node)
                self.clean_cache()
        except KeyError:
            if name == "all":
                warnings.warn("No post-processes in the database.")
            else:
                warnings.warn("Post-process %s not in the database.")

    @property
    def post_processed_cols(self):
        nodes = self.post_processes
        try:
            with self.store as store:
                df = pd.concat(
                    [
                        store["/post_processes/%s" % node]
                        for node in nodes
                    ],
                    axis=1,
                    sort=False,
                )
        except ValueError:
            df = DataFrame()
        return self._to_multi_index(df)

    def update(self, islands: DataFrame):
        """Update the islands with the provided Dataframe.

        Args:
            islands (DataFrame): the DataFrame that contain the updated data.
        """
        islands = islands.drop(
            [
                "last_updated",
                "ncbi_genome_path",
                "ncbi_island_seq_path",
                "extracted_island_seq_path",
            ],
            axis=1,
            errors="ignore",
        )
        diff = islands[np.not_equal(*self.islands.align(islands, join="left"))]
        diff = diff.dropna(axis=0, how="all").dropna(axis=1, how="all")
        if diff.empty:
            warnings.warn(
                "The diff with the database seems empty. It could be because the modified key does not exist"
                "or if your updated islands are the same as the one in the database."
            )
            return
        diff.loc[:, "last_updated"] = datetime.datetime.now()

        old_updates = self.updated_islands
        new_updates, aligned_diff = old_updates.align(diff, join="outer")
        new_updates.update(aligned_diff)
        with self.store as store:
            store.put("update", self._from_multi_index(new_updates))
        self.clean_cache()

    def cancel_update(self, indexes: Union[str, Sequence[str]]):
        """Cancel a previous update.

        Args:
            indexes (Union[str, Sequence[str]]): the indexes of a previously dropped row.

        """
        if isinstance(indexes, str) and indexes == "all":
            try:
                with self.store as store:
                    store.remove("update")
                self.clean_cache()
            except KeyError:
                warnings.warn("No updates in the database.")
            return

        if isinstance(indexes, str):
            indexes = [indexes]
        with self.store as store:
            keys = store.keys()
        if "/update" in keys:
            with self.store as store:
                store.remove("update", where="index in indexes")
            self.clean_cache()

    @property
    def updated_islands(self) -> DataFrame:
        """Get updated islands.

        Returns:
            DataFrame: A dataframe that contain only the updated row.

        """
        with self.store as store:
            update_df = (
                store["update"]
                if "/update" in store.keys()
                else DataFrame(columns=["last_updated"])
            )
        update_df["last_updated"] = pd.to_datetime(update_df["last_updated"]).astype(
            "datetime64[s]"
        )
        update_df = self._to_multi_index(update_df)
        return update_df

    def drop_islands(self, islands, *, why):
        """Drop some island from the database.

        Remark:
            The islands are not wipped out, but their indexes are marked so they
            are not retrieved. They will stille appear in the raw data, and that
            drop can be canceled with AtollDB.cancel_drop

        Args:
            islands: the islands to drop
            why (str) default to "": if any, the reason of the drop.
        """
        index_to_drop = self._from_multi_index(islands.drop(islands.columns, axis=1))
        index_to_drop["why"] = why
        index_to_drop["drop_date"] = datetime.datetime.now()

        with self.store as store:
            if "/dropped" in store.keys():
                old_drops = store["dropped"]
            else:
                old_drops = pd.DataFrame()
        all_drops = pd.concat([old_drops, index_to_drop]).sort_values(
            by="drop_date"
        )
        to_put = all_drops.loc[all_drops.index.drop_duplicates(keep="last")]
        if len(to_put):
            with self.store as store:
                store.put(
                    "dropped", to_put
                )
        self.clean_cache()

    def cancel_drop(self, indexes: Union[str, Sequence[str]]):
        """Cancel a previous drop.

        Args:
            indexes (Union[str, Sequence[str]]): the indexes of a previously dropped row.
        """
        try:
            with self.store as store:
                store.remove("dropped")
            self.clean_cache()
        except KeyError:
            warnings.warn("No drops recorded.")
            return

        if isinstance(indexes, str):
            indexes = [indexes]
        with self.store as store:
            keys = store.keys
        if "/dropped" in keys:
            with self.store as store:
                store.remove("dropped", where="index in indexes")
            self.clean_cache()

    @property
    def dropped(self):
        """Get all previous drops."""
        with self.store as store:
            try:
                dropped = store["dropped"]
            except KeyError:
                dropped = DataFrame(columns=["drop_date", "why"])
        return self._to_multi_index(dropped)

    def export_database(
        self,
        output_dir: Path,
        split_files_by_source=True,
        include_fasta_path=False,
        include_fasta_files=False,
        include_taxid=True,
        force=False,
    ):
        """Export the database into tabulated separated values (tsv) file(s).

        Args:
            output_dir: folder where the base will be exported.
            split_files_by_source (bool), default False: if True, write one file per source. Otherwise, write one file with all islands.

        """
        output_dir = Path(output_dir)
        if output_dir.exists() and not force:
            raise FileExistsError(
                "The directory %s exists. Use force=True to overwrite that folder."
                % output_dir
            )
        output_dir.rmtree_p()
        output_dir.makedirs_p()

        if include_fasta_path:
            islands = self.islands_with_fpath
        else:
            islands = self.islands

        if include_taxid:
            islands = islands.join(self.taxids.astype(int), on="accession")

        if split_files_by_source:
            [
                islands.to_csv(output_dir / "%s.tsv" % source, sep="\t")
                for source in self.sources
            ]
        else:
            islands.to_csv(output_dir / "atoll.tsv", sep="\t")

        if include_fasta_files:
            self.fasta_dir.copytree(output_dir / "fasta")
