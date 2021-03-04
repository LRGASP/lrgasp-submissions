"""
Entry metadata parsing and validation.
"""
import os.path as osp
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.metadata_validate import Field, check_from_defs, validate_email
from lrgasp.defs import Challenge, validate_symbolic_ident, validate_synapse_ident, validate_entry_ident, ENTRY_JSON

##
# top-level entry struct (from JSON)
##
fld_entry_id = Field("entry_id", validator=validate_entry_ident)
fld_challenge_id = Field("challenge_id", Challenge)
fld_team_id = Field("team_id", validator=validate_synapse_ident)
fld_team_name = Field("team_name")
fld_experiment_ids = Field("experiment_ids", list, element_dtype=str, validator=validate_symbolic_ident)
fld_notes = Field("notes", allow_empty=True, optional=True)
fld_contacts = Field("contacts", list, element_dtype=dict)

entry_fields = (
    fld_entry_id,
    fld_challenge_id,
    fld_team_id,
    fld_team_name,
    fld_experiment_ids,
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
        raise LrgaspException(f"invalid {desc} {fld_entry_id.name}") from ex

    challenge_id = validate_entry_ident(entry.entry_id)
    if entry.challenge_id != challenge_id:
        raise LrgaspException(f"invalid {desc} {fld_entry_id.name} entry_id {entry.entry-id} prefix does not match challenge_id {entry.challenge_id}")
    for contact in entry.contacts:
        entry_contact_validate(contact)

def load(entry_json):
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

def load_dir(entry_dir):
    """load entry metadata, verifying that the file system directory matches
    the entry_id.  Save entry_dir in metadata """
    entry_json = osp.join(entry_dir, ENTRY_JSON)
    entry = load(entry_json)
    entry_base_dir = osp.basename(entry_dir)
    if entry_base_dir != entry.entry_id:
        raise LrgaspException(f"entry {entry.entry_id} must be in an directory {entry.entry_id}, not {entry_base_dir}")
    entry.entry_dir = entry_dir
    return entry
