#!/usr/bin/env python
# coding=utf-8

from peewee import (
    SQL,
    CharField,
    CompositeKey,
    FloatField,
    IntegerField,
    Model,
    Proxy,
    TextField,
)

database_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


# class Accessions(BaseModel):
#     acc_id = CharField(null=True)
#     accession = CharField(null=True)
#     id = CharField(null=True)
#     start_stop = CharField(null=True)
#     tmrna_id = IntegerField(null=True)

#     class Meta:
#         table_name = "accessions"
#         primary_key = False


class Bioprojects(BaseModel):
    accession = CharField(primary_key=True)
    category = CharField()
    gc = FloatField()
    length = IntegerField()
    lineage = TextField()
    organism = TextField()
    project = IntegerField()

    class Meta:
        table_name = "bioprojects"


# class FalsePositives(BaseModel):
#     island = TextField(primary_key=True)
#     leaveout = TextField()

#     class Meta:
#         table_name = "false_positives"


class Island_(BaseModel):
    bacteria_nickname = CharField(column_name="Bacteria_nickname", null=True)
    comment = IntegerField(column_name="Comment", null=True)
    damage_l = IntegerField(column_name="Damage_L", null=True)
    damage_r = IntegerField(column_name="Damage_R", null=True)
    dupli_l = IntegerField(column_name="Dupli_L", null=True)
    dupli_r = IntegerField(column_name="Dupli_R", null=True)
    extend = IntegerField(column_name="Extend", null=True)
    frag_l = IntegerField(column_name="Frag_L", null=True)
    frag_r = IntegerField(column_name="Frag_R", null=True)
    gc_content = CharField(column_name="GC_Content", null=True)
    ir_version = IntegerField(column_name="IR_Version", null=True)
    index_point = IntegerField(column_name="Index_Point", null=True)
    int_subfam = IntegerField(column_name="Int_Subfam", null=True)
    island = CharField(column_name="Island", primary_key=True)
    island_genome_l = IntegerField(column_name="Island_Genome_L", null=True)
    island_genome_r = IntegerField(column_name="Island_Genome_R", null=True)
    markup = TextField(column_name="Markup", null=True)
    mismatch = CharField(column_name="Mismatch", null=True)
    orientation = IntegerField(column_name="Orientation", null=True)
    portion = CharField(column_name="Portion", null=True)
    ftp_folder = CharField(null=True)
    nc_number = CharField(null=True)
    trna = CharField(column_name="tRNA", null=True)
    trna_l = IntegerField(column_name="tRNA_L", null=True)
    trna_r = IntegerField(column_name="tRNA_R", null=True)

    class Meta:
        table_name = "island"
        primary_key = False


class Islander(BaseModel):
    dupli_l = TextField(column_name="Dupli_L")
    dupli_r = TextField(column_name="Dupli_R")
    frag_l = IntegerField(column_name="Frag_L")
    frag_r = IntegerField(column_name="Frag_R")
    indexpoint = IntegerField(column_name="IndexPoint")
    mismatch = TextField(column_name="Mismatch")
    bact_nickname = TextField()
    gc_content = TextField()
    int_family = IntegerField()
    ir_version = IntegerField()
    island = TextField(primary_key=True)
    island_genome_l = IntegerField()
    island_genome_r = IntegerField()
    island_index = IntegerField(index=True)
    lineage = TextField()
    nc = TextField()
    orientation = IntegerField()
    portion = TextField()
    strain = TextField()
    trna = TextField(column_name="tRNA")
    trna_l = TextField(column_name="tRNA_L")
    trna_r = TextField(column_name="tRNA_R")

    class Meta:
        table_name = "islander"
        indexes = ((("island", "island_genome_l", "island_genome_r", "trna"), True),)


class IslandSequence(BaseModel):
    island = TextField(primary_key=True)
    sequence = TextField()

    class Meta:
        table_name = "island_sequence"
        primary_key = False


class LiteratureIslands(BaseModel):
    accession = TextField()
    citation = TextField()
    island = TextField()
    left = IntegerField()
    literature_name = TextField()
    right = IntegerField()

    class Meta:
        table_name = "literature_islands"
        primary_key = CompositeKey("island", "literature_name")
