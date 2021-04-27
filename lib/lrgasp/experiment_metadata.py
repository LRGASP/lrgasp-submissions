"""
Experiment metadata parsing and validation.
"""
import os.path as osp
import json
from collections import namedtuple, defaultdict
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.defs import Repository, Species, Challenge, DataCategory, Platform, validate_symbolic_ident, EXPERIMENT_JSON
from lrgasp.metadata_validate import Field, check_from_defs, validate_url
from lrgasp.data_sets import get_lrgasp_rna_seq_metadata

fld_experiment_id = Field("experiment_id", validator=validate_symbolic_ident)
fld_challenge_id = Field("challenge_id", Challenge)
fld_description = Field("description")
fld_species = Field("species", Species)
fld_data_category = Field("data_category", DataCategory)
fld_libraries = Field("libraries", list, element_dtype=str, validator=validate_symbolic_ident)
fld_extra_libraries = Field("extra_libraries", list, optional=True, allow_empty=True, element_dtype=dict)
fld_software = Field("software", list, element_dtype=dict)
fld_notes = Field("notes", allow_empty=True, optional=True)

experiment_fields = (
    fld_experiment_id,
    fld_challenge_id,
    fld_species,
    fld_description,
    fld_data_category,
    fld_libraries,
    fld_extra_libraries,
    fld_software,
    fld_notes,
)

fld_acc = Field("acc")
fld_repository = Field("repository", Repository)

