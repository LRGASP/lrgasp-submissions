"""
Experiment metadata parsing and validation.
"""
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.defs import ExperimentType, Sample, ExpressionUnits, ResultFileType, validate_symbolic_ident
from lrgasp.metadata_validate import Field, check_from_defs, validate_url, validate_md5


fld_team_id = Field("team_id", validator=validate_symbolic_ident)
fld_experiment_id = Field("experiment_id", validator=validate_symbolic_ident)
fld_description = Field("description")
fld_challenge_id = Field("challenge_id", validator=validate_symbolic_ident)
fld_experiment_type = Field("experiment_type", ExperimentType)
fld_model_experiment_id = Field("model_experiment_id", optional=True, validator=validate_symbolic_ident)
fld_samples = Field("samples", list, element_dtype=Sample)
fld_data_files = Field("data_files", list, element_dtype=dict)
fld_result_files = Field("result_files", list, element_dtype=dict)
fld_software = Field("software", list, element_dtype=dict)
fld_notes = Field("notes", allow_empty=True, optional=True)

experiment_fields = (
    fld_team_id,
    fld_experiment_id,
    fld_description,
    fld_challenge_id,
    fld_experiment_type,
    fld_model_experiment_id,
    fld_samples,
    fld_data_files,
    fld_result_files,
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

fld_fname = Field("fname")
fld_ftype = Field("ftype", ResultFileType)
fld_md5 = Field("md5", validator=validate_md5)
fld_units = Field("units", ExpressionUnits, optional=True)

result_file_fields = (
    fld_fname,
    fld_ftype,
    fld_md5,
    fld_units,
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

def result_file_expression_validate(desc, experiment, result_file):
    if experiment.experiment_type == ExperimentType.model:
        raise LrgaspException(f"{desc} can not provides {result_file.ftype} files for {ExperimentType.model} experiments")
    if fld_units.name not in result_file:
        raise LrgaspException(f"{desc} {result_file.ftype} must specify {fld_units.name}")

def result_file_model_validate(desc, experiment, result_file):
    if experiment.experiment_type == ExperimentType.expression:
        raise LrgaspException(f"{desc} can not provides {result_file.ftype} files for {ExperimentType.expression} experiments")
    if fld_units.name in result_file:
        raise LrgaspException(f"{desc} {result_file.ftype} must not specify {fld_units.name}")

def result_file_validate(experiment, result_file):
    desc = "experiment.result_files"
    check_from_defs(desc, result_file_fields, result_file)
    if result_file.ftype is ResultFileType.expression_matrix:
        result_file_expression_validate(desc, experiment, result_file)
    else:
        result_file_model_validate(desc, experiment, result_file)

def experiment_validate(experiment):
    desc = "experiment"
    check_from_defs(desc, experiment_fields, experiment)
    if experiment.experiment_type is ExperimentType.expression:
        if fld_model_experiment_id.name not in experiment:
            raise LrgaspException(f"{desc} must specify experiment.{fld_model_experiment_id.name} for {experiment.experiment_type} experiments")
    else:
        if fld_model_experiment_id.name in experiment:
            raise LrgaspException(f"{desc} must not specify experiment.{fld_model_experiment_id.name} for {experiment.experiment_type} experiments")

    for data_file in experiment.data_files:
        data_file_validate(data_file)
    for result_file in experiment.result_files:
        result_file_validate(experiment, result_file)

def experiment_load(experiment_json):
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
