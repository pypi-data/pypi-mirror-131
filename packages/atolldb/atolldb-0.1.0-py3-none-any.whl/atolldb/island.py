#!/usr/bin/env python
# coding=utf-8

import datetime
import json
import re
from pkgutil import get_data
from typing import Any, Optional, Sequence

import attr
import numpy as np
import pandas as pd
from fuzzywuzzy import process
from slugify import slugify
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq


@attr.s
class AccessionOrganismMapping:
    """Construct two dict, given a string that contain one tuple organism / accession number per line, separated with tab.

    Methods:
        get_accession_number: return the accession given an organism in natural form.

    Properties:
        accession_to_organism: a dict with accession as keys, organism as values
        organism_to_accession: a dict with organism as key in a canonical form, accession as values


    """

    index_txt = attr.ib(type=str)
    accession_indexes = attr.ib(type=Optional[Sequence[str]], default=None, init=False)
    organisms = attr.ib(type=Optional[Sequence[str]], default=None, init=False)
    slug_organisms = attr.ib(type=Optional[Sequence[str]], default=None, init=False)

    @property
    def organism_to_accession(self):
        return dict(zip(self.slug_organisms, self.accession_indexes))

    @property
    def accession_to_organism(self):
        return dict(zip(self.accession_indexes, self.organisms))

    def get_accession_number(
        self, organism: str, fuzzy: bool = False, threshold: int = 99
    ) -> Optional[str]:
        """Extract the accession number that correspond to the the best match between the organism provided and the ones available if its score is higher than the threshold.

        Args:
            organism (str): user provided organism name.
            fuzzy (bool): if True, use a fuzzy search to extract the best match if the exact key is not in the organism list.
            threshold (int): the score threshold.

        Returns:
            Optional[str]: the accession number, or None if organism not in the available ones.
        """
        try:
            return self.organism_to_accession[slugify(organism, separator="")]
        except KeyError:
            pass
        if fuzzy:
            match, score = process.extractOne(
                slugify(organism, separator=""), self.slug_organisms
            )
            if score >= threshold:
                return match
        return None

    @staticmethod
    def _slugify_organism(organism: str) -> str:
        """Transform the organism in a canonical form in order to compare them.

        Args:
            organism (str): The original organism

        Returns:
            str: the canonical form of the sequence (as slug)
        """
        organism = (
            organism.split(",")[0]
            .replace("complete sequence", "")
            .replace("complete genome", "")
        )
        return slugify(organism, separator="")

    def __attrs_post_init__(self):
        self.accession_indexes, self.organisms = zip(
            *[line.strip().split("\t") for line in self.index_txt.strip().split("\n")]
        )
        self.slug_organisms = list(map(self._slugify_organism, self.organisms))


accession_re = re.compile(r"(([A-Z]+|[A-Z]+_[A-Z]*)[0-9]+(_\w+)?)")


def other_to_accession(other: str) -> Optional[str]:
    """other_to_accession

    Args:
        other (str): The other string that could contain one or more accession number

    Returns:
        Optional[Tuple[str, str]]: the first match of an accession number if any, None otherwise.
    """
    matches = accession_re.findall(other)
    if not matches:
        return None
    matches = [match[0] for match in matches]
    accession = matches[0]
    return accession


index_access = get_data("atoll", "index.acc_num.txt")
if index_access:
    accession_mapping = AccessionOrganismMapping(index_access.decode())


def capitalize(string: Any) -> str:
    """ Put the sequence upper if any.

    Args:
        seq (str)

    Returns:
        str: the sequence with upper letter.
    """
    if isinstance(string, str):
        return string.capitalize()
    return ""


def convert_other(other):
    return json.dumps(other)


@attr.s
class Island:
    """Data container that represent an Island.
    """

    # The accession number (NC_####### or NZ_#######)
    accession = attr.ib(type=Optional[str], default="", converter=str)
    version = attr.ib(type=Optional[int], default="", converter=str)
    organism = attr.ib(type=Optional[str], default="", converter=str)
    start = attr.ib(type=Optional[int], default=0, converter=int)
    end = attr.ib(type=Optional[int], default=0, converter=int)
    insertion = attr.ib(type=Optional[str], default="", converter=str)
    # Where come the island (islander, ICEberg...)
    detection = attr.ib(type=Optional[str], default="", converter=capitalize)
    reference = attr.ib(type=Optional[str], default="", converter=str)
    type_ = attr.ib(type=Optional[str], default="", converter=str)
    other = attr.ib(type=Optional[str], default="{}", converter=convert_other)
    sequence = attr.ib(type=Optional[SeqRecord], default="", repr=False)
    seq_len = attr.ib(type=Optional[int], converter=int)
    last_updated = attr.ib(
        type=datetime.datetime, init=False, factory=datetime.datetime.now
    )

    dtype = {
        "accession": str,
        "version": str,
        "organism": str,
        "insertion": str,
        "type_": str,
        "other": str,
        "detection": str,
        "start": int,
        "end": int,
        "seq_len": int,
        "last_updated": str,
    }

    @seq_len.default
    def compute_seq_len(self):
        if self.start and self.end:
            return np.abs(self.end - self.start)
        elif self.sequence:
            return len(self.sequence)
        return 0

    def _extract_accession(self):
        """If the accession is unavailable, try to extract it
        - from the other field
        - from the organism and the accession mapping provided as couples accession_number / organism
        """

        if self.accession:
            return

        if self.other:
            accession = other_to_accession(json.loads(self.other))
            if accession:
                self.accession = accession
                return

        if self.organism and accession_mapping:
            self.accession = accession_mapping.get_accession_number(self.organism)

    def _convert_accession(self):
        caption = self.accession.split(".")[0]
        if not self.version and len(self.accession.split(".")) > 1:
            try:
                self.version = self.accession.split(".")[-1]
            except ValueError:
                pass
        self.accession = caption.strip()

    def to_dict(self):
        return attr.asdict(self)

    @staticmethod
    def to_df(islands):
        df = pd.DataFrame(
            [island.to_dict() for island in islands],
            columns=[attrib.name for attrib in Island.__attrs_attrs__],
        )
        # df = df.drop("sequence")
        df.start = df.start.fillna(0)
        df.end = df.end.fillna(0)
        df.seq_len = df.seq_len.fillna(0)
        df = df.astype(dtype=Island.dtype)
        df = df.replace("None", "")
        return df

    @staticmethod
    def columns():
        return [attrib.name for attrib in Island.__attrs_attrs__]

    @staticmethod
    def from_df(df):
        cols = Island.columns()
        cols.remove("last_updated")
        return [
            Island(**row.to_dict())
            for _, row in df.reindex(columns=cols)[cols].iterrows()
        ]

    def __attrs_post_init__(self):
        if not self.accession:
            self._extract_accession()
        self._convert_accession()
        self.start, self.end = sorted([self.start, self.end])
        if isinstance(self.sequence, str) and self.sequence != "":
            self.sequence = SeqRecord(
                id=self.accession,
                seq=Seq(self.sequence.upper()),
                description="%s_%i:%i" % (self.detection, self.start, self.end),
            )
