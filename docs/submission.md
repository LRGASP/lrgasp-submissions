# Submission structure

Submissions to LRGASP consist of a set of experiments targeting a particular
challenge submitted by a *team*.  With two types of experiment: *model* and
*expression*.  Model experiments are genomic transcript model predictions, and
expression experiments are transcript expression quantification of a set of
submitted models.

A given challenge may combine results from multiple, distinct experiments.
For instance, the high-quality genome isoform annotation challenge will
include both human and mouse experiments. To accommodate this, *experiments*
are grouped into *entries* against a particular challenge.  An *entry* is
the unit of both submission and evaluation.  The *experiments* in an *entry*
should uses as similar a set of parameters and data as possible to allow
for meaningful combination of the results.

When a team registers for LRGASP on [Synapse](https://www.synapse.org), they are assigned a [Synapse
identifier](metadata-identifiers.md#synapse-identifiers), called the ``team_id``.  Other symbolic
experiment identifiers assigned by the team and must be valid [symbolic
identifier](metadata-identifiers.md#symbolic-identifiers), as described below.

## Submission overview

This diagram shows the general logical and directory structure of LRGASP entries,
which are explain below.

![Submission file hierarchy diagram](submit_tree.png)

## Entry structure

Each ``entry`` must conform to fix, straight-forward file hierarchy.
Each entry to a challenge is in a directory with the same name as the `entry_id`.
The entry ids mustprefixed with the [LRGASP Challenge identifier](metadata-identifiers.md#lrgasp-challenge-identifiers) followed by
a `_` and a unique team-defined name.  For instance:

- `iso_detect_ref_ont_drna``
- `iso_quant_ont_drna1`
- `iso_detect_de_novo_pb1`

The entry directory contains and `entry.json` [entry
metadata](metadata.md#entry.json) describing the entry.  Within the entry directory,
there is a directory per experiment, with each directory named the same as the
submitter-defined ``experiment_id`.

All entries MUST be validated by the provided [submission
tools](submission-tools) before uploading.

## Experiment structure

Model experiments must contain the following files:

- `experiment.json` - [Experiment metadata](metadata.md#experiment.json) describing the experiment results
- `models.gtf.gz` - [GTF file](model-format.md} with model annotations, compressed with gzip.
- `read_model_map.tsv.gz` [Read to model map file](read_model_map_format.md) that associates every transcript model with a least one read.

Quantification experiments must contain the following files:

- `experiment.json` - [Experiment metadata](metadata.md#experiment.json) describing the experiment results
- `expression.tsv.gz` - [Expression matrix file](expression_matrix_format.md) with the results of the experiment.
- `models.gtf.gz` - [GTF file](model-format.md} with target model annotations, compressed with gzip.

## Detailed specifications

- [Metadata](metadata.md)
- [Reference genomes and transcripts](reference-genomes.md)
- [Transcript model format](model-format.md)
- [Read to model map format](read_model_map_format.md)
- [Transcript expression matrix format](expression_matrix_format.md)
- [Submission tools](submission-tools.md)
