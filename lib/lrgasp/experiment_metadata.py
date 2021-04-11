"""
Experiment metadata parsing and validation.
"""
import os.path as osp
import json
from collections import defaultdict
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.defs import Repository, Species, ExperimentType, DataCategory, LibraryPrep, LibraryCategory, ExpressionUnits, validate_symbolic_ident, EXPERIMENT_JSON
from lrgasp.metadata_validate import Field, check_from_defs, validate_url
from lrgasp.data_sets import get_lrgasp_rna_seq

fld_experiment_id = Field("experiment_id", validator=validate_symbolic_ident)
fld_experiment_type = Field("experiment_type", ExperimentType)
fld_description = Field("description")
fld_species = Field("species", Species)
fld_data_category = Field("data_category", DataCategory)
fld_libraries = Field("libraries", list, element_dtype=str, validator=validate_symbolic_ident)
fld_extra_libraries = Field("extra_libraries", list, optional=True, element_dtype=dict)
fld_units = Field("units", ExpressionUnits, optional=True)
fld_software = Field("software", list, element_dtype=dict)
fld_notes = Field("notes", allow_empty=True, optional=True)

experiment_fields = (
    fld_experiment_id,
    fld_experiment_type,
    fld_species,
    fld_description,
    fld_data_category,
    fld_libraries,
    fld_extra_libraries,
    fld_units,
    fld_software,
    fld_notes,
)

fld_acc = Field("acc")
fld_repository = Field("repository", Repository)

extra_library_fields = (
    fld_acc,
    fld_repository,
    fld_notes,
)

fld_name = Field("name")
fld_version = Field("version")
fld_url = Field("url", validator=validate_url)
fld_config = Field("url", allow_empty=True, optional=True)

experiment_software_fields = (
    fld_name,
    fld_version,
    fld_url,
    fld_config,
    fld_notes,
)

def get_extra_libraries(experiment):
    """get the extra libraries field, or empty if not specified"""
    return experiment.get("extra_libraries", ())

def find_dups(lst):
    dups = []
    found = set()
    for v in lst:
        if (v in found) and (v not in dups):
            dups.append(v)
        found.add(v)
    return sorted(dups)

def library_validate(experiment, lrgasp_rna_seq, library):
    rna_seq = lrgasp_rna_seq.get_by_acc(library)  # exception if unknown acc
    if rna_seq.species != experiment.species:
        raise LrgaspException(f"LRGASP RNA Seq library {rna_seq.accession} is for species {rna_seq.species} while experiment {experiment.experiment_id} specifies species as {experiment.species}")

def group_libs_by_cat(lrgasp_rna_seq, libraries):
    libs_by_cat = defaultdict(list)
    for lib in libraries:
        libs_by_cat[lrgasp_rna_seq.get_by_acc(lib).library_category] = lib
    libs_by_cat.default_factory = None
    return libs_by_cat

def to_strlist(values):
    "make into comma-separate lists"
    return ",".join([str(v) for v in values])

def libraries_validate_compat(experiment, lrgasp_rna_seq, libraries):
    """compatibility between libraries and with experiment data category"""
    # FIXME: this needs cleaned up
    libs_by_cat = group_libs_by_cat(lrgasp_rna_seq, libraries)
    cats = frozenset(libs_by_cat.keys())
    long_cats = cats - set([LibraryCategory.Illumina_cDNA])
    if experiment.data_category == DataCategory.short_only:
        if len(long_cats) > 0:
            raise LrgaspException(f"{experiment.data_category} experiments can't use long-read libraries: " + to_strlist(cats))
        if LibraryCategory.Illumina_cDNA not in cats:
            raise LrgaspException(f"{experiment.data_category} experiments must include {LibraryCategory.Illumina_cDNA}: " + to_strlist(cats))
    elif experiment.data_category == DataCategory.long_only:
        if len(long_cats) != 1:
            raise LrgaspException(f"{experiment.data_category} experiments must contain one long-read libraries prep: " + to_strlist(cats))
        if LibraryCategory.Illumina_cDNA in cats:
            raise LrgaspException(f"{experiment.data_category} experiments must not include {LibraryCategory.Illumina_cDNA}: " + to_strlist(cats))
    elif experiment.data_category == DataCategory.long_short:
        if len(long_cats) != 1:
            raise LrgaspException(f"{experiment.data_category} experiments must contain one long-read libraries prep: " + to_strlist(cats))
        if LibraryCategory.Illumina_cDNA not in cats:
            raise LrgaspException(f"{experiment.data_category} experiments must include {LibraryCategory.Illumina_cDNA}: " + to_strlist(cats))
    elif experiment.data_category == DataCategory.kitchen_sink:
        # FIXME: check if should be om other category
        pass
    else:
        raise LrgaspException("bug")

def libraries_validate(experiment):
    dups = find_dups(experiment.libraries)
    if len(dups) > 0:
        raise LrgaspException(f"duplicate accession in libraries: {dups}")

    # make sure all are known
    lrgasp_rna_seq = get_lrgasp_rna_seq()
    for library in experiment.libraries:
        library_validate(experiment, lrgasp_rna_seq, library)
    libraries_validate_compat(experiment, lrgasp_rna_seq, experiment.libraries)

def extra_library_validate(extra_library):
    desc = "experiment.extra_libraries"
    check_from_defs(desc, extra_library_fields, extra_library)

def extra_libraries_validate(experiment):
    if experiment.data_category != DataCategory.kitchen_sink:
        raise LrgaspException("experiment extra_libraries may only be specified for kitchen_sink experiments")
    dups = find_dups([el.acc for el in experiment.extra_libraries])
    if len(dups) > 0:
        raise LrgaspException(f"duplicate accession in extra libraries: {dups}")
    for extra_library in experiment.extra_libraries:
        extra_library_validate(extra_library)

def experssion_units_validate(experiment):
    if experiment.experiment_type is ExperimentType.model:
        if fld_units.name in experiment:
            raise LrgaspException(f"experiment type {experiment.experiment_type} must not specify {fld_units.name}")
    else:
        if fld_units.name not in experiment:
            raise LrgaspException(f"experiment type {experiment.experiment_type} must specify {fld_units.name}")

def experiment_validate(experiment):
    desc = "experiment"
    check_from_defs(desc, experiment_fields, experiment)
    libraries_validate(experiment)
    if len(get_extra_libraries(experiment)) > 0:
        extra_libraries_validate(experiment)
    experssion_units_validate(experiment)

def load(experiment_json):
    """load and validate experiment metadata"""
    try:
        with gopen(experiment_json) as fh:
            experiment = json.load(fh, object_pairs_hook=ObjDict)
    except json.decoder.JSONDecodeError as ex:
        raise LrgaspException(f"parse of experiment metadata (JSON) failed: {experiment_json}") from ex
    try:
        experiment_validate(experiment)
    except LrgaspException as ex:
        raise LrgaspException(f"validation of experiment metadata failed: {experiment_json}") from ex
    return experiment

def load_from_entry(entry, experiment_id):
    """load and validation experiment metadata given a entry,
    add experiment_dir to metadata"""
    experiment_dir = osp.join(entry.entry_dir, experiment_id)
    experiment_json = osp.join(experiment_dir, EXPERIMENT_JSON)
    try:
        experiment = load(experiment_json)
    except (LrgaspException, FileNotFoundError, ValueError) as ex:
        raise LrgaspException(f"error parse metadata for entry {entry.entry_id}, experiment {experiment_id}: {experiment_json}") from ex
    experiment.experiment_dir = experiment_dir
    return experiment
