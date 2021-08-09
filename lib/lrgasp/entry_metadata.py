"""
Entry metadata parsing and validation.
"""
import os.path as osp
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.metadata_validate import Field, check_from_defs, validate_email
from lrgasp import experiment_metadata
from lrgasp.defs import Challenge, validate_symbolic_ident, validate_synapse_ident, validate_entry_ident, ENTRY_JSON

# Note: a field "experiments" is added when metadata is loaded.  It is None
# until experiment metadata is loaded.

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

def entry_id_validate(challenge_id, entry_id):
    "entry id must be prefixed by the challenge_id"
    expect_pre = str(challenge_id) + '_'
    if (not entry_id.startswith(expect_pre)) or (len(entry_id) == len(expect_pre)):
        raise LrgaspException(f"entry id '{entry_id}' must be prefixed with challenge_id ({challenge_id}) + '_' + a participant-defined name")

def entry_contact_validate(contact):
    desc = "entry.contacts"
    check_from_defs(desc, entry_contact_fields, contact)

def entry_validate(entry_md):
    desc = "entry"
    check_from_defs(desc, entry_fields, entry_md)
    entry_id_validate(entry_md.challenge_id, entry_md.entry_id)

    challenge_id = validate_entry_ident(entry_md.entry_id)
    if entry_md.challenge_id != challenge_id:
        raise LrgaspException(f"invalid {desc} entry_id '{entry_md.entry_id}' prefix does not match challenge_id '{entry_md.challenge_id}'")
    for contact in entry_md.contacts:
        entry_contact_validate(contact)

def load(entry_json):
    """load and validate entry metadata"""
    try:
        with gopen(entry_json) as fh:
            entry_md = json.load(fh, object_pairs_hook=ObjDict)
    except (json.decoder.JSONDecodeError, UnicodeDecodeError) as ex:
        raise LrgaspException(f"parse of entry metadata (JSON) failed: {entry_json}") from ex
    try:
        entry_validate(entry_md)
    except LrgaspException as ex:
        raise LrgaspException(f"validation of entry metadata failed: {entry_json}") from ex
    entry_md.experiments = None
    return entry_md

def parser_entry_dirname(entry_dir):
    try:
        entry_base_dir = osp.basename(osp.normpath(entry_dir))
        validate_entry_ident(entry_base_dir)
        return entry_base_dir
    except LrgaspException as ex:
        raise LrgaspException(f"entry directory is not a valid entry id: '{entry_dir}'") from ex

def load_dir(entry_dir):
    """load entry metadata, verifying that the file system directory matches
    the entry_id.  Save entry_dir in metadata """
    entry_base_dir = parser_entry_dirname(entry_dir)
    entry_json = osp.join(entry_dir, ENTRY_JSON)
    entry_md = load(entry_json)
    if entry_base_dir != entry_md.entry_id:
        raise LrgaspException(f"entry_id and directory name must be the same; '{entry_md.entry_id}' is in '{entry_base_dir}' ({entry_dir})")
    entry_md.entry_dir = osp.normpath(entry_dir)
    entry_md.entry_json = entry_json
    return entry_md

def load_experiments_metadata(entry_md):
    """read experiment metadata and save in entry_md.experiments, no-op if already loaded.
    Can be restricted for testing"""
    if entry_md.experiments is None:
        entry_md.experiments = [experiment_metadata.load_from_entry(entry_md, experiment_id)
                                for experiment_id in entry_md.experiment_ids]
