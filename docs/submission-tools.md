# Submission tools

A package of command-line programs is provided to assist in submitting LRGASP.  Participants are required to validate their files in
an entry before submitting.

The code is installable from the [PyPi lrgasp-tools package](https://pypi.org/project/lrgasp-tools/), and the
source is available on from the [GitHub LRGASP-submissions repository](https://github.com/LRGASP/lrgasp-submissions).

If there are problems, please [create a ticket on GitHub](https://github.com/LRGASP/lrgasp-submissions/issues).
If there is a program failure, run with `--logDebug` to report errors.

## Installation

Python 3.7 or greater is required to run lrgasp-tools.  The recommended method for installation is using
a [virtual environment](https://docs.python.org/3/tutorial/venv.html).  Here is an example
of a typical installation:

```
    python3 -m virtualenv lrgasp-env
    source ./lrgasp-env/bin/activate
    pip install lrgasp-tools
```

## Validation tools

Programs are provided to validate each of the required files independently.
These only check the syntax of the files and are intended to allow for quick
validation during development.  Another tool does complete checking of an entry,
including file syntax validation and relationships between files.

- `lrgasp-validate-models` - validate a `models.gtf.gz` file
- `lrgasp-validate-de-novo-rna` - validate a `rna.fasta.gz` file.
- `lrgasp-validate-read-model-map` - validate a `read_model_map.tsv.gz` file, optionally checking against a model GTF or de novo RNA fasta.
  - options ``--models_gtf``, ``--rna_fasta``
- `lrgasp-validate-expression-matrix` - validate an `expression.tsv.gz` file, optionally checking against a model GTF
  - option ``--models_gtf``
- `lrgasp-validate-experiment-metadata` - validate an `experiment.json` metadata file
- `lrgasp-validate-entry-metadata`- validate an `entry.json` metadata file
- `lrgasp-validate-entry` - validate a full entry given a populated entry directory, optionally skipping data validation
  to speed up initial consistency checks.
  - option ``--metadata_only``

## Submission programs

These tools are provide to assist submission of entries to LRGASP challenges to Synapse.
See [Uploading to Synapse and submitting to LRGASP](synapse.md) for details on the submission
process.

- `lrgasp-upload-entry` - uploads or updates an [LRGASP entry](submission.md/#entry_structure) metadata and data to the participates private project.
  This does not submit the entry for evaluation, which must be done in a separate step.
- `lrgasp-synapse-download` - download file hierarchies from Synapse.  While mainly intended for LRGASP organizers,
  this may also be used by participates to download their entries if they need to review them.
