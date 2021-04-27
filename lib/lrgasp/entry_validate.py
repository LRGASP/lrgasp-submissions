"""
Load and validate model and expression entries
"""
import os.path as osp
from lrgasp import LrgaspException
from lrgasp.defs import Challenge, MODELS_GTF, DE_NOVO_RNA_FASTA, READ_MODEL_MAP_TSV, EXPRESSION_TSV
from lrgasp.defs import get_challenge_samples
from lrgasp import entry_metadata
from lrgasp import experiment_metadata
from lrgasp import model_data
from lrgasp import de_novo_rna_data
from lrgasp import read_model_map_data
from lrgasp import expression_data
from lrgasp.metadata_validate import set_to_str
from lrgasp.data_sets import get_lrgasp_rna_seq_metadata

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

def _validate_ref_model_experiment(experiment):
    model_gtf = osp.join(experiment.experiment_dir, MODELS_GTF)
    map_file = osp.join(experiment.experiment_dir, READ_MODEL_MAP_TSV)
    try:
        models = model_data.load(model_gtf)
        read_model_map = read_model_map_data.load(map_file)
        validate_ref_model_and_read_mapping(models, read_model_map)
    except Exception as ex:
        raise LrgaspException(f"validation failed on '{model_gtf}' and '{map_file}'") from ex

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

def _validate_de_novo_model_experiment(experiment):
    rna_fasta = osp.join(experiment.experiment_dir, DE_NOVO_RNA_FASTA)
    map_file = osp.join(experiment.experiment_dir, READ_MODEL_MAP_TSV)
    try:
        de_novo_rna_ids = de_novo_rna_data.load(rna_fasta)
        read_model_map = read_model_map_data.load(map_file)
        validate_de_novo_rna_and_read_mapping(de_novo_rna_ids, read_model_map)
    except Exception as ex:
        raise LrgaspException(f"validation failed on '{rna_fasta}' with '{map_file}'") from ex

def validate_expression_and_model(models, expression):
    # all expression matrix ids must be in models
    for row in expression.iterrows():
        if row[1].ID not in models.by_transcript_id:
            raise LrgaspException(f"expression matrix ID '{row[1].ID}' not found in models")

def _validate_expression_experiment(experiment):
    model_gtf = osp.join(experiment.experiment_dir, MODELS_GTF)
    expression_tsv = osp.join(experiment.experiment_dir, EXPRESSION_TSV)
    try:
        models = model_data.load(model_gtf)
        expression = expression_data.load(expression_tsv)
        validate_expression_and_model(models, expression)
    except Exception as ex:
        raise LrgaspException(f"validation failed on '{model_gtf}' with '{expression_tsv}'") from ex

def _validate_experiment_library(entry, experiment, rna_seq_md, library):
    sample = rna_seq_md.get_run_by_file_acc(library).sample
    valid_samples = get_challenge_samples(entry.challenge_id)
    if sample not in valid_samples:
        raise LrgaspException(f"library '{library}' sample '{sample}' is not valid for challenge '{entry.challenge_id}',"
                              " expected one of {}".format(set_to_str(valid_samples)))

def _validate_experiment_libraries(entry, experiment):
    "check if libraries uses are compatible with challenge"""
    rna_seq_md = get_lrgasp_rna_seq_metadata()
    for library in experiment.libraries:
        _validate_experiment_library(entry, experiment, rna_seq_md, library)

def _validate_experiment(entry, experiment):
    if experiment.challenge_id != entry.challenge_id:
        raise LrgaspException(f"entry '{entry.entry_id}' challenge_id '{entry.challenge_id}' match experiment '{experiment.experiment_id}' challenge_id")
    _validate_experiment_libraries(entry, experiment)
    if experiment.challenge_id == Challenge.iso_detect_ref:
        _validate_ref_model_experiment(experiment)
    elif experiment.challenge_id == Challenge.iso_detect_de_novo:
        _validate_de_novo_model_experiment(experiment)
    elif experiment.challenge_id == Challenge.iso_quant:
        _validate_expression_experiment(experiment)
    else:
        raise LrgaspException("bug")

def validate_experiment(entry, experiment_id):
    experiment = experiment_metadata.load_from_entry(entry, experiment_id)
    try:
        _validate_experiment(entry, experiment)
    except Exception as ex:
        raise LrgaspException(f"validation of experiment '{experiment_id}' failed: {experiment.experiment_json}") from ex

def _entry_data_validate(entry, restrict_experiment_id=None):
    if restrict_experiment_id is not None:
        if restrict_experiment_id not in entry.experiment_ids:
            raise LrgaspException(f"entry '{entry.entry_id}' does not contain experiment '{restrict_experiment_id}'")
        experiment_ids = [restrict_experiment_id]
    else:
        experiment_ids = entry.experiment_ids

    for experiment_id in experiment_ids:
        validate_experiment(entry, experiment_id)

def entry_data_validate(entry_dir, restrict_experiment_id=None):
    """load and validate all metadata and data files for an entry, ensuring
    consistency.  Optionally restricted to one experiment for speed"""
    entry = entry_metadata.load_dir(entry_dir)
    try:
        _entry_data_validate(entry, restrict_experiment_id=restrict_experiment_id)
    except Exception as ex:
        raise LrgaspException(f"validation of entry '{entry.entry_id}' failed: {entry.entry_json}") from ex
