"""
Load and validate model and expression entries
"""
import os.path as osp
from lrgasp import LrgaspException
from lrgasp.defs import ExperimentType, challengeToExperimentType, MODELS_GTF, READ_MODEL_MAP_TSV, EXPRESSION_TSV
from lrgasp import entry_metadata
from lrgasp import experiment_metadata
from lrgasp import model_data
from lrgasp import read_model_map_data
from lrgasp import expression_data

def _validate_trans_and_read_mapping(trans, read_model_map):
    if read_model_map.get_by_transcript_id(trans.transcript_id) is None:
        raise LrgaspException(f"transcript in models {trans.transcript_id} not in read-model_map")

def _validate_read_mapping_trans(transcript_id, models):
    if models.by_transcript_id.get(transcript_id) is None:
        raise LrgaspException(f"transcript in read_model_map {transcript_id} not in models")

def _validate_model_and_read_mapping(models, read_model_map):
    # all model mapping must be in models
    for transcript_id in set([p.transcript_id for p in read_model_map]):
        _validate_read_mapping_trans(transcript_id, models)
    # all transcripts must be in model map
    for trans in models:
        _validate_trans_and_read_mapping(trans, read_model_map)

def _validate_model_experiment(entry, experiment):
    gtf_file = osp.join(experiment.experiment_dir, MODELS_GTF)
    map_file = osp.join(experiment.experiment_dir, READ_MODEL_MAP_TSV)
    try:
        models = model_data.load(gtf_file)
        read_model_map = read_model_map_data.load(map_file)
        _validate_model_and_read_mapping(models, read_model_map)
    except Exception as ex:
        raise LrgaspException(f"entry {entry.entry_id} experiment {experiment.experiment_id} validation failed on {gtf_file} and {map_file}") from ex

def _validate_expression_and_model(models, expression):
    # all expression matrix ids must be in models
    for row in expression.iterrows():
        if row[1].ID not in models.by_transcript_id:
            raise LrgaspException(f"expression matrix ID {row[1].ID} not found in models")

def _validate_expression_experiment(entry, experiment):
    gtf_file = osp.join(experiment.experiment_dir, MODELS_GTF)
    expression_tsv = osp.join(experiment.experiment_dir, EXPRESSION_TSV)
    try:
        models = model_data.load(gtf_file)
        expression = expression_data.load(expression_tsv)
        _validate_expression_and_model(models, expression)
    except Exception as ex:
        raise LrgaspException(f"entry {entry.entry_id} experiment {experiment.experiment_id} validation failed on {gtf_file} and {expression_tsv}") from ex

def _validate_experiment(entry, experiment_id):
    experiment = experiment_metadata.load_from_entry(entry, experiment_id)
    experiment_type = challengeToExperimentType(entry.challenge_id)
    if experiment.experiment_type is not experiment_type:
        raise LrgaspException(f"entry {entry.entry_id} challenge {entry.challenge_id} does not consistent with experiment {experiment_id} type {experiment_type}")
    if experiment_type == ExperimentType.model:
        _validate_model_experiment(entry, experiment)
    else:
        _validate_expression_experiment(entry, experiment)

def entry_data_validate(entry_dir, restrict_experiment_id=None):
    """load and validate all metadata and data files for an entry, ensuring
    consistency.  Optionally restricted to one experiment to speed"""
    entry = entry_metadata.load_dir(entry_dir)

    if restrict_experiment_id is not None:
        if restrict_experiment_id not in entry.experiment_ids:
            raise LrgaspException(f"entry {entry.entry_id} does not contain experiment {restrict_experiment_id}")
        experiment_ids = [restrict_experiment_id]
    else:
        experiment_ids = entry.experiment_ids

    for experiment_id in experiment_ids:
        _validate_experiment(entry, experiment_id)
