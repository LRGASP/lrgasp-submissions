"""
Load and validate model and expression entries.  This does full validation of
all metadata and data files.
"""
from lrgasp import LrgaspException, iter_to_str
from lrgasp.defs import Challenge
from lrgasp.defs import get_challenge_samples, challenge_desc
from lrgasp import entry_metadata
from lrgasp import model_data
from lrgasp import de_novo_rna_data
from lrgasp import read_model_map_data
from lrgasp import expression_data
from lrgasp.data_sets import get_lrgasp_rna_seq_metadata
from lrgasp.experiment_metadata import get_models_gtf, get_read_model_map_tsv, get_rna_fasta, get_expression_tsv

def _model_map_transcript_ids(read_model_map):
    "get list of all read_model_map transcript ids"
    return sorted(set([p.transcript_id for p in read_model_map if p.transcript_id is not None]))

def _validate_model_to_read_mapping(transcript_id, read_model_map):
    if read_model_map.get_by_transcript_id(transcript_id) is None:
        raise LrgaspException(f"transcript in models '{transcript_id}' not in read-model_map")

def _validate_read_mapping_to_model(transcript_id, models):
    # transcript might be None if specified as `*'
    if (transcript_id is not None) and (models.by_transcript_id.get(transcript_id) is None):
        raise LrgaspException(f"transcript in read_model_map '{transcript_id}' not in models")

def validate_ref_model_and_read_mapping(models, read_model_map):
    # all model mapping must be in models
    for transcript_id in _model_map_transcript_ids(read_model_map):
        _validate_read_mapping_to_model(transcript_id, models)
    # all transcripts must be in model map
    for trans in models:
        _validate_model_to_read_mapping(trans.transcript_id, read_model_map)

def _validate_ref_model_experiment(experiment_md):
    models_gtf = get_models_gtf(experiment_md)
    map_file = get_read_model_map_tsv(experiment_md)
    try:
        models = model_data.load(models_gtf)
        read_model_map = read_model_map_data.load(map_file)
        validate_ref_model_and_read_mapping(models, read_model_map)
    except Exception as ex:
        raise LrgaspException(f"validation failed on '{models_gtf}' and '{map_file}'") from ex

def _validate_de_novo_rna_to_read_mapping(transcript_id, read_model_map):
    if read_model_map.get_by_transcript_id(transcript_id) is None:
        raise LrgaspException(f"transcript in de novo RNAs '{transcript_id}' not in read-model_map")

def _validate_read_mapping_to_de_novo_rna(transcript_id, de_novo_rna_ids):
    # transcript might be None if specified as `*'
    if (transcript_id is not None) and (transcript_id not in de_novo_rna_ids):
        raise LrgaspException(f"transcript in read_model_map '{transcript_id}' not in de novo RNAs")

def validate_de_novo_rna_and_read_mapping(de_novo_rna_ids, read_model_map):
    # all model mapping must be in reads
    for transcript_id in _model_map_transcript_ids(read_model_map):
        _validate_read_mapping_to_de_novo_rna(transcript_id, de_novo_rna_ids)
    # all transcripts must be in model map
    for transcript_id in de_novo_rna_ids:
        _validate_de_novo_rna_to_read_mapping(transcript_id, read_model_map)

def _validate_de_novo_model_experiment(experiment_md):
    rna_fasta = get_rna_fasta(experiment_md)
    map_file = get_read_model_map_tsv(experiment_md)
    try:
        de_novo_rna_ids = de_novo_rna_data.load(rna_fasta)
        read_model_map = read_model_map_data.load(map_file)
        validate_de_novo_rna_and_read_mapping(de_novo_rna_ids, read_model_map)
    except Exception as ex:
        raise LrgaspException(f"validation failed on '{rna_fasta}' with '{map_file}'") from ex

def validate_expression_and_model(models, expression_mat):
    # all expression matrix ids must be in models
    for row in expression_mat.df.iterrows():
        if row[1].ID not in models.by_transcript_id:
            raise LrgaspException(f"expression matrix ID '{row[1].ID}' not found in models")

