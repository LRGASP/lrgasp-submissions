"""
Load and validate a model entry
"""
import os.path as osp
from lrgasp import LrgaspException
from lrgasp.defs import Challenge, ExperimentType, challengeToExperimentType, MODELS_GTF, READ_MODEL_MAP_TSV
from lrgasp.entry_metadata import entry_load_dir
from lrgasp.experiment_metadata import experiment_load_from_entry
from lrgasp.gtf import gtf_load, get_trans_id
from lrgasp.read_model_map import read_model_map_load

def _load_models(entry, experiment):
    gtf_file = osp.join(experiment.experiment_dir, MODELS_GTF)
    models = gtf_load(gtf_file)
    if len(models) == 0:
        raise LrgaspException(f"entry {entry.entry_id} experiment {experiment.experiment_id} model GTF is empty: {gtf_file}")
    return models, gtf_file

def _validate_model_and_read_mapping(models, read_model_map):
    # all transcripts must be in model map
    for trans in models:
        trans_id = get_trans_id(trans)
        mapping = read_model_map.transcript_id
        if (trans.transcript_id not in read_model_map.transcript_id):
            raise LrgaspException(f"transcript {trans.transcript_id} not in read to model map")


def _validate_model_experiment(entry, experiment):
    models, gtf_file = _load_models(entry, experiment)
    map_file = osp.join(experiment.experiment_dir, READ_MODEL_MAP_TSV)
    read_model_map = read_model_map_load(map_file)
    try:
        _validate_model_and_read_mapping(models, read_model_map)
    except Exception as ex:
        raise LrgaspException(f"entry {entry.entry_id} experiment {experiment.experiment_id} validation failed on {gtf_file} and {map_file}")


def _validate_expression_experiment(entry, experiment):
    pass

def _validate_experiment(entry, experiment_id):
    experiment = experiment_load_from_entry(entry, experiment_id)
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
    entry = entry_load_dir(entry_dir)

    if restrict_experiment_id is not None:
        if restrict_experiment_id not in entry.experiment_ids:
            raise LrgaspException(f"entry {entry.entry_id} does not contain experiment {restrict_experiment_id}")
        experiment_ids = [restrict_experiment_id]
    else:
        experiment_ids = entry.experiment_ids

    for experiment_id in experiment_ids:
        _validate_experiment(entry, experiment_id)
