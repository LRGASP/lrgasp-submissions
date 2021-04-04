"""
Experiment metadata parsing and validation.
"""
import os.path as osp
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.defs import Repository, Species, ExperimentType, DataCategory, ExpressionUnits, validate_symbolic_ident, EXPERIMENT_JSON
from lrgasp.metadata_validate import Field, check_from_defs, validate_url
from lrgasp.data_matrix import get_lrgasp_rna_seq

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

def library_validate(experiment, lrgasp_rna_seq, library):
    rna_seq = lrgasp_rna_seq.get_by_acc(library)  # exception if unknown acc
    if rna_seq.species != experiment.species:
        raise LrgaspException(f"LRGASP RNA Seq library {rna_seq.accession} is for species {rna_seq.species} while experiment {experiment.experiment_id} specifies species as {experiment.species}")

def libraries_validate_compat(experiment, lrgasp_rna_seq, libraries):
    """compatibility between libraries and experiment category"""
    libs = [lrgasp_rna_seq.get_by_acc(l).library for l in libraries]
    if len(set(libs)) != 1:
        raise LrgaspException("all LRGASP libraries must be of the same type: {} are {}".format(",".join(libraries), ",".join([str(l) for l in libs])))

def libraries_validate(experiment, libraries):
    # FIXME: check for dups or conflised
    lrgasp_rna_seq = get_lrgasp_rna_seq()
    for library in libraries:
        library_validate(experiment, lrgasp_rna_seq, library)
    libraries_validate_compat(experiment, lrgasp_rna_seq, libraries)

def extra_library_validate(extra_library):
    desc = "experiment.extra_libraries"
    check_from_defs(desc, extra_library_fields, extra_library)

def extra_libraries_validate(extra_libraries):
    for extra_library in extra_libraries:
        extra_library_validate(extra_library)

def experiment_validate(experiment):
    desc = "experiment"
    check_from_defs(desc, experiment_fields, experiment)
    libraries_validate(experiment, experiment.libraries)
    extra_libraries_validate(experiment.extra_libraries)

    if experiment.experiment_type is ExperimentType.model:
        if fld_units.name in experiment:
            raise LrgaspException(f"{desc} {experiment.experiment_type} must not specify {fld_units.name}")
    else:
        if fld_units.name not in experiment:
            raise LrgaspException(f"{desc} {experiment.experiment_type} must specify {fld_units.name}")

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
