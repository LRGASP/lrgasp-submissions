# Submission tools

A package of command-line programs is provided to assist in submitting LRGASP.  Participants are required to validate their files in
an entry before submitting.

The code is installable from the [PyPi lrgasp-tools package](https://pypi.org/project/lrgasp-tools/), and the
source is available on from the [GitHub LRGASP-submissions repository](https://github.com/LRGASP/lrgasp-submissions).
If there are problems, please [create a ticket on GitHub](https://github.com/LRGASP/lrgasp-submissions/issues).

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

- `lrgasp-validate-models` - validate a ``models.gtf.gz`` file
- `lrgasp-validate-read-model-map` - validate a `read_model_map.tsv.gz` file, optionally checking against a model GTF
- `lrgasp-validate-expression-matrix` - validate an `expression.tsv.gz` file, optionally checking against a model GTF
- `lrgasp-validate-experiment-metadata` - validate an `experiment.json` metadata file
- `lrgasp-validate-entry-metadata`- validate an `entry.json` metadata file
- `lrgasp-validate-entry` - validate a full entry given a populated entry directory.
