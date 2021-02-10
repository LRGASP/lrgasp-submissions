"""
Parsing and validation of metadata.
See metadata.md for all metadata
"""
import json
from email_validator import validate_email, EmailNotValidError
import validators.url
from lrgasp import LrgaspException
from lrgasp.objDict import ObjDict

fld_submitter_id = "submitter_id"
fld_group_name = "group_name"
fld_contacts = "contacts"
fld_group_url = "group_url"
fld_notes = "notes"
fld_name = "name"
fld_email = "email"
fld_submission_id = "submission_id"
fld_description = "description"
fld_challenge_id = "challenge_id"
fld_submission_type = "submission_type"
fld_model_submission_id = "model_submission_id"
fld_technologies = "technologies"
fld_protocol = "protocol"
fld_samples = "samples"
fld_files = "files"
fld_fname = "fname"
fld_ftype = "ftype"
fld_md5 = "md5"
fld_units = "units"
fld_software = "software"
fld_version = "version"
fld_url = "url"

def _check_required(desc, obj, required):
    for fld in required:
        if fld not in obj:
            raise LrgaspException(f"{desc} field {fld} is required")

def _names_values(obj, fields):
    for fld in fields:
        if fld in obj:
            yield fld, getattr(obj, fld)

def _check_non_empty_type(desc, obj, type, fields):
    "checks only fields that exist"
    for fld, val in _names_values(obj, fields):
        if (not isinstance(val, type)) or (len(val) == 0):
            raise LrgaspException(f"{desc} field {fld} must be a non-empty {type.__name__}")

def _check_type(desc, obj, type, fields):
    "checks only fields that exist"
    for fld, val in _names_values(obj, fields):
        if not isinstance(val, type):
            raise LrgaspException(f"{desc} field {fld} must be a {type.__name__}")

def submitter_contact_validate(contact):
    desc = "submitter.contacts"
    _check_required(desc, contact, (fld_name, fld_email,))
    _check_non_empty_type(desc, contact, str, (fld_name, fld_email,))
    _check_type(desc, contact, str, (fld_notes,))
    try:
        validate_email(contact.email, check_deliverability=False)
    except EmailNotValidError as ex:
        raise LrgaspException(f"{desc} field {fld_email} is valid email address: {contact.email}") from ex

def submitter_validate(submitter):
    desc = "submitter"
    _check_required(desc, submitter, (fld_submitter_id, fld_group_name, fld_contacts))
    _check_non_empty_type(desc, submitter, str, (fld_submitter_id, fld_group_name, fld_group_url))
    _check_type(desc, submitter, str, (fld_notes,))
    _check_non_empty_type(desc, submitter, list, (fld_contacts,))
    if (fld_group_url in submitter) and (validators.url(submitter.group_url) is not True):
        raise LrgaspException(f"{desc} field {fld_group_url} is not a valid URL: {submitter.group_url}")
    for contact in submitter.contacts:
        submitter_contact_validate(contact)

def submitter_load(submitter_json):
    """load and validate submitter object"""
    try:
        with open(submitter_json) as fh:
            submitter = json.load(fh, object_pairs_hook=ObjDict)
    except json.decoder.JSONDecodeError as ex:
        raise LrgaspException(f"parse of submitter metadata failed: {submitter_json}") from ex
    try:
        submitter_validate(submitter)
    except LrgaspException as ex:
        raise LrgaspException(f"validation of submitter metadata failed: {submitter_json}") from ex
    return submitter
