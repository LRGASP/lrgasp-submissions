"""
Entry metadata parsing and validation.
"""
import os.path as osp
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.metadata_validate import Field, check_from_defs, validate_email, field_omitted_or_none
from lrgasp import experiment_metadata
from lrgasp.defs import (Challenge, DataCategory, LibraryPrep, Platform, EntryCategory,
                         validate_symbolic_ident, validate_synapse_ident, validate_entry_ident,
                         ENTRY_JSON)

# Note:
#  - a field entry_category is added from data_category, library_prep, and platform
#  - field "experiments" is added when metadata is loaded.  It is None until
#     experiment metadata is loaded.

fld_notes = Field("notes", allow_empty=True, optional=True)

entry_catagory_non_freestyle_fields = ("library_prep", "platform")

##
# top-level entry struct (from JSON)
##
entry_fields = (
    Field("entry_id", validator=validate_entry_ident),
    Field("challenge_id", Challenge),
    Field("team_id", validator=validate_synapse_ident),
    Field("team_name"),
    Field("data_category", DataCategory),
    Field("library_prep", LibraryPrep, optional=True),
    Field("platform", Platform, optional=True),
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

def check_entry_category_fields(entry_md):
    "library_prep and method required for other than freestyle"
    if entry_md.data_category == DataCategory.freestyle:
        for fld in entry_catagory_non_freestyle_fields:
            if not field_omitted_or_none(entry_md, fld):
                raise LrgaspException(f"data_category {entry_md.data_category} can not specify field {fld}")
    else:
        for fld in entry_catagory_non_freestyle_fields:
            if field_omitted_or_none(entry_md, fld):
                raise LrgaspException(f"data_category {entry_md.data_category} must specify field {fld}")

# these are require on other than freestyle, and must be omitted on freestyle
entry_catagory_non_freestyle_fields = ("library_prep", "platform")

def entry_id_validate(challenge_id, entry_id):
    "entry id must be prefixed by the challenge_id"
    expect_pre = str(challenge_id) + '_'
    if (not entry_id.startswith(expect_pre)) or (len(entry_id) == len(expect_pre)):
        raise LrgaspException(f"entry id '{entry_id}' must be prefixed with challenge_id ({challenge_id}) + '_' + a participant-defined name")

def entry_contact_validate(contact):
    check_from_defs("entry.contacts", entry_contact_fields, contact)

def entry_validate(entry_md):
    check_from_defs("entry", entry_fields, entry_md)
    check_entry_category_fields(entry_md)
    entry_id_validate(entry_md.challenge_id, entry_md.entry_id)

    challenge_id = validate_entry_ident(entry_md.entry_id)
    if entry_md.challenge_id != challenge_id:
        raise LrgaspException(f"invalid entry_id '{entry_md.entry_id}' prefix does not match challenge_id '{entry_md.challenge_id}'")
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

    # special handle for freestyle
    if entry_md.data_category == DataCategory.freestyle:
        entry_md.library_prep = None
        entry_md.platform = None

    # non-serialized fields
    entry_md.experiments = None
    entry_md.entry_category = EntryCategory(entry_md.data_category,
                                            entry_md.library_prep,
                                            entry_md.platform)
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
