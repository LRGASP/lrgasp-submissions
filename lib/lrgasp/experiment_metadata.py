"""
Experiment metadata parsing and validation.
"""
import os.path as osp
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.defs import ExperimentType, Sample, ExpressionUnits, validate_symbolic_ident, EXPERIMENT_JSON
from lrgasp.metadata_validate import Field, check_from_defs, validate_url

fld_experiment_id = Field("experiment_id", validator=validate_symbolic_ident)
fld_experiment_type = Field("experiment_type", ExperimentType)
fld_description = Field("description")
fld_samples = Field("samples", list, element_dtype=Sample)
fld_data_files = Field("data_files", list, element_dtype=dict)
fld_units = Field("units", ExpressionUnits, optional=True)
fld_software = Field("software", list, element_dtype=dict)
fld_notes = Field("notes", allow_empty=True, optional=True)

experiment_fields = (
    fld_experiment_id,
    fld_experiment_type,
    fld_description,
    fld_samples,
    fld_data_files,
    fld_units,
    fld_software,
    fld_notes,
)

fld_acc = Field("acc", optional=True)
fld_url = Field("url", optional=True, validator=validate_url)

data_file_fields = (
    fld_acc,
    fld_url,
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

def data_file_validate(data_file):
    desc = "experiment.data_files"
    check_from_defs(desc, data_file_fields, data_file)
    if (fld_acc.name not in data_file) and (fld_url not in data_file):
        raise LrgaspException(f"{desc} must specify at least one of {fld_acc.name} or {fld_url.name}")

def experiment_validate(experiment):
    desc = "experiment"
    check_from_defs(desc, experiment_fields, experiment)

    for data_file in experiment.data_files:
        data_file_validate(data_file)

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
