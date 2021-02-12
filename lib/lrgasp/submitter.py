"""
Submitter metadata parsing and validation.
"""
import json
from lrgasp import LrgaspException
from lrgasp.objDict import ObjDict
from lrgasp.metadata_validate import Field, check_from_defs, validate_email, validate_http_url
from lrgasp.types import validate_symbolic_ident

##
# top-level submitter struct (from JSON)
##
fld_submitter_id = Field("submitter_id")
fld_group_name = Field("group_name")
fld_group_url = Field("group_url", optional=True, validator=validate_http_url)
fld_notes = Field("notes", allow_empty=True, optional=True)
fld_contacts = Field("contacts", list)

submitter_fields = (
    fld_submitter_id,
    fld_group_name,
    fld_group_url,
    fld_notes,
    fld_contacts
)

##
# contacts entries
##
fld_contact_name = Field("name", str)
fld_contact_email = Field("email", str, validator=validate_email)

submitter_contact_fields = (
    fld_contact_name,
    fld_contact_email,
    fld_notes
)

def submitter_contact_validate(contact):
    desc = "submitter.contacts"
    check_from_defs(desc, submitter_contact_fields, contact)

def submitter_validate(submitter):
    desc = "submitter"
    check_from_defs(desc, submitter_fields, submitter)
    try:
        validate_symbolic_ident(submitter.submitter_id)
    except LrgaspException as ex:
        raise LrgaspException(f"invalid {desc}.{fld_submitter_id.name}") from ex
    for contact in submitter.contacts:
        submitter_contact_validate(contact)

def submitter_load(submitter_json):
    """load and validate submitter metadata"""
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
