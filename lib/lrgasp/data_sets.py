"""Class to load pre-built data set information from JSON files in source .  All results are cached"""
import os.path as osp
import csv
# import json
from lrgasp import LrgaspException
from lrgasp.objDict import ObjDict
from lrgasp.defs import Species, RefGenome, Gencode, Sample, LibraryCategory

class LrgaspRun(ObjDict):
    """Used to create an LRGASP run object for sequencing data"""
    def __init__(self, *, sample, run_acc, description, library_prep, platform):
        self.sample = sample
        self.run_acc = run_acc
        self.description = description
        self.library_prep = library_prep
        self.platform = platform
        self.replicates = None

class LrgaspReplicate(ObjDict):
    """collection of files for a replicate"""
    def __init__(self, replicate_number):
        self.replicate_number = replicate_number
        self.files = []

class LrgaspRnaSeqFile(ObjDict):
    """One data file from an RNA-Seq run, uses to build JSON in a consistency way"""
    def __init__(self, *, file_acc, file_type, url, s3_uri, file_size, md5sum, biological_replicate_number):
        self.file_acc = file_acc
        self.file_type = file_type
        self.url = url
        self.s3_uri = s3_uri
        self.file_size = file_size
        self.md5sum = md5sum
        self.biological_replicate_number = biological_replicate_number

def _load_tsv(tsv_basefile, fieldTypeMap):
    """load TSV into an ObjDict; if not None,fieldTypeMap is used to covert fields
    from string to types"""
    recs = []
    with open(osp.join(osp.dirname(__file__), "data", tsv_basefile), newline='') as fh:
        for csv_rec in csv.DictReader(fh, dialect=csv.excel_tab):
            rec = ObjDict(csv_rec)
            recs.append(rec)
            if fieldTypeMap is not None:
                for field in fieldTypeMap.keys():
                    rec[field] = fieldTypeMap[field](rec[field])
    return recs

def field_or_none(val, cls):
    """return value as a SymEnum or None"""
    if val == "":
        return None
    else:
        return cls(val)

class LrgaspGenomeAnnotations(list):
    """genome annotation sources from data matrix TSV"""
    cache = None

def get_lrgasp_genome_anotations():
    if LrgaspGenomeAnnotations.cache is None:
        fieldTypeMap = {"species": Species,
                        "name": RefGenome}
        LrgaspGenomeAnnotations.cache = LrgaspGenomeAnnotations(_load_tsv('genome-annotations.tsv',
                                                                          fieldTypeMap))
    return LrgaspGenomeAnnotations.cache

class LrgaspGenomeAssemblies(list):
    """genome assemblies from data matrix TSV"""
    cache = None

def get_lrgasp_genome_assemblies():
    if LrgaspGenomeAssemblies.cache is None:
        fieldTypeMap = {"species": Species,
                        "name": Gencode}
        LrgaspGenomeAssemblies.cache = LrgaspGenomeAnnotations(_load_tsv('genome-annotations.tsv',
                                                                         fieldTypeMap))
    return LrgaspGenomeAssemblies.cache

class LrgaspRnaSeq(list):
    """genome assemblies from data matrix TSV"""
    cache = None

    def __init__(self, recs):
        self.by_acc = {}
        for rec in recs:
            self.add(rec)

    def add(self, rec):
        self.append(rec)
        if rec.accession != "":  # not yet complete
            if rec.accession in self.by_acc:
                raise LrgaspException("duplicate RNA-Seq BAM accession: " + rec.accession)
            self.by_acc[rec.accession] = rec

    def get_by_acc(self, acc):
        "error if not an LRGASP accession"
        try:
            return self.by_acc[acc]
        except KeyError:
            raise LrgaspException(f"LRGASP RNA-Seq accession {acc} is unknown")

def get_lrgasp_rna_seq():
    if LrgaspRnaSeq.cache is None:
        fieldTypeMap = {"species": Species,
                        "sample": lambda val: field_or_none(val, Sample),
                        "library_category": LibraryCategory}
        LrgaspRnaSeq.cache = LrgaspRnaSeq(_load_tsv('rna-seq-bams.tsv', fieldTypeMap))
    return LrgaspRnaSeq.cache
