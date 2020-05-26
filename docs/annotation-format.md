# Genome annotation submission format

## GTF format
Genome transcript annotation submissions are in GTF format
(see [GTF2.2](https://mblab.wustl.edu/GTF22.html)
and [Ensembl GFF/GTF File Format](https://www.ensembl.org/info/website/upload/gff.html)).

Only `exon` features are used, and exons of a given transcript are linked together by the `transcript_id` attribute.  Gaps of at least XX bases between exons are assumed
to be introns.  Smaller gaps are closed, combining the exon features.  The evaluation ignores other features
that are provided, however, they will still be validated for syntax and consistency.

The standard GTF fields have the following restrictions:
* seqname - Must be one of the sequence identifiers in the LRGAPS [reference genomes](reference-genomes.md).
* source - **FIXME: making this a submission name is a nice way to prevent data confusion**
* feature - Only `exon` is used.
* start - Standard, one-based start position.
* end - Standard, one-based end position.
* score - Ignored.
* strand - Must be specified as `+` or `-` on `exon` features, other features types may be validated.
* frame - Must be `.` on `exon` features, other features types may be validated.
* attributes:
  * `transcript_id` - Required for all `exon` features and assigned by the submitter.
  * `reference_transcript_id` - Optional, used to indicate the transcript is a reference call for the specified [reference transcript](reference-genomes.md).
 If specified, it must be specified for all exons of the transcript.


An example submission GTF file is at [../examples/example.gtf](../examples/example.gtf).

## File naming
Files must be named `xxx.gtf` (FIXME defend better) and maybe compressed with `gzip` and 
then have a name in the form `xxx.gtf.gz`.

## Validation

A validation program is provide dfor the annotation GTFs, and the submitter must run this before submitting the file.
