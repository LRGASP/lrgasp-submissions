# Metadata format

Metadata files are in [JSON](https://www.json.org/json-en.html) format.  JSON
provides a good compromise between able to store structured data and ease of
use.  Templates and a validator are provided.

## ``entry.json``

This file contains information about the *entry* and team that is submitting
it.  This is at the top of an entry tree (see [Submission structure](submission.md)).
See [``entry.json``](../examples/darwin_lab/iso_detect_ref_ont_drna/entry.json) for an example.  An empty
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

See [``experiment.json``](../examples/darwin_lab/iso_detect_ref_ont_drna/drnaA/experiment.json) for an example.
An empty template is also available: [``experiment.json``](../templates/experiment.json).

* ``experiment_id`` -  Experiment [symbolic identifer](metadata-identifiers.md#symbolic-identifiers) for this entry, defined by the submitter.
* ``experiment_type`` - one of ``model`` or ``expression``.
* ``description`` - description of experiment
* ``notes`` - notes (optional)
* ``species`` - one of ``hs``, ``mm``, or ``manatee``.
* ``is_kitchen_sink`` - If ``true`` (JSON boolean) if this is a kitchen sink experiment, otherwise ``false`` or omitted.
* ``libraries`` - list of LRGASP library accessions used in the experiment,  For non-kitchen sink, only one or two replicates of the same sample and library preparation method maybe specified.  For kitchen sink experiments, any combination of LRGASP libraries maybe specified.
* ```extra_libraries`` - list of non-LRGASP libraries that were used.  For other than kitchen sink experiments, only short RNA_Seq
  maybe added
  * ``repository`` - Public repository were data was obtained; one of the values in
    [Public repository identifiers](metadata-identifiers.md#public repository_identifiers)
  * ``acc`` - accession in a public repository for input data file
  * ``notes`` - notes about the file (optional)
* ``units`` - Expression units for expression results matrix: ``RPM``, ``RPKM``, ``FPKM``, ``TPM``, ``counts``.
* ``software`` - list of software used by the pipeline:
  * ``name`` - name of software package
  * ``description`` - description of software (optional)
  * ``version`` - version of software
  * ``url`` - URL to software repository
  * ``config`` - command line and/or configuration options
  * ``notes`` - notes about software or how it was used (optional)

