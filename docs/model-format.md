# Transcript model format

## GTF format

Genome transcript annotation submissions are in GTF format
(see [GTF2.2](https://mblab.wustl.edu/GTF22.html)
and [Ensembl GFF/GTF File Format](https://www.ensembl.org/info/website/upload/gff.html)).

Only `exon` features are used, and exons of a given transcript are linked together by the `transcript_id` attribute.  Gaps of at least XX bases between exons are assumed
to be introns.  Smaller gaps are closed, combining the exon features.  The evaluation ignores other features
that are provided, however, they will still be validated for syntax and consistency.

The standard GTF fields have the following restrictions:

* seqname - Must be one of the sequence identifiers in the LRGAPS [reference genomes](reference-genomes.md).
* source - Ignored.
* feature - Only `exon` is used. Other types of records are ignored.
* start - Standard, one-based start position.
* end - Standard, one-based end position.
* score - Ignored.
* strand - Must be specified as `+`, `-` or `.` on `exon` features, other features types may be validated.
* frame - Should be `.` on `exon` features, but not valid. Others features types may be validated.
* attributes:
  * `transcript_id` - Required for all `exon` features and assigned by the submitter.
  * `gene_id` - Required for all `exon` features.  While not evaluated by LRGASP, it is unclear if this is require by GTF. Some tools, such as the UCSC Genome Browse and command-line tools, will fail without `gene_id`.  The assigned `gene_id` doesn't have to represent an actual gene. However, it must not reflect impossible genes, such as those on different chromosomes.  If gene assignment are not supported, it suggest that each transcript is assigned it own `gene_id`, which maybe the same as the `transcript_id`.
  * `reference_transcript_id` - Optional, used to indicate the transcript is a reference call for the specified [reference transcript](reference-genomes.md).
  * `reference_gene_id` - Optional, used to indicate the gene is a reference call for the specified [reference gene](reference-genomes.md).  This maybe specified without a `reference_transcript_id` attribute if the models is not as assigned to a specific transcript within the gene.
  * Other attributes are ignored

All of the attributes specified above must be repeated on all exons of a
transcript with the same value.  An example models submission GTF file is at
[models.gtf](../examples/experts/model_try/models.gtf).

## File naming

Files must be named `xxx.gtf` and maybe compressed with `gzip` and then have a
name in the form `xxx.gtf.gz`.

## Validation

A validation program is provide dfor the annotation GTFs, and the submitter must run this before submitting the file.
