"""
Entry metadata parsing and validation.
"""
import os.path as osp
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.metadata_validate import Field, check_from_defs, validate_email
from lrgasp.defs import Challenge, validate_symbolic_ident, validate_synapse_ident, validate_entry_ident, ENTRY_JSON

fld_notes = Field("notes", allow_empty=True, optional=True)


##
# top-level entry struct (from JSON)
##
entry_fields = (
    Field("entry_id", validator=validate_entry_ident),
    Field("challenge_id", Challenge),
    Field("team_id", validator=validate_synapse_ident),
    Field("team_name"),
    Field("experiment_ids", list, element_dtype=str, validator=validate_symbolic_ident),
    fld_notes,
    Field("contacts", list, element_dtype=dict)
)

##
# contacts fields
##

entry_contact_fields = (
    Field("name", str),
    Field("email", str, validator=validate_email),
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
        raise LrgaspException(f"invalid {desc} entry_id '{entry.entry_id}'") from ex

    challenge_id = validate_entry_ident(entry.entry_id)
    if entry.challenge_id != challenge_id:
        raise LrgaspException(f"invalid {desc} entry_id '{entry.entry-id}' prefix does not match challenge_id '{entry.challenge_id}'")
    for contact in entry.contacts:
        entry_contact_validate(contact)

def load(entry_json):
    """load and validate entry metadata"""
    try:
        with gopen(entry_json) as fh:
            entry = json.load(fh, object_pairs_hook=ObjDict)
    except (json.decoder.JSONDecodeError, UnicodeDecodeError) as ex:
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
    entry_base_dir = osp.basename(osp.realpath(entry_dir))
    if entry_base_dir != entry.entry_id:
        raise LrgaspException(f"entry '{entry.entry_id}' must be in an directory '{entry.entry_id}', not '{entry_base_dir}'")
    entry.entry_dir = entry_dir
    entry.entry_json = entry_json
    return entry
