# Metadata format

Metadata files are in [JSON](https://www.json.org/json-en.html) format.  JSON
provides a good compromise between able to store structured data and ease of
use.  Templates and a validator are provided.

## ``entry.json``

This file contains information about the *entry* and team that is submitting
it.  This is at the top of an entry tree (see [Submission structure](submission.md)).
See [``entry.json``](../examples/darwin-lab/ont_drna_model_ref/entry.json) for an example.  An empty
template is also available: [``entry.json``](../templates/entry.json).

* ``entry_id`` - submitter-assigned [symbolic identifer](metadata-identifiers.md#symbolic-identifiers) for this entry.
* ``challenge_id`` - challenge to which this entry is being submitted, see [LRGASP Challenge identifiers](metadata-identifiers.md#LRGASP_Challenge_identifiers) for valid values.
* ``team_id`` - the Synapse *team* identifier.
* ``team_name`` - name of the submitting lab
* ``experiment_ids`` - Experiment ids, which is also the directory name containing the
  experiment.  It is [symbolic identifer](metadata-identifiers.md#symbolic-identifiers) for this entry.
* ``notes`` - notes (optional)
* ``contacts`` - array of contacts, with the first entry considered the primary contact
  * ``name`` - name of the contact
  * ``email`` - e-mail of the contact, which can be an e-mail list
  * ``notes`` - notes about the contact (optional)

## ``experiment.json``

This file describes the experiment, specifying all data files.  One is created
in each experiment directory (see [Experiment structure](submission.md#experiment-structure)).
Data files are either in the experiment directory or a sub-directories.  All files paths in
``experiment.json`` are relative to the directory containing ``experiment.json``.

See [``experiment.json``](../examples/darwin-lab/ont_drna_model_ref/model_ont_drna1/experiment.json) for an example.
An empty template is also available: [``experiment.json``](../templates/experiment.json).

* ``experiment_id`` -  Experiment [symbolic identifer](metadata-identifiers.md#symbolic-identifiers) for this entry.
* ``experiment_type`` - one of ``model`` or ``expression``.
* ``description`` - description of experiment
* ``model_experiment_id`` - if an ``expression`` experiment, the model ``experiment_id`` for which the expressions were computed.
* ``notes`` - notes (optional)
* ``samples`` - list of LRGASP [sample identifiers](metadata-identifiers.md#Sample-identifiers) used in the experiment.
* ```data_files`` - list of input data files supplied by the LRGASP
  * ``acc`` - accession (ENCODE or LRGASP) for input data files (optional if URL supplied)
  * ``url`` - URL to file; intended for non-LRGASP provided files (optional if acc supplied)
  * ``notes`` - notes about the file (optional)
* ``units`` - Expression units for expression results matrix: ``RPM``, ``RPKM``, ``FPKM``, ``TPM``, ``counts``.
* ``software`` - list of software used by the pipeline:
  * ``name`` - name of software package
  * ``description`` - description of software (optional)
  * ``version`` - version of software
  * ``url`` - URL to software repository
  * ``config`` - command line and/or configuration options (optional)
  * ``notes`` - notes about software or how it was used (optional)

