#!/usr/bin/env python
# coding=utf-8


"""
>>> for island in parse_islander_db("../data/inputs/islander.08.03.2015.db"):
...     print(island)
"""

import json
from typing import Optional

from bs4 import BeautifulSoup
from pkg_resources import resource_filename

import plumbum
from peewee import DoesNotExist, SqliteDatabase

from ..island import Island
from .islander_db import (
    Bioprojects,
    Island_,
    Islander,
    IslandSequence,
    LiteratureIslands,
    database_proxy,
)


def Island_from_db_islander(islander: Islander) -> Island:
    """extract the Islands from the `Islander` table of an Islander database.

    Args:
        islander (Islander): an Islander item (dealt via the peewee ORM).

    Returns:
        Island
    """
    accession = islander.nc
    try:
        organism = Bioprojects.get(Bioprojects.accession == accession).organism
    except DoesNotExist:
        organism = ""
    bounds = islander.island_genome_l, islander.island_genome_r
    if islander.orientation < 0:
        bounds = bounds[::-1]
    start, end = bounds
    try:
        sequence = IslandSequence.get(IslandSequence.island == islander.island).sequence
    except DoesNotExist:
        sequence = ""
    try:
        link = LiteratureIslands.get(
            LiteratureIslands.island == islander.island
        ).citation
        pmid = (
            BeautifulSoup(link, features="lxml")
            .find_all("a", href=True)[0]["href"]
            .split("/")[-1]
        )
        ref: Optional[str] = "PMID:%s" % pmid
    except DoesNotExist:
        ref = ""
    other = dict(name=islander.island)
    return Island(
        accession=accession,
        organism=organism,
        start=start,
        end=end,
        reference=ref,
        detection="islander",
        sequence=sequence,
        other=json.dumps(other),
    )


def Island_from_db_island(island: Island_) -> Island:
    """extract the Islands from the `Islander` table of an Islander database.

    Args:
        island (Island_): an Island item (dealt via the peewee ORM).

    Returns:
        Island
    """
    accession = island.nc_number
    other = {}
    try:
        organism = Bioprojects.get(Bioprojects.accession == accession).organism
    except DoesNotExist:
        organism = ""

    bounds = island.island_genome_l, island.island_genome_r
    if island.orientation < 0:
        bounds = bounds[::-1]
    start, end = bounds

    try:
        island = Islander.get(Islander.nc == accession).island
        other["name"] = island
    except DoesNotExist:
        pass

    try:
        sequence = IslandSequence.get(IslandSequence.island == other["name"]).sequence
    except (KeyError, DoesNotExist):
        sequence = ""

    try:
        link = LiteratureIslands.get(LiteratureIslands.island == other["name"]).citation
        pmid = (
            BeautifulSoup(link, features="lxml")
            .find_all("a", href=True)[0]["href"]
            .split("/")[-1]
        )
        ref: Optional[str] = "PMID:%s" % pmid
    except (KeyError, DoesNotExist):
        ref = ""

    return Island(
        accession=accession,
        organism=organism,
        start=start,
        end=end,
        reference=ref,
        detection="islander",
        sequence=sequence,
        other=json.dumps(other),
    )


mysql2sqlite_path = resource_filename("atoll.parsing", "mysql2sqlite")


def mysqldump_to_sqlite(mysqldump: str, sqlite_output: str):
    """Generate a sqlite base from a mysql dump (exported via the cli or phpmyadmin for example).

    Awk has to be installed and in the path, as well as sqlite3.

    Args:
        mysqldump (str): the mysql dump (as .sql file).
        sqlite_output (str): The requested output as sqlite base.
    """
    try:
        awk = plumbum.local["mawk"]
    except plumbum.CommandNotFound:
        awk = plumbum.local["gawk"]
    sqlite3 = plumbum.local["sqlite3"]
    mysqldumb_to_sqlitebase = (
        awk["-f", mysql2sqlite_path, mysqldump] | sqlite3[sqlite_output]
    )
    mysqldumb_to_sqlitebase()


def parse_islander_db(sqlite_path: str):
    """Parse an Islander sqlite database and yield the corresponding Islands.

    Args:
        sqlite_path (str): the path to the islander sqlite base.

    Yield:
        Island
    """
    database_proxy.initialize(SqliteDatabase(sqlite_path))
    for island in Island_.select():
        yield Island_from_db_island(island)

    for islander in Islander.select():
        yield Island_from_db_islander(islander)
