"""
Load and validate a model entry
"""
import os.path as osp
from lrgasp.defs import Challenge, ExperimentType, challengeToExperimentType
from lrgasp.entry_metadata import entry_load_dir
from lrgasp.experiment_metadata import experiment_load_from_entry

def _validate_model_experiment(entry, experiment_id):
    experiment = experiment_load_from_entry(entry, experiment_id)
    if experiment.experiment_type is ExperimentType.expression:
        if fld_model_experiment_id.name not in experiment:
            raise LrgaspException(f"{desc} must specify experiment.{fld_model_experiment_id.name} for {experiment.experiment_type} experiments")
    else:
        if fld_model_experiment_id.name in experiment:
            raise LrgaspException(f"{desc} must not specify experiment.{fld_model_experiment_id.name} for {experiment.experiment_type} experiments")


def entry_data_validate(entry_dir):
    """load and validate all metadata and data files for an entry, ensuring
    consistency."""
    entry = entry_load_dir(entry_dir)
    for experiment in entry.experiment_ids:
        _validate_experiment(entry, experiment_id)
