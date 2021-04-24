"""Class to load pre-built data set information from JSON files in source .  All results are cached"""
import os.path as osp
import json
from lrgasp import LrgaspException
from lrgasp.objDict import ObjDict
from lrgasp.defs import Species, Sample, LibraryPrep, Platform

##
# LRGASP run metadata files in lib/lrgasp/data/
##
lrgasp_run_metadata_files = ("encode-metadata.json", "manatee-metadata.json")


class LrgaspRun(ObjDict):
    """Used to create an LRGASP run object for sequencing data. Class is only uses
    to serialized, ObjDict used to access when deserialized."""
    def __init__(self, *, species, sample, run_acc, description, library_prep, platform):
        self.species = species
        self.sample = sample
        self.run_acc = run_acc
        self.description = description
        self.library_prep = library_prep
        self.platform = platform
        self.replicates = None

class LrgaspReplicate(ObjDict):
    """collection of files for a replicate. Class is only uses
    to serialized, ObjDict used to access when deserialized."""
    def __init__(self, replicate_number):
        self.replicate_number = replicate_number
        self.files = []

class LrgaspRnaSeqFile(ObjDict):
    """One data file from an RNA-Seq run, uses to build JSON in a consistency way
    Class is only uses to serialized, ObjDict used to access when
    deserialized."""
    def __init__(self, *, file_acc, file_type, url, s3_uri, file_size, md5sum, run_acc, biological_replicate_number,
                 output_type, paired_end=None, paired_with=None):
        self.file_acc = file_acc
        self.file_type = file_type
        self.url = url
        self.s3_uri = s3_uri
        self.file_size = file_size
        self.md5sum = md5sum
        self.run_acc = run_acc
        self.biological_replicate_number = biological_replicate_number
        self.output_type = output_type
        self.paired_end = paired_end
        self.paired_with = paired_with

class LrgaspRnaSeqMetaData(list):
    """deserialized LRSGAP RNA-Seq metadata, along with access methods"""
    cache = None

    def __init__(self):
        self.by_file_acc = {}
        self.by_run_acc = {}

    def _edit_run_types(self, run):
        "conversion to SymEnum"
        run.species = Species(run.species)
        run.sample = Sample(run.sample)
        run.library_prep = LibraryPrep(run.library_prep)
        run.platform = Platform(run.platform)

    def _add_files(self, files):
        for fil in files:
            if fil.file_acc in self.by_file_acc:
                raise LrgaspException("duplicate file accession: " + fil.file_acc)
            self.by_file_acc[fil.file_acc] = fil

    def add(self, run):
        self._edit_run_types(run)
        if run.run_acc in self.by_run_acc:
            raise LrgaspException("duplicate run id: " + run.run_acc)
        self.append(run)
        self.by_run_acc[run.run_acc] = run
        for replicate in run.replicates:
            self._add_files(replicate.files)

    def get_file_by_acc(self, file_acc):
        try:
            return self.by_file_acc[file_acc]
        except KeyError:
            raise LrgaspException(f"unknown LRGASP file accession {file_acc}, file accession should be from the LRGASP RNA-Seq data matrix")

    def get_run_by_acc(self, run_acc):
        try:
            return self.by_run_acc[run_acc]
        except KeyError:
            raise LrgaspException(f"unknown LRGASP run accession {run_acc}, run accession should be from the LRGASP RNA-Seq data matrix")

    def get_run_by_file_acc(self, file_acc):
        fil = self.get_file_by_acc(file_acc)
        return self.get_run_by_acc(fil.run_acc)

def _load_lrgasp_rna_seq_metadata_file(rna_seq_md, metadata_json):
    with open(metadata_json) as fh:
        for run in json.load(fh, object_pairs_hook=ObjDict):
            rna_seq_md.add(run)

def _load_lrgasp_rna_seq_metadata_files():
    "load of all metadata files when not cached"
    rna_seq_md = LrgaspRnaSeqMetaData()
    for json_file in lrgasp_run_metadata_files:
        json_path = osp.join(osp.dirname(__file__), "data", json_file)
        try:
            _load_lrgasp_rna_seq_metadata_file(rna_seq_md, json_path)
        except Exception as ex:
            raise LrgaspException(f"failed to load {json_path}") from ex
    return rna_seq_md

def get_lrgasp_rna_seq_metadata():
    """get LRGASP metadata, possible cached"""
    if LrgaspRnaSeqMetaData.cache is None:
        LrgaspRnaSeqMetaData.cache = _load_lrgasp_rna_seq_metadata_files()
    return LrgaspRnaSeqMetaData.cache
