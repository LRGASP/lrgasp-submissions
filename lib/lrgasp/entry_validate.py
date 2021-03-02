"""
Load and validate a model entry
"""
import os.path as osp
from lrgasp import LrgaspException
from lrgasp.defs import Challenge, ExperimentType, challengeToExperimentType
from lrgasp.entry_metadata import entry_load_dir
from lrgasp.experiment_metadata import experiment_load_from_entry

def _validate_model_experiment(entry, experiment):
    pass

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

def entry_data_validate(entry_dir):
    """load and validate all metadata and data files for an entry, ensuring
    consistency."""
    entry = entry_load_dir(entry_dir)
    for experiment_id in entry.experiment_ids:
        _validate_experiment(entry, experiment_id)
