"""Class to Load data matrix TSVs.  All results are cached"""
import os.path as osp
import csv
from lrgasp import LrgaspException
from lrgasp.objDict import ObjDict
from lrgasp.defs import Species, RefGenome, Gencode, Sample, LibraryPrep

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
                        "library": LibraryPrep}
        LrgaspRnaSeq.cache = LrgaspRnaSeq(_load_tsv('rna-seq-bams.tsv', fieldTypeMap))
    return LrgaspRnaSeq.cache
