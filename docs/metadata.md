# Metadata format

Metadata files are in [JSON](https://www.json.org/json-en.html) format.  JSON
provides a good compromise between able to store structured data and ease of
use.  Templates and a validator are provided.

## ``team.json``
This file contains information about the submitting team.  This is at the top
of the team's tree (see [Experiment structure](experiment.md)) and
applies to all experiments by the group.  See
[``team.json``](../examples/experts/team.json) for an example.  An
empty template is also available:
[``team.json``](../templates/team.json).

* ``team_id`` - [symbolic identifer](experiment.md#symbolic-identifiers) for the team, assigned when the user registers for LRGASP.
* ``group_name`` - name of the submitting lab
* ``group_url`` - URL of the submitting lab page (optional)
* ``notes`` - notes (optional)
* ``contacts`` - array of contacts, with the first entry considered the primary contact
  * ``name`` - name of the contact
  * ``email`` - e-mail of the contact, which can be an e-mail list
  * ``notes`` - notes about the contact (optional)

## ``experiment.json``
This file describes the experiment, specifying all data files.  One is created
in each experiment directory (see [Experiment structure](experiment.md)).  Data
files are either in the experiment directory or a sub-directories.  All files
paths in ``experiment.json`` are relative to the directory containing  ``experiment.json``.

See [``experiment.json``](../examples/experts/mod_try/experiment.json) for an example.
An empty template is also available: [``experiment.json``](../templates/experiment.json).

* ``team_id`` - must match the ``team_id`` in ``team.json``.
* ``experiment_id`` - team-defined [symbolic identifer](experiment.md#symbolic-identifiers), unique to that team.
* ``description`` - description of experiment
* ``challenge_id`` - one of the valid [challenge symbolic identifers](metadata-identifiers.md#LRGASP-Challenge-identifiers).
* ``experiment_type`` - one of ``model`` or ``expression``.
* ``model_experiment_id`` - if an ``expression`` experiment, the model ``experiment_id`` for which the expressions were computed.
* ``notes`` - notes (optional)
* ```data_files`` - list of input data files supplied by the LRGASP
  * ``acc`` - accession (ENCODE or LRGASP) for input data files (optional if URL supplied)
  * ``url`` - URL to file; intended for non-LRGASP provided files (optional if acc supplied)
  * ``notes`` - notes about the file (optional)
* ``result_files`` - List of files descriptions for submitted files:
  * ``fname`` - name of file (without directory), compressed with required extensions.
  * ``ftype`` - type of file, one of:
    * ``model_gtf``- [Transcript model format](model-format.md)
    * ``read_model_map`` - [Read to transcript model map](read_model_map_format.md)
    * ``expression_matrix`` - [Transcript expression matrix format](expression_matrix_format.md)
  * ``md5`` - md5 sum of file, as a hexadecimal string (output from ``md5sum`` command)
  * ``units`` - Expression units for expression results matrix: ``RPM``, ``RPKM``, ``FPKM``, ``TPM``, ``counts``.
  * ``notes`` - notes about the file (optional)
* ``software`` - list of software used by the pipeline:
  * ``name`` - name of software package
  * ``description`` - description of software (optional)
  * ``version`` - version of software
  * ``url`` - URL to software repository
  * ``config`` - command line and/or configuration options (optional)
  * ``notes`` - notes about software or how it was used (optional)
  
