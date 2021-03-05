# Submission tools

A package of command line programs is provided to assist in making a
submission to LRGASP.  Participants are required to validated their files in
an entry before submitting.

The code is installable from the [PyPi lrgasp-tools package](https://pypi.org/project/lrgasp-tools/) and the
source is available on from the [GitHub lrgasp-submissions repository](https://github.com/LRGASP/lrgasp-submissions).
If you have problems, please [create an a ticket on GitHub](https://github.com/LRGASP/lrgasp-submissions/issues).

## Installation

Python 3.7 or greater required to run lrgasp-tools.  The recommend method for installation is using
a [virtual environment](https://docs.python.org/3/tutorial/venv.html).  Here is an example
of a typical installations:

```
    python3 -m virtualenv lrgasp-env
    source ./lrgasp-env/bin/activate
    pip install lrgasp-tools
```

## Validation tools

Programs are provided to independently validate each of the required files.
These only check the syntax of the files and are intended to allow for quick
validation during development.  Another tool does full checking of the an entry,
including file syntax validation as well as relationships between files.

- `lrgasp-validate-models` - validate a ``models.gtf.gz`` file
- `lrgasp-validate-read-model-map` - validate a `read_model_map.tsv.gz` file
- `lrgasp-validate-expression-matrix` - validate an `expression.tsv.gz` file
- `lrgasp-validate-experiment-metadata` - validate an `experiment.json` metadata file
- `lrgasp-validate-entry-metadata`- validate an `entry.json` metadata file
- `lrgasp-validate-entry` - validate a full entry given a populated entry directory.
