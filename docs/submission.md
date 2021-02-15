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

When a team registers for LRGASP, they are assigned a [symbolic
identifier](#symbolic-identifiers), called the ``team_id``.  Other symbolic
experiment identifiers assigned by the team and must be valid [symbolic
identifier](#symbolic-identifiers), as described below.  Model experiment
identifiers must start with ``mod_`` and expression ones with ``exp_``.

Each team is given a file area to upload their results (a mechanism to be
determined).  The top-level directory name in that area is the
*team_id*. Below that are directories for each submission.  Experiments are
updated by replacing files, and experiments retracted simply by removing the
directory.

This diagram shows the general structure:

![Submission file hierarchy diagram](submit_tree.png)


## Symbolic identifiers

Various components of the submission system have symbolic identifiers.  These identifiers consist of [ASCII](https://en.wikipedia.org/wiki/ASCII) upper- and lower-case alphabetic characters, numbers, and underscores.  They must not begin with numbers.  In some cases, specific prefixes are required.

## Feature and read identifiers

Feature identifiers (transcripts and genes) and read identifiers may contain any combination of printing, non-whitespace characters [ASCII](https://en.wikipedia.org/wiki/ASCII).  This requirement is more restrictive than allowed by GTF.
