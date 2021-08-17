"""Class to load pre-built data set information from JSON files in source .  All results are cached"""
import os.path as osp
import json
from collections import defaultdict, namedtuple
from lrgasp import LrgaspException
from lrgasp.objDict import ObjDict
from lrgasp.defs import Species, Sample, LibraryPrep, Platform

##
# LRGASP run metadata files in lib/lrgasp/data/
##
lrgasp_run_metadata_files = ("encode-metadata.json", "simulated-metadata.json", )


class LrgaspRun(ObjDict):
    """Used to create an LRGASP run object for sequencing data. Class is only used
    to serialized, ObjDict is used to access when deserialized."""
    def __init__(self, *, species, sample, run_acc, description, library_prep, platform):
        self.species = species
        self.sample = sample
        self.run_acc = run_acc
        self.description = description
        self.library_prep = library_prep
        self.platform = platform
        self.replicates = None

class LrgaspReplicate(ObjDict):
    """Collection of files for a replicate within a run.   Note that a given
    Biosample and replicated can be used by multiple runs.  Class is only used
    to serialized, ObjDict is used to access when deserialized."""
    def __init__(self, replicate_number, biosample_accs, size_range):
        self.replicate_number = replicate_number
        self.biosample_accs = biosample_accs  # deserialized as a sorted tuple
        self.size_range = size_range
        self.files = []
        # self.run_md = added when deserialized

class LrgaspRnaSeqFile(ObjDict):
    """One data file from an RNA-Seq run, used to build JSON in a consistent way
    Class is only used to serialized, ObjDict is used to access when deserialized.
    When deserialized paired files will be link
    """
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
        # self.paired_file is built when deserialized
        # self.replicate_md = added when deserialized

class RunType(namedtuple("RunType",
                         ("sample", "library_prep", "platform"))):
    "attributes describing a run"

    def __str__(self):
        return str(self.sample) + '/' + str(self.library_prep) + '/' + str(self.platform)

class LrgaspRnaSeqMetaData(list):
    """deserialized LRSGAP RNA-Seq metadata, along with access methods"""
    cache = None

    def __init__(self):
        self.file_md_by_acc = {}
        self.run_by_acc = {}

        # indexed by (library_prep, platform)
        self.runs_by_prep_platform = defaultdict(list)

        # this is indexed by both individual biosample accs and by sorted
        # tuple of accs to handle mixes.  The same values can map to replicates
        # in different sequences technologies, hence it is a list
        self.replicate_by_biosample_acc = defaultdict(list)

    def finish(self):
        self.runs_by_prep_platform.default_factory = None
        self.replicate_by_biosample_acc.default_factory = None

    def _edit_run_types(self, run_md):
        "conversion to SymEnum"
        run_md.species = Species(run_md.species)
        run_md.sample = Sample(run_md.sample)
        run_md.library_prep = LibraryPrep(run_md.library_prep)
        run_md.platform = Platform(run_md.platform)

    def _add_file(self, replicate_md, file_md):
        if file_md.file_acc in self.file_md_by_acc:
            raise LrgaspException(f"duplicate file accession '{file_md.file_acc}'")
        self.file_md_by_acc[file_md.file_acc] = file_md
        file_md.replicate_md = replicate_md
        if file_md.paired_file is not None:
            self.file_md_by_acc[file_md.paired_file.file_acc] = file_md.paired_file

    def _add_files(self, replicate_md, file_mds):
        for file_md in file_mds:
            self._add_file(replicate_md, file_md)

    def _add_biosample(self, replicate_md):
        # add by both all samples and sorted tuple
        self.replicate_by_biosample_acc[replicate_md.biosample_accs] = replicate_md
        for acc in replicate_md.biosample_accs:
            self.replicate_by_biosample_acc[acc] = replicate_md

    def _add_replicate(self, run_md, replicate_md):
        replicate_md.run_md = run_md
        self._add_biosample(replicate_md)
        self._add_files(replicate_md, replicate_md.files)

    def add(self, run_md):
        self._edit_run_types(run_md)
        if run_md.run_acc in self.run_by_acc:
            raise LrgaspException(f"duplicate run id '{run_md.run_acc}'")
        self.append(run_md)
        self.run_by_acc[run_md.run_acc] = run_md
        self.runs_by_prep_platform[run_md.library_prep, run_md.platform].append(run_md)
        for replicate_md in run_md.replicates:
            self._add_replicate(run_md, replicate_md)

    def get_file_by_acc(self, file_acc):
        try:
            return self.file_md_by_acc[file_acc]
        except KeyError:
            raise LrgaspException(f"unknown LRGASP file accession '{file_acc}', file accession must be one in the LRGASP RNA-Seq data matrix")

    def get_run_by_acc(self, run_acc):
        try:
            return self.run_by_acc[run_acc]
        except KeyError:
            raise LrgaspException(f"unknown LRGASP run accession '{run_acc}', run accession should be one in the LRGASP RNA-Seq data matrix")

    def get_run_by_file_acc(self, file_acc):
        fil = self.get_file_by_acc(file_acc)
        return self.get_run_by_acc(fil.run_acc)

    def get_runs_by_prep_platform(self, library_prep, platform):
        "get runs for prep/platform"
        return self.runs_by_prep_platform.get((library_prep, platform), ())

def get_run_type(run_md):
    return RunType(run_md.sample, run_md.library_prep, run_md.platform)

def _pair_files(file_mds):
    "linked paired ends files and construct list of pairs"
    files_by_acc = {f.file_acc: f for f in file_mds}
    paired_files = []
    while len(files_by_acc) > 0:
        _, file_md = files_by_acc.popitem()
        if file_md.paired_end is None:
            file_md.paired_file = None
            paired_files.append(file_md)
        else:
            # put in right order
            paired_md = files_by_acc.pop(file_md.paired_with)
            p1, p2 = (file_md, paired_md) if file_md.paired_end < paired_md.paired_end else (paired_md, file_md)
            p1.paired_file = p2
            p2.paired_file = p1
            paired_files.append(p1)
    return paired_files

def _edit_run(run_md):
    """Modify deserialized run. Link paired end files and convert biosample_accs
    to a sorted tuple"""
    for rep in run_md.replicates:
        rep.files = _pair_files(rep.files)
        rep.biosample_accs = tuple(sorted(rep.biosample_accs))
    return run_md

def _load_lrgasp_rna_seq_metadata_file(rna_seq_md, metadata_json):
    with open(metadata_json) as fh:
        for run_md in json.load(fh, object_pairs_hook=ObjDict):
            rna_seq_md.add(_edit_run(run_md))

def _load_lrgasp_rna_seq_metadata_files():
    "load of all metadata files when not cached"
    rna_seq_md = LrgaspRnaSeqMetaData()
    for json_file in lrgasp_run_metadata_files:
        json_path = osp.join(osp.dirname(__file__), "data", json_file)
        try:
            _load_lrgasp_rna_seq_metadata_file(rna_seq_md, json_path)
        except Exception as ex:
            raise LrgaspException(f"failed to load '{json_path}'") from ex
    rna_seq_md.finish()
    return rna_seq_md

def get_lrgasp_rna_seq_metadata():
    """get LRGASP metadata, possible cached"""
    if LrgaspRnaSeqMetaData.cache is None:
        LrgaspRnaSeqMetaData.cache = _load_lrgasp_rna_seq_metadata_files()
    return LrgaspRnaSeqMetaData.cache
