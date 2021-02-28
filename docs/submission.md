# Submission structure

Submissions to LRGASP consist of experiments targeting a particular challenge
submitted by a *team*.  With two types of experiment: *model* and
*expression*.  Model experiments are genomic transcript model predictions, and
expression experiments are transcript expression quantification of a set of
submitted models.

A given challenge may combine results from multiple, distinct experiments.
For instance, the high-quality genome isoform annotation challenge may
include both human and mouse experiments. To accommodate this, *experiments*
are grouped into *entries* against a particular challenge.  An *entry* is
the unit of both submission and evaluation.  The *experiments* in an *entry*
should uses as similar a set of parameters and data as possible to allow
for meaningful combination of the results.

A team may submit two *entries* per challenge.  The purpose of this
limit is to prevent the evaluation process from being overwhelmed by
experiments with minor variations.  An *entry* maybe updated or deleted
up to the submission deadline.

When a team registers for LRGASP on [Synapse](https://www.synapse.org), they are assigned a [Synapse
identifier](metadata-identifiers.md#synapse-identifiers), called the ``team_id``.  Other symbolic
experiment identifiers assigned by the team and must be valid [symbolic
identifier](metadata-identifiers.md#symbolic-identifiers), as described below.

Each team is given a file area to upload their results (a mechanism to be
determined).  The top-level directory name in that area is the
*team_id*. Below that are directories for each submission.  Experiments are
updated by replacing files, and experiments retracted simply by removing the
directory.

This diagram shows the general structure:

![Submission file hierarchy diagram](submit_tree.png)

## Experiment structure

Model experiments must contain the following files:

- ```experiment.json``` - [Experiment metadata](metadata.md#experiment.json) describing the experiment results
- ```models.gtf.gz``` - [GTF file](model-format.md} with model annotations, compressed with gzip.
- ```read_model_map.tsv.gz``` [Read to model map file](read_model_map_format.md) that associates every transcript model with a least one read.

Quantification experiments must contain the following files:

- ```experiment.json``` - [Experiment metadata](metadata.md#experiment.json) describing the experiment results
- ```expression-matrix.tsv.gz``` - [Expression matrix file](expression_matrix_format.md) with the results of the experiment.
- ```models.gtf.gz``` - [GTF file](model-format.md} with target model annotations, compressed with gzip.

## Detailed specifications

- [Metadata](metadata.md)
- [Reference genomes and transcripts](reference-genomes.md)
- [Transcript model format](model-format.md)
- [Read to model map format](read_model_map_format.md)
- [Transcript expression matrix format](expression_matrix_format.md)