extra_library_fields = (
    fld_acc,
    fld_repository,
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

valid_file_content = frozenset(["reads", "subreads", "nanopore_signal"])

class RunType(namedtuple("RunType",
                         ("sample", "library_prep", "platform"))):
    "attributes describing a run"

    def __str__(self):
        return str(self.sample) + '/' + str(self.library_prep) + '/' + str(self.platform)


def get_extra_libraries(experiment):
    """get the extra libraries field, or empty if not specified"""
    return experiment.get("extra_libraries", ())

def find_dups(lst):
    dups = []
    found = set()
    for v in lst:
        if (v in found) and (v not in dups):
            dups.append(v)
        found.add(v)
    return sorted(dups)

def _get_libraries_file_metadata(rna_seq_md, experiment):
    """collect metadata for all library files in experiment"""
    # exception if unknown acc
    return [rna_seq_md.get_file_by_acc(file_acc)
            for file_acc in experiment.libraries]

def library_validate(experiment, rna_seq_md, file_md):
    run_md = rna_seq_md.get_run_by_acc(file_md.run_acc)
    if run_md.species != experiment.species:
        raise LrgaspException(f"LRGASP RNA-Seq library '{run_md.run_acc}' file '{file_md.file_acc}' is for species '{run_md.species}' while experiment '{experiment.experiment_id}' specifies species as '{experiment.species}'")

    # this should never happen, as the data matrix should be restrict to types we allow
    if file_md.output_type not in valid_file_content:
        raise LrgaspException(f"File '{file_md.file_acc}' of output_type '{file_md.output_type}' not support for LRGASP, "
                              "valid types are {}; please contact LRGASP project if this type of file is needed".format(", ".join(sorted(valid_file_content))))

def _fmt_run_types(run_types):
    "make set of RunType objects pretty"
    if len(run_types) == 0:
        return "none"
    else:
        return ", ".join([str(rt) for rt in sorted(run_types)])

def get_file_run_type(rna_seq_md, expr_file_md):
    run_md = rna_seq_md.get_run_by_acc(expr_file_md.run_acc)
    return RunType(run_md.sample, run_md.library_prep, run_md.platform)

def get_run_types(rna_seq_md, expr_file_mds):
    "group into sets of long and short RunType,"
    long_run_types = set()
    short_run_types = set()
    for file_md in expr_file_mds:
        run_md = rna_seq_md.get_run_by_acc(file_md.run_acc)
        rt = RunType(run_md.sample, run_md.library_prep, run_md.platform)
        if rt.platform == Platform.Illumina:
            short_run_types.add(rt)
        else:
            long_run_types.add(rt)
    return long_run_types, short_run_types

def get_run_type_descs(rna_seq_md, expr_file_mds):
    "produce string descriptions of file acc to run types for error messages"
    rt_to_file_acc = defaultdict(set)
    for expr_file_md in expr_file_mds:
        rt = get_file_run_type(rna_seq_md, expr_file_md)
        rt_to_file_acc[rt].add(expr_file_md.file_acc)

    return ["{}: {}".format(str(rt), ", ".join(sorted(rt_to_file_acc[rt])))
            for rt in sorted(rt_to_file_acc.keys())]


def libraries_validate_compat(experiment, rna_seq_md, expr_file_mds):
    """compatibility between libraries and experiments;"""
    data_category = experiment.data_category
    long_run_types, short_run_types = get_run_types(rna_seq_md, expr_file_mds)

    def _run_type_err_msg(rts):
        return "found: " + _fmt_run_types(rts) + " in these specified library files:\n    " + "\n    ".join(get_run_type_descs(rna_seq_md, expr_file_mds))

    if data_category == DataCategory.short_only:
        if len(long_run_types) > 0:
            raise LrgaspException(f"{data_category} experiments must not use long-read platforms, " + _run_type_err_msg(long_run_types))
        if len(short_run_types) != 1:
            raise LrgaspException(f"{data_category} experiments must use one and only one short read library/platform, " + _run_type_err_msg(short_run_types))
    elif data_category == DataCategory.long_only:
        if len(long_run_types) != 1:
            raise LrgaspException(f"{data_category} experiments must use one and only one long-read library/platform, " + _run_type_err_msg(long_run_types))
        if len(short_run_types) != 0:
            raise LrgaspException(f"{data_category} experiments must not use short read platforms, " + _run_type_err_msg(short_run_types))
    elif data_category == DataCategory.long_short:
        if len(long_run_types) != 1:
            raise LrgaspException(f"{data_category} experiments must use one and only one long-read library/platform, " + _run_type_err_msg(long_run_types))
        if len(short_run_types) != 1:
            raise LrgaspException(f"{data_category} experiments must use one and only one short read library/platform, " + _run_type_err_msg(short_run_types))
    elif data_category == DataCategory.kitchen_sink:
        if len(experiment.libraries) == 0:
            raise LrgaspException(f"{data_category} experiments must use some LRGASP RNA-Seq libraries")
    else:
        raise LrgaspException("bug")

def libraries_validate_paired_end(rna_seq_md, expr_file_mds):
    "make sure both paired ends are there"
    paired_expr_file_mds = [fm for fm in expr_file_mds if fm.paired_end is not None]
    paired_acc = frozenset([fm.file_acc for fm in paired_expr_file_mds])
    for file_md in paired_expr_file_mds:
        if file_md.paired_with not in paired_acc:
            raise LrgaspException(f"'{file_md.file_acc}' is a paired-end experiment, however the paired file '{file_md.paired_with}' is not specified in experiment.libraries")

def libraries_validate(experiment):
    rna_seq_md = get_lrgasp_rna_seq_metadata()
    dups = find_dups(experiment.libraries)
    if len(dups) > 0:
        raise LrgaspException(f"duplicate accession in libraries: {dups}")

    # per library validation
    expr_file_mds = _get_libraries_file_metadata(rna_seq_md, experiment)
    for file_md in expr_file_mds:
        library_validate(experiment, rna_seq_md, file_md)

    # cross-library validations
    libraries_validate_compat(experiment, rna_seq_md, expr_file_mds)
    libraries_validate_paired_end(rna_seq_md, expr_file_mds)

def extra_library_validate(extra_library):
    desc = "experiment.extra_libraries"
    check_from_defs(desc, extra_library_fields, extra_library)

def extra_libraries_validate(experiment):
    if experiment.data_category != DataCategory.kitchen_sink:
        raise LrgaspException("experiment extra_libraries may only be specified for kitchen_sink experiments")
    dups = find_dups([el.acc for el in experiment.extra_libraries])
    if len(dups) > 0:
        raise LrgaspException(f"duplicate accession in extra libraries: {dups}")
    for extra_library in experiment.extra_libraries:
        extra_library_validate(extra_library)

def experiment_validate(experiment):
    desc = "experiment"
    check_from_defs(desc, experiment_fields, experiment)
    libraries_validate(experiment)
    if len(get_extra_libraries(experiment)) > 0:
        extra_libraries_validate(experiment)

def load(experiment_json):
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

def load_from_entry(entry, experiment_id):
    """load and validation experiment metadata given a entry,
    add experiment_dir to metadata"""
    experiment_dir = osp.join(entry.entry_dir, experiment_id)
    experiment_json = osp.join(experiment_dir, EXPERIMENT_JSON)
    try:
        experiment = load(experiment_json)
    except (LrgaspException, FileNotFoundError, ValueError) as ex:
        raise LrgaspException(f"error parse metadata for entry '{entry.entry_id}', experiment '{experiment_id}': {experiment_json}") from ex
    experiment.experiment_dir = experiment_dir
    experiment.experiment_json = experiment_json
    return experiment
