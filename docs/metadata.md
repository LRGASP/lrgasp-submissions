# Metadata format

Metadata files are in [JSON](https://www.json.org/json-en.html) format.  JSON
provides a good compromise between able to store structured data and ease of
use.  Templates and a validator are provided.

## ``entry.json``

This file contains information about the *entry* and team that is submitting
it.  This is at the top of an entry tree (see [Submission structure](submission.md)).
See [``entry.json``](../examples/darwin_lab/iso_detect_ref_darwin_drna_ont/entry.json) for an example.  An empty
template is also available: [``entry.json``](../templates/entry.json).

* ``entry_id`` - submitter-assigned [symbolic identifer](metadata-identifiers.md#symbolic-identifiers) for this entry.
* ``challenge_id`` - challenge to which this entry is being submitted.
    See [LRGASP Challenge identifiers](metadata-identifiers.md#challenge-identifiers)
* ``team_name`` - the name of the Synapse team or Synapse user submitting the entry.  This should exactly match the
    name in Synapse.
* ``experiment_ids`` - Experiment ids, which is also the directory name containing the
    experiment.  It is a [symbolic identifer](metadata-identifiers.md#symbolic-identifiers) for this entry.
* ``data_category`` - one of ``long_only``, ``short_only``, ``long_short``, ``long_genome``, or ``freestyle``.
    See [Experiment data categories](metadata-identifiers.md#experiment-data-categories).
* ``samples`` - one or more of ``WTC11``, ``H1_mix``, ``ES``, ``blood``, or ``synthetic``.
    See [Sample identifiers](metadata-identifiers.md#sample-identifiers).
* ``library_preps`` - one or more of ``CapTrap``,``dRNA``, ``R2C2``, or ``cDNA``, as allowed by data category.
    See [Library prep](metadata-identifiers.md#library-prep).
* ``platforms`` - one or more of ``Illumina``, ``PacBio``, or * ``ONT`` . as allowed by data category.
    See [Sequencing platform](metadata-identifiers.md#sequencing-platform).
* ``notes`` - notes (optional)
* ``contacts`` - an array of contacts, with the first entry considered the primary contact
  * ``name`` - name of the contact
  * ``email`` - e-mail of the contact, which can be an e-mail list
  * ``notes`` - notes about the contact (optional)

## ``experiment.json``

This file describes the experiment, specifying all data files.  One is created
in each experiment directory (see [Experiment structure](submission.md#experiment-structure)).
Data files are either in the experiment directory or sub-directories.  All files paths in
``experiment.json`` are relative to the directory containing ``experiment.json``.

See [``experiment.json``](../examples/darwin_lab/iso_detect_de_novo_darwin/pbCDnaES/experiment.json) for an example.
An empty template is also available: [``experiment.json``](../templates/experiment.json).

* ``experiment_id`` - experiment [symbolic identifer](metadata-identifiers.md#symbolic-identifiers) for this entry, defined by the submitter.
* ``challenge_id`` - challenge to which this entry is being submitted, see [LRGASP Challenge identifiers](metadata-identifiers.md#challenge-identifiers). This must match the value in``entry.json``.
* ``description`` - description of experiment
* ``notes`` - notes (optional)
* ``species`` - one of ``human``, ``mouse``, ``manatee``, or ``synthetic``, see [Species identifiers](metadata-identifiers.md#species-identifiers).
* ``data_category`` - one of ``long_only``, ``short_only``, ``long_short``, ``long_genome``, or ``freestyle``,
    See [Experiment data categories](metadata-identifiers.md#experiment-data-categories).
* ``samples`` - one or more of ``WTC11``, ``H1_mix``, ``ES``, ``blood``, or ``synthetic``.
    See [Sample identifiers](metadata-identifiers.md#sample-identifiers).
* ``library_preps`` - one or more of ``CapTrap``,``dRNA``, ``R2C2``, or ``cDNA``, as allowed by data category.
    See [Library prep](metadata-identifiers.md#library-prep).
* ``platforms`` - one or more of ``Illumina``, ``PacBio``, or * ``ONT`` . as allowed by data category.
    See [Sequencing platform](metadata-identifiers.md#sequencing-platform).
* ``libraries`` - list of LRGASP RNA-Seq file accessions used in the experiment. The file accessions are those found in the [LRGASP RNA-Seq Data Matrix](rnaseq-data-matrix.md). For non-freestyle experiments, only replicates of the same sample and library preparation.  It must be one sequence method, or one sequencing method plus Illumina short-read sequencing.   For freestyle experiments, any combination of LRGASP libraries may be specified, with at least one LRGASP library being used. For paired-end Illumina experiments, both pairs must be specified.
* ``extra_libraries`` - list of non-LRGASP libraries files accessions that were used.  Optional; should be empty or omitted for non-freestyle experiments.  For Challenge 3, may also include external transcript that is used.
  * ``repository`` - Public repository where data was obtained; one of the values in
    [Public repository identifiers](metadata-identifiers.md#public-repository-identifiers)
  * ``acc`` - accession in a public repository for input data file.
  * ``notes`` - notes about the file (optional)
* ``software`` - list of software used by the pipeline:
  * ``name`` - the name of the software package
  * ``description`` - description of software (optional)
  * ``version`` - version of the software
  * ``url`` - URL to the software repository
  * ``config`` - command line and/or configuration options
  * ``notes`` - notes about the software or how it was used (optional)

