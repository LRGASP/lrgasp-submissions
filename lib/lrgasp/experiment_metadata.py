"""
Experiment metadata parsing and validation.
"""
import os.path as osp
import json
from collections import defaultdict
from lrgasp import LrgaspException, gopen, iter_to_str
from lrgasp.objDict import ObjDict
from lrgasp.defs import Repository, Species, Challenge, DataCategory, Sample, LibraryPrep, Platform, EXPERIMENT_JSON
from lrgasp.defs import validate_symbolic_ident, is_simulation, challenge_desc, get_challenge_samples
from lrgasp.defs import MODELS_GTF, READ_MODEL_MAP_TSV, DE_NOVO_RNA_FASTA, EXPRESSION_TSV
from lrgasp.metadata_validate import Field, check_from_defs, validate_url
from lrgasp.data_sets import get_lrgasp_rna_seq_metadata, get_run_type

fld_notes = Field("notes", allow_empty=True, optional=True)

experiment_fields = (
    Field("experiment_id", validator=validate_symbolic_ident),
    Field("challenge_id", Challenge),
    Field("description"),
    Field("species", Species),
    Field("data_category", DataCategory),
    Field("samples", list, element_dtype=Sample),
    Field("library_preps", list, element_dtype=LibraryPrep),
    Field("platforms", list, element_dtype=Platform),
    Field("libraries", list, element_dtype=str, validator=validate_symbolic_ident),
    Field("extra_libraries", list, optional=True, allow_empty=True, element_dtype=dict),
    Field("software", list, element_dtype=dict),
    fld_notes,
)

extra_libraries_fields = (
    Field("acc"),
    Field("repository", Repository),
    fld_notes,
)

experiment_software_fields = (
    Field("name"),
    Field("version"),
    Field("description", optional=True),
    Field("url", validator=validate_url),
    Field("config"),
    fld_notes,
)

valid_file_content = frozenset(["reads", "subreads", "nanopore_signal"])

def get_extra_libraries(experiment_md):
    """get the extra_libraries field, or empty if not specified"""
    return experiment_md.get("extra_libraries", ())

def find_dups(lst):
    dups = []
    found = set()
    for v in lst:
        if (v in found) and (v not in dups):
            dups.append(v)
        found.add(v)
    return sorted(dups)

def get_libraries_file_metadata(rna_seq_md, experiment_md):
    """collect metadata for all library files in experiment"""
    # exception if unknown acc
    return [rna_seq_md.get_file_by_acc(file_acc)
            for file_acc in experiment_md.libraries]

def library_validate(experiment_md, rna_seq_md, file_md):
    run_md = rna_seq_md.get_run_by_acc(file_md.run_acc)
    if run_md.species != experiment_md.species:
        raise LrgaspException(f"LRGASP RNA-Seq library '{run_md.run_acc}' file '{file_md.file_acc}' is for species '{run_md.species}' while experiment '{experiment_md.experiment_id}' specifies species as '{experiment_md.species}'")

    # this should never happen, as the data matrix should be restrict to types we allow
    if file_md.output_type not in valid_file_content:
        raise LrgaspException(f"File '{file_md.file_acc}' of output_type '{file_md.output_type}' not support for LRGASP, "
                              "valid types are {}; please contact LRGASP project if this type of file is needed".format(", ".join(sorted(valid_file_content))))

def get_file_run_type(rna_seq_md, file_md):
    return get_run_type(rna_seq_md.get_run_by_acc(file_md.run_acc))

def get_run_types(rna_seq_md, file_mds):
    "group into sets of long and short RunType,"
    long_run_types = set()
    short_run_types = set()
    for file_md in file_mds:
        rt = get_file_run_type(rna_seq_md, file_md)
        if rt.platform == Platform.Illumina:
            short_run_types.add(rt)
        else:
            long_run_types.add(rt)
    return long_run_types, short_run_types

