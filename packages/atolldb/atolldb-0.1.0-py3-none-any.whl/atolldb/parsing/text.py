#!/usr/bin/env python
# coding=utf-8

"""
>>> for island in parse_islandviewer_files("../data/inputs/all_gis_islander_iv4.txt"):
...     print(island)
"""


import pandas as pd

from ..island import Island, accession_mapping


def get_organism(accession: str):
    """Use the internal mapping file to get an organism from an accession number.

    Args:
        accession (str): the requested accession number.

    Returns:
        str: the corresponding organism.
    """
    return accession_mapping.accession_to_organism.get(accession, None)


def parse_islandviewer_files(file: str, chunksize=100):
    """Parse an islandviewer tsv and yield the corresponding Islands.

    Args:
        file (str): the islandviewer text file.

    Yield:
        Island
    """

    chunks = pd.read_csv(
        file,
        sep=",",
        names=["accession", "start", "end", "detection"],
        skiprows=1,
        chunksize=chunksize,
    )

    if not chunksize:
        chunks = [chunks]

    for df in chunks:
        df["organism"] = list(map(get_organism, df["accession"]))
        for i, row in df.iterrows():
            yield Island(**row.to_dict())
