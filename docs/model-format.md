# Transcript model format

## GTF format

Genome transcript annotation submissions are in GTF format
(see [GTF2.2](https://mblab.wustl.edu/GTF22.html)
and [Ensembl GFF/GTF File Format](https://www.ensembl.org/info/website/upload/gff.html)).

Model files must be gzip-compressed and named ```models.gtf.gz```.

Only `exon` features are used, and exons of a given transcript are linked together by the `transcript_id` attribute.  Gaps of at least XX bases between exons are assumed
to be introns.  Smaller gaps are closed, combining the exon features.  The evaluation ignores other features
that are provided. However, they will still be validated for syntax and consistency.

The standard GTF fields have the following restrictions:

* seqname - Must be one of the sequence identifiers in the LRGAPS [reference genomes](reference-genomes.md).
* source - Ignored.
* feature - Only `exon` is used. Other types of records are ignored.
* start - Standard, one-based start position.
* end - Standard, one-based end position.
* score - Ignored.
* strand - Must be specified as `+`, `-` or `.` on `exon` features. Other feature types may be validated.
* frame - Should be `.` on `exon` features, but not valid. Other feature types may be validated but are not required.
* attributes:
  * `transcript_id` - Required for all `exon` features and assigned by the submitter.
  * `gene_id` - Required for all `exon` features.  While not evaluated by LRGASP, it is unclear if GTF requires this. Some tools, such as the UCSC Genome Browser and command-line tools, will fail without `gene_id`.  The assigned `gene_id` does not have to represent an actual gene. However, it must not reflect impossible genes, such as those on different chromosomes.  If gene assignment is not supported, it is suggested that each transcript is assigned its own `gene_id`, which may be the same as the `transcript_id`.
  * `reference_transcript_id` - Optional, used to indicate the transcript is a reference call for the specified [reference transcript](reference-genomes.md).
  * `reference_gene_id` - Optional, used to indicate the gene is a reference call for the specified [reference gene](reference-genomes.md).  This attribute is used without a `reference_transcript_id` attribute if the models are not assigned to a specific transcript ofthe gene.
  * Other attributes are ignored

All of the attributes specified above must be repeated on all exons of a
transcript with the same value.  An example models submission GTF file is at
[models.gtf](../examples/darwin_lab/iso_detect_ref_ont_drna/H1_mix_drna_ont_long/models.gtf).