def _validate_expression_experiment(experiment_md):
    models_gtf = get_models_gtf(experiment_md)
    expression_tsv = get_expression_tsv(experiment_md)
    try:
        models = model_data.load(models_gtf)
        expression_mat = expression_data.load(expression_tsv, experiment_md)
        validate_expression_and_model(models, expression_mat)
    except Exception as ex:
        raise LrgaspException(f"validation failed on '{models_gtf}' with '{expression_tsv}'") from ex

def _validate_experiment_library(entry_md, experiment_md, rna_seq_md, library):
    sample = rna_seq_md.get_run_by_file_acc(library).sample
    valid_samples = get_challenge_samples(entry_md.challenge_id)
    if sample not in valid_samples:
        raise LrgaspException(f"library '{library}' sample '{sample}' is not valid for challenge '{entry_md.challenge_id}',"
                              " expected one of {}".format(iter_to_str(valid_samples)))

def _validate_experiment_libraries(entry_md, experiment_md):
    """check if libraries uses are compatible with challenge"""
    rna_seq_md = get_lrgasp_rna_seq_metadata()
    for library in experiment_md.libraries:
        _validate_experiment_library(entry_md, experiment_md, rna_seq_md, library)

def _validate_experiment(entry_md, experiment_md, allow_partial):
    if experiment_md.challenge_id != entry_md.challenge_id:
        raise LrgaspException(f"entry '{entry_md.entry_id}' challenge_id '{entry_md.challenge_id}' match experiment '{experiment_md.experiment_id}' challenge_id")
    _validate_experiment_libraries(entry_md, experiment_md)
    if experiment_md.challenge_id == Challenge.iso_detect_ref:
        _validate_ref_model_experiment(experiment_md)
    elif experiment_md.challenge_id == Challenge.iso_detect_de_novo:
        _validate_de_novo_model_experiment(experiment_md)
    elif experiment_md.challenge_id == Challenge.iso_quant:
        _validate_expression_experiment(experiment_md)
    else:
        raise LrgaspException("bug")

def validate_experiment(entry_md, experiment_md, allow_partial):
    try:
        _validate_experiment(entry_md, experiment_md, allow_partial)
    except Exception as ex:
        raise LrgaspException(f"validation of experiment '{experiment_md.experiment_id}' failed: {experiment_md.experiment_json}") from ex

def get_entry_samples(entry_md):
    rna_seq_md = get_lrgasp_rna_seq_metadata()
    samples = set()
    for ex in entry_md.experiments:
        for file_acc in ex.libraries:
            samples.add(rna_seq_md.get_run_by_file_acc(file_acc).sample)
    return samples

def validate_samples(entry_md):
    "validate that all samples are covered (requires all experiments"
    entry_samples = get_entry_samples(entry_md)
    challenge_samples = get_challenge_samples(entry_md.challenge_id)
    if entry_samples != challenge_samples:
        raise LrgaspException("{} must have all of the samples '{}', only '{}' were found".format(challenge_desc(entry_md.challenge_id),
                                                                                                  iter_to_str(challenge_samples),
                                                                                                  iter_to_str(entry_samples)))

def validate_experiment_consistency(entry_md, allow_partial):
    """validate that all experiments are consistent"""
    if not allow_partial:
        validate_samples(entry_md)

def _entry_data_validate(entry_md, allow_partial):
    entry_metadata.load_experiments_metadata(entry_md)

    for experiment_md in entry_md.experiments:
        validate_experiment(entry_md, experiment_md, allow_partial)
    validate_experiment_consistency(entry_md, allow_partial)

def entry_data_validate(entry_dir, *, allow_partial=False):
    """load and validate all metadata and data files for an entry, ensuring
    consistency.  Optionally restricted to one experiment for speed.  Setting
    allow_partial disables checking of submissions without all samples, checking
    incompletely entries."""
    entry_md = entry_metadata.load_dir(entry_dir)
    try:
        _entry_data_validate(entry_md, allow_partial=allow_partial)
    except Exception as ex:
        raise LrgaspException(f"validation of entry '{entry_md.entry_id}' failed: {entry_md.entry_json}") from ex