def get_run_type_descs(rna_seq_md, file_mds):
    "produce list of string descriptions of file acc to run types for error messages"

    def _mk_desc(file_md, done):
        done.add(file_md.file_acc)
        if file_md.paired_with is None:
            acc_desc = file_md.file_acc
        else:
            acc_desc = file_md.file_acc + ", " + file_md.paired_with
            done.add(file_md.paired_with)
        rt = get_file_run_type(rna_seq_md, file_md)
        return f"{acc_desc}: {rt}"

    descs = []
    done = set()  # to avoid duplicating due to paired_with
    for file_md in file_mds:
        if file_md.file_acc not in done:
            descs.append(_mk_desc(file_md, done))
    return descs

def _validate_sample_compat(rna_seq_md, experiment_md, run_type):
    valid_samples = get_challenge_samples(experiment_md.challenge_id)
    if run_type.sample not in valid_samples:
        raise LrgaspException(f"sample '{run_type.sample}' is not valid for challenge '{experiment_md.challenge_id}',"
                              " expected one of {}".format(iter_to_str(valid_samples)))

def _validate_samples_compat(rna_seq_md, experiment_md, run_types):
    """check if samples uses are compatible with challenge"""
    for run_type in run_types:
        _validate_sample_compat(rna_seq_md, experiment_md, run_type)

def _validate_data_category_compat(rna_seq_md, experiment_md, long_run_types, short_run_types, file_mds):  # noqa: C901
    """compatibility between data category and libraries in an experiments;"""
    data_category = experiment_md.data_category

    def _run_type_err_msg():
        return ("from specified library files:\n    " +
                "\n    ". join(get_run_type_descs(rna_seq_md, file_mds)))

    def _validate_short_only():
        if len(long_run_types) > 0:
            raise LrgaspException(f"{data_category} experiments must not use long-read platforms, found {len(long_run_types)}, " + _run_type_err_msg())
        if len(short_run_types) != 1:
            raise LrgaspException(f"{data_category} experiments must use one and only one short-read library/platform, found {len(short_run_types)}, " + _run_type_err_msg())

    def _validate_long_only():
        if len(long_run_types) != 1:
            raise LrgaspException(f"{data_category} experiments must use one and only one long-read library/platform, found {len(long_run_types)}, " + _run_type_err_msg())
        if len(short_run_types) != 0:
            raise LrgaspException(f"{data_category} experiments must not use short-read platforms, " + _run_type_err_msg())

    def _validate_long_short():
        if len(long_run_types) != 1:
            raise LrgaspException(f"{data_category} experiments must use one and only one long-read library/platform, found {len(long_run_types)}, " + _run_type_err_msg())
        if len(short_run_types) != 1:
            raise LrgaspException(f"{data_category} experiments must use one and only one short-read library/platform, found {len(short_run_types)}, " + _run_type_err_msg())
        if list(short_run_types)[0].sample != list(long_run_types)[0].sample:
            raise LrgaspException(f"{data_category} experiments must use the same sample for long and short libraries, got " +
                                  _run_type_err_msg())

    def _validate_long_genome():
        if experiment_md.challenge_id != Challenge.iso_detect_de_novo:
            raise LrgaspException(f"{data_category} only allowed for {challenge_desc(Challenge.iso_detect_de_novo)}")
        _validate_long_only()

    def _validate_freestyle():
        if len(experiment_md.libraries) == 0:
            raise LrgaspException(f"{data_category} experiments must use some LRGASP RNA-Seq libraries")
        # simulation not allowed
        for file_md in file_mds:
            if is_simulation(rna_seq_md.get_run_by_file_acc(file_md.file_acc).sample):
                raise LrgaspException(f"{data_category} experiments may not use simulation data '{file_md.file_acc}'")

    if data_category == DataCategory.short_only:
        _validate_short_only()
    elif data_category == DataCategory.long_only:
        _validate_long_only()
    elif data_category == DataCategory.long_short:
        _validate_long_short()
    elif data_category == DataCategory.long_genome:
        _validate_long_genome()
    elif data_category == DataCategory.freestyle:
        _validate_freestyle()
    else:
        raise LrgaspException("bug")

