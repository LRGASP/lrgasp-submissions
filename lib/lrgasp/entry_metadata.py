"""
Entry metadata parsing and validation.
"""
import os.path as osp
import json
from lrgasp import LrgaspException, gopen, iter_to_str
from lrgasp.objDict import ObjDict
from lrgasp.metadata_validate import Field, check_from_defs, validate_email
from lrgasp import experiment_metadata
from lrgasp.defs import (Challenge, DataCategory, Sample, LibraryPrep, Platform,
                         validate_symbolic_ident, validate_synapse_ident, validate_entry_ident,
                         challenge_desc, get_challenge_samples, get_data_category_platforms,
                         ENTRY_JSON)
from lrgasp.data_sets import get_lrgasp_rna_seq_metadata

# Note:
#  - field "experiments" is added when metadata is loaded.  It is None until
#     experiment metadata is loaded.

fld_notes = Field("notes", allow_empty=True, optional=True)

##
# top-level entry struct (from JSON)
##
entry_fields = (
    Field("entry_id", validator=validate_entry_ident),
    Field("challenge_id", Challenge),
    Field("team_id", validator=validate_synapse_ident),
    Field("team_name"),
    Field("data_category", DataCategory),
    Field("samples", list, element_dtype=Sample),
    Field("library_preps", list, element_dtype=LibraryPrep),
    Field("platforms", list, element_dtype=Platform),
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
    check_from_defs("entry.contacts", entry_contact_fields, contact)

def validate_entry_experiment_compat(entry_md, experiment_md):
    if experiment_md.challenge_id != entry_md.challenge_id:
        raise LrgaspException(f"experiment '{experiment_md.experiment_id}' challenge_id '{experiment_md.challenge_id}' does not match"
                              f"entry '{entry_md.entry_id}' challenge_id '{entry_md.challenge_id}'")
    if experiment_md.data_category != entry_md.data_category:
        raise LrgaspException(f"experiment '{experiment_md.experiment_id}' data_category '{experiment_md.data_category}' does not match"
                              f"entry '{entry_md.entry_id}' data_category '{entry_md.data_category}'")

def entry_experiments_validate_combined_attrs(entry_md):
    """check samples, library_preps, and platforms to see if they cover all experiments"""
    def _match_err(fld_name, fld_value, expect_value):
        raise LrgaspException(f"entry '{entry_md.entry_id} field '{fld_name}' must be the '{fld_name}' values from all experiments,"
                              f" found '{iter_to_str(fld_value)}', expected '{iter_to_str(expect_value)}'")

    expr_samples = set([p for ex in entry_md.experiments for p in ex.samples])
    if expr_samples != set(entry_md.samples):
        _match_err("samples", entry_md.samples, expr_samples)
    expr_library_preps = set([p for ex in entry_md.experiments for p in ex.library_preps])
    if expr_library_preps != set(entry_md.library_preps):
        _match_err("library_preps", entry_md.library_preps, expr_library_preps)
    expr_platforms = set([p for ex in entry_md.experiments for p in ex.platforms])
    if expr_platforms != set(entry_md.platforms):
        _match_err("platforms", entry_md.platforms, expr_platforms)

def get_entry_samples(entry_md):
    rna_seq_md = get_lrgasp_rna_seq_metadata()
    samples = set()
    for ex in entry_md.experiments:
        for file_acc in ex.libraries:
            samples.add(rna_seq_md.get_run_by_file_acc(file_acc).sample)
    return samples

def get_entry_category_samples(entry_md):
    rna_seq_md = get_lrgasp_rna_seq_metadata()
    valid_platforms = get_data_category_platforms(entry_md.data_category)
    samples = set()
    for library_prep in entry_md.library_preps:
        for platform in entry_md.platforms:
            for run_md in rna_seq_md.get_runs_by_prep_platform(library_prep, platform):
                if run_md.platform in valid_platforms:
                    samples.add(run_md.sample)
    return samples

def validate_challenge_samples(entry_md):
    """validate that all samples for entry category challenge are covered;
    non-freestyle only (requires all experiments loaded)"""
    entry_samples = set(entry_md.samples)
    entry_category_samples = get_entry_category_samples(entry_md)
    challenge_samples = get_challenge_samples(entry_md.challenge_id)
    required_samples = entry_category_samples & challenge_samples
    if entry_samples != required_samples:
        raise LrgaspException(f"entry must use all of the available samples for {challenge_desc(entry_md.challenge_id)},"
                              f" need '{iter_to_str(challenge_samples)}', only '{iter_to_str(entry_samples)}' were found")

def entry_experiments_validate(entry_md):
    for experiment_md in entry_md.experiments:
        validate_entry_experiment_compat(entry_md, experiment_md)
    entry_experiments_validate_combined_attrs(entry_md)
    if entry_md.data_category != DataCategory.freestyle:
        validate_challenge_samples(entry_md)

def entry_validate(entry_md):
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
        check_from_defs("entry", entry_fields, entry_md)
        # add non-serialized fields after field check
        entry_md.experiments = None
        entry_md.entry_dir = None
        entry_md.entry_json = entry_json
        entry_validate(entry_md)
    except LrgaspException as ex:
        raise LrgaspException(f"validation of entry metadata failed: {entry_json}") from ex

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
    entry_md.entry_dir = osp.normpath(entry_dir)
    if entry_base_dir != entry_md.entry_id:
        raise LrgaspException(f"entry_id and directory name must be the same; '{entry_md.entry_id}' is in '{entry_base_dir}' ({entry_dir})")
    return entry_md

def load_experiments_metadata(entry_md):
    """Read experiment metadata and save in entry_md.experiments, no-op if already loaded.
    Validate consistency of entry and experiments metadata"""
    if entry_md.experiments is None:
        entry_md.experiments = [experiment_metadata.load_from_entry(entry_md, experiment_id)
                                for experiment_id in entry_md.experiment_ids]
        entry_experiments_validate(entry_md)
