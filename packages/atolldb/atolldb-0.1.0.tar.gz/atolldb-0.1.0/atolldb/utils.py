#!/usr/bin/env python
# coding=utf-8

import itertools as it
from pkgutil import get_data
import warnings
from path import Path

from Bio.SeqRecord import SeqRecord

from .island import Island


def relpath_or_none(fasta_dir, path):
    if path:
        return fasta_dir.relpathto(path)
    return ""


def genome_to_island_sequence(genome_seq_record, start, end):
    seq = genome_seq_record.seq
    try:
        if start > end:
            sub_sequence = seq.complement()[start:end:-1]
        else:
            sub_sequence = seq[start:end]
    except IndexError:
        return None
    if not sub_sequence:
        return None

    id_ = genome_seq_record.id
    description = "Coordinate %s-%s; %s" % (start, end, genome_seq_record.description)
    name = genome_seq_record.name
    dbxrefs = genome_seq_record.dbxrefs
    return SeqRecord(
        seq=sub_sequence, name=name, dbxrefs=dbxrefs, id=id_, description=description
    )


index_access = get_data("atoll", "index.acc_num.txt")


def filter_not_seq_len(island):
    return not island.seq_len