def _validate_library_category_compat(rna_seq_md, experiment_md, file_mds, run_types):
    def _match_err(fld_name, fld_value, expect_value):
        raise LrgaspException(f"experiment '{experiment_md.experiment_id}' field '{fld_name}', '{iter_to_str(fld_value)}', must match"
                              f" '{fld_name}' for all library files, got '{iter_to_str(expect_value)}', "
                              "from specified library files:\n    " +
                              "\n    ". join(get_run_type_descs(rna_seq_md, file_mds)))

    run_samples = set([rt.sample for rt in run_types])
    if set(run_samples) != set(experiment_md.samples):
        _match_err("samples", experiment_md.samples, run_samples)
    run_library_preps = set([rt.library_prep for rt in run_types])
    if set(run_library_preps) != set(experiment_md.library_preps):
        _match_err("library_preps", experiment_md.library_preps, run_library_preps)
    run_platforms = set([rt.platform for rt in run_types])
    if run_platforms != set(experiment_md.platforms):
        _match_err("platform", experiment_md.platforms, run_platforms)


def _validate_library_compat(rna_seq_md, experiment_md, file_mds):
    """compatibility between challenge, data category and libraries in an experiments;"""
    long_run_types, short_run_types = get_run_types(rna_seq_md, file_mds)
    run_types = long_run_types | short_run_types
    _validate_samples_compat(rna_seq_md, experiment_md, run_types)
    _validate_data_category_compat(rna_seq_md, experiment_md, long_run_types, short_run_types, file_mds)
    _validate_library_category_compat(rna_seq_md, experiment_md, file_mds, run_types)

def _validate_paired_end(rna_seq_md, file_mds):
    "make sure both paired ends are there"
    paired_file_mds = [fm for fm in file_mds if fm.paired_end is not None]
    paired_acc = frozenset([fm.file_acc for fm in paired_file_mds])
    for file_md in paired_file_mds:
        if file_md.paired_with not in paired_acc:
            raise LrgaspException(f"'{file_md.file_acc}' is a paired-end experiment, however the paired file '{file_md.paired_with}' is not specified in experiment_md.libraries")

def get_runs_replicates(rna_seq_md, file_mds):
    "get dict of runs to set of replicates for all libraries"
    runs_replicates = defaultdict(set)
    for file_md in file_mds:
        runs_replicates[file_md.run_acc].add(file_md.biological_replicate_number)
    runs_replicates.default_factory = None
    return runs_replicates

def _validate_replicates(rna_seq_md, experiment_md, file_mds):
    """validate that all replicates are used in an experiment"""
    runs_replicates = get_runs_replicates(rna_seq_md, file_mds)

    def _get_run_file_desc(run_md):
        """generate list of possible files"""
        rep_file_descs = []
        for rep in run_md.replicates:
            for f in rep.files:
                rep_file_descs.append(f"{f.run_acc} {f.file_acc} {f.biological_replicate_number} {f.file_type}")
        return rep_file_descs

    def _check_run(run_acc, rep_set):
        run_md = rna_seq_md.get_run_by_acc(run_acc)
        if len(rep_set) != len(run_md.replicates):
            raise LrgaspException(f"experiment must use all replicates from run {run_acc}, available replicate files:\n    "
                                  + "\n    ".join(_get_run_file_desc(run_md)))

    for run_acc, rep_set in runs_replicates.items():
        _check_run(run_acc, rep_set)

def _validate_libraries(experiment_md):
    rna_seq_md = get_lrgasp_rna_seq_metadata()
    dups = find_dups(experiment_md.libraries)
    if len(dups) > 0:
        raise LrgaspException(f"duplicate accession in libraries: {dups}")

    # per library validation
    file_mds = get_libraries_file_metadata(rna_seq_md, experiment_md)
    for file_md in file_mds:
        library_validate(experiment_md, rna_seq_md, file_md)

    # cross-library file validations
    _validate_paired_end(rna_seq_md, file_mds)
    _validate_library_compat(rna_seq_md, experiment_md, file_mds)
    _validate_replicates(rna_seq_md, experiment_md, file_mds)

