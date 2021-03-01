"""
Load and validate a model entry
"""
import os.path as osp
from lrgasp.defs import Challenge, ExperimentType, challengeToExperimentType
from lrgasp.entry_metadata import entry_load_fs
from lrgasp.experiment_metadata import experiment_load_from_entry

def _validate_experiment(entry, experiment_id):
    experiment = experiment_load_from_entry(entry, experiment_id)


def load_model_entry(model_entry_json):
    """load and validate all metadata and data files model entry, ensuring
    consistency."""
    entry = entry_load_fs(model_entry_json)
    for experiment in entry.experiment_ids:
        _validate_experiment(entry, experiment_id)
