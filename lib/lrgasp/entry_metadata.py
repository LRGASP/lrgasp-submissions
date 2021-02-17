"""
Entry metadata parsing and validation.
"""
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.metadata_validate import Field, check_from_defs, validate_email
from lrgasp.types import Challenge, validate_symbolic_ident, validate_synapse_ident

##
# top-level entry struct (from JSON)
##
fld_entry_id = Field("entry_id", validator=validate_symbolic_ident)
fld_challenge_id = Field("challenge_id", Challenge)
fld_team_id = Field("team_id", validator=validate_synapse_ident)
fld_team_name = Field("team_name")
fld_notes = Field("notes", allow_empty=True, optional=True)
fld_contacts = Field("contacts", list)

entry_fields = (
    fld_entry_id,
    fld_challenge_id,
    fld_team_id,
    fld_team_name,
    fld_notes,
    fld_contacts
)

##
# contacts entries
##
fld_contact_name = Field("name", str)
fld_contact_email = Field("email", str, validator=validate_email)

entry_contact_fields = (
    fld_contact_name,
    fld_contact_email,
    fld_notes
)

def entry_contact_validate(contact):
    desc = "entry.contacts"
    check_from_defs(desc, entry_contact_fields, contact)

def entry_validate(entry):
    desc = "entry"
    check_from_defs(desc, entry_fields, entry)
    try:
        validate_symbolic_ident(entry.entry_id)
    except LrgaspException as ex:
        raise LrgaspException(f"invalid {desc}.{fld_entry_id.name}") from ex
    for contact in entry.contacts:
        entry_contact_validate(contact)

def entry_load(entry_json):
    """load and validate entry metadata"""
    try:
        with gopen(entry_json) as fh:
            entry = json.load(fh, object_pairs_hook=ObjDict)
    except json.decoder.JSONDecodeError as ex:
        raise LrgaspException(f"parse of entry metadata (JSON) failed: {entry_json}") from ex
    try:
        entry_validate(entry)
    except LrgaspException as ex:
        raise LrgaspException(f"validation of entry metadata failed: {entry_json}") from ex
    return entry