def _validate_extra_libraries(experiment_md):
    if experiment_md.data_category not in (DataCategory.long_short, DataCategory.freestyle):
        raise LrgaspException("experiment extra_libraries may only be specified for 'long_short' or 'freestyle' experiments")
    dups = find_dups([el.acc for el in experiment_md.extra_libraries])
    if len(dups) > 0:
        raise LrgaspException(f"duplicate accession in extra libraries: {dups}")
    for ilib in range(len(experiment_md.extra_libraries)):
        check_from_defs(f"experiment_md.extra_libraries[{ilib}]",
                        extra_libraries_fields, experiment_md.extra_libraries[ilib])

def _validate_software(experiment_md):
    for isoft in range(len(experiment_md.software)):
        check_from_defs(f"experiment_md.software[{isoft}]",
                        experiment_software_fields, experiment_md.software[isoft])

def experiment_validate(experiment_md):
    _validate_libraries(experiment_md)
    if len(get_extra_libraries(experiment_md)) > 0:
        _validate_extra_libraries(experiment_md)
    _validate_software(experiment_md)

def load(experiment_json):
    """load and validate experiment metadata"""
    try:
        with gopen(experiment_json) as fh:
            experiment_md = json.load(fh, object_pairs_hook=ObjDict)
    except json.decoder.JSONDecodeError as ex:
        raise LrgaspException(f"parse of experiment metadata (JSON) failed: {experiment_json}") from ex
    try:
        check_from_defs("experiment", experiment_fields, experiment_md)
        # add non-serialized fields after field check
        experiment_md.experiment_dir = None
        experiment_md.experiment_json = experiment_json
        experiment_validate(experiment_md)
    except LrgaspException as ex:
        raise LrgaspException(f"validation of experiment metadata failed: {experiment_json}") from ex

    return experiment_md

def load_from_entry(entry_md, experiment_id):
    """load and validation experiment metadata given a entry,
    add experiment_dir to metadata"""
    experiment_dir = osp.join(entry_md.entry_dir, experiment_id)
    experiment_json = osp.join(experiment_dir, EXPERIMENT_JSON)
    try:
        experiment_md = load(experiment_json)
        # add non-serialized fields after field check
        experiment_md.experiment_dir = osp.normpath(experiment_dir)
    except (LrgaspException, FileNotFoundError, ValueError) as ex:
        raise LrgaspException(f"error parse metadata for entry '{entry_md.entry_id}', experiment '{experiment_id}' (obtained from entry.json): {experiment_json}") from ex

    if experiment_md.experiment_id != osp.basename(experiment_dir):
        raise LrgaspException(f"experiment_id and directory name must be the same; '{experiment_md.experiment_id}' is in '{osp.basename(experiment_dir)}' ({experiment_dir})")

    return experiment_md

def get_models_gtf(experiment_md):
    """get path to models.gtf file or None if not valid for this experiment.
    Will not include .gz extension or check for existence."""
    if experiment_md.challenge_id in (Challenge.iso_detect_ref, Challenge.iso_quant):
        return osp.join(experiment_md.experiment_dir, MODELS_GTF)
    else:
        return None

def get_read_model_map_tsv(experiment_md):
    """get path to read_model_map.gtf file or None if not valid for this
    experiment. Will not include .gz extension or check for existence."""
    if experiment_md.challenge_id in (Challenge.iso_detect_ref, Challenge.iso_detect_de_novo):
        return osp.join(experiment_md.experiment_dir, READ_MODEL_MAP_TSV)
    else:
        return None

def get_rna_fasta(experiment_md):
    """get path to RNA fasta file or None if not valid for this
    experiment. Will not include .gz extension or check for existence."""
    if experiment_md.challenge_id is Challenge.iso_detect_de_novo:
        return osp.join(experiment_md.experiment_dir, DE_NOVO_RNA_FASTA)
    else:
        return None

def get_expression_tsv(experiment_md):
    """get path to expression TSV file or None if not valid for this
    experiment. Will not include .gz extension or check for existence."""
    if experiment_md.challenge_id is Challenge.iso_quant:
        return osp.join(experiment_md.experiment_dir, EXPRESSION_TSV)
    else:
        return None
