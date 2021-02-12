"""
Submission metadata parsing and validation.
"""
import json
from lrgasp import LrgaspException
from lrgasp.objDict import ObjDict
from lrgasp.types import SubmissionType, ExpressionUnits, ResultFileType, validate_symbolic_ident
from lrgasp.metadata_validate import Field, check_from_defs, validate_url, validate_md5


fld_submitter_id = Field("submitter_id")
fld_submission_id = Field("submission_id")
fld_description = Field("description")
fld_challenge_id = Field("challenge_id", validator=validate_symbolic_ident)
fld_submission_type = Field("submission_type", SubmissionType)
fld_model_submission_id = Field("model_submission_id", optional=True, validator=validate_symbolic_ident)
fld_data_files = Field("data_files", list)
fld_result_files = Field("result_files", list)
fld_software = Field("software", list)
fld_notes = Field("notes", allow_empty=True, optional=True)

submission_fields = (
    fld_submitter_id,
    fld_submission_id,
    fld_description,
    fld_challenge_id,
    fld_submission_type,
    fld_model_submission_id,
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

submission_software_fields = (
    fld_name,
    fld_version,
    fld_url,
    fld_config,
    fld_notes,
)

def data_file_validate(data_file):
    desc = "submission.data_files"
    check_from_defs(desc, data_file_fields, data_file)
    if (fld_acc.name not in data_file) and (fld_url not in data_file):
        raise LrgaspException(f"{desc} must specify at least one of {fld_acc.name} or {fld_url.name}")

def result_file_expression_validate(desc, submission, result_file):
    if submission.submission_type == SubmissionType.model:
        raise LrgaspException(f"{desc} can not provides {result_file.ftype} files for {SubmissionType.model} submissions")
    if fld_units.name not in result_file:
        raise LrgaspException(f"{desc} {result_file.ftype} must specify {fld_units.name}")

def result_file_model_validate(desc, submission, result_file):
    if submission.submission_type == SubmissionType.expression:
        raise LrgaspException(f"{desc} can not provides {result_file.ftype} files for {SubmissionType.expression} submissions")
    if fld_units.name in result_file:
        raise LrgaspException(f"{desc} {result_file.ftype} must not specify {fld_units.name}")

def result_file_validate(submission, result_file):
    desc = "submission.result_files"
    check_from_defs(desc, result_file_fields, result_file)
    if result_file.ftype is ResultFileType.expression_matrix:
        result_file_expression_validate(desc, submission, result_file)
    else:
        result_file_model_validate(desc, submission, result_file)

def submission_validate(submission):
    desc = "submission"
    check_from_defs(desc, submission_fields, submission)
    if submission.submission_type is SubmissionType.expression:
        if fld_model_submission_id.name not in fld_model_submission_id.name:
            raise LrgaspException(f"{desc} must specify submission.{fld_model_submission_id.name} for {submission.submission_type} submissions")
    else:
        if fld_model_submission_id.name in fld_model_submission_id.name:
            raise LrgaspException(f"{desc} must not specify submission.{fld_model_submission_id.name} for {submission.submission_type} submissions")

    for data_file in submission.data_files:
        data_file_validate(data_file)
    for result_file in submission.result_files:
        result_file_validate(submission, result_file)

def submission_load(submission_json):
    """load and validate submission metadata"""
    try:
        with open(submission_json) as fh:
            submission = json.load(fh, object_pairs_hook=ObjDict)
    except json.decoder.JSONDecodeError as ex:
        raise LrgaspException(f"parse of submission metadata failed: {submission_json}") from ex
    try:
        submission_validate(submission)
    except LrgaspException as ex:
        raise LrgaspException(f"validation of submission metadata failed: {submission_json}") from ex
    return submission
