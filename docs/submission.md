# Submission structure

Submissions to LRGASP target a particular challenge, with two types of
submissions: model and expression.  Model submissions are genomic transcript
model predictions and expression submissions are transcript expression
estimates of a set of submitted models.

A participant may submit up to two model submission per challenge and up to two expression submissions per model submissions.  The purpose of this limit to prevent the evaluation process from being overwhelmed by submissions with minor variation.  If you have a need to exceed this limit, please contact [lrgasp-support](mailto:lrgasp-support-group@ucsc.edu).

When a submitter registers for LRGASP, they are assigned a symbolic,
meaningful ``submitter_id``.  Other submission identifiers are assigned by the submitter and must be valid python-style identifiers.  Model submission identifiers must start with ``mod_`` and expression ones with ``exp_``.

Each submitter is given a file area to upload their results (mechanism to be determined).  The top level directory name in that area is the *submitter_id*. Below that are directories for each submission.  Submissions may be updated by replacing files, and submissions retracted simply by removing the directory

The general structure is show by this diagram:

<submit_tree.png>






