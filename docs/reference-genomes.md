# Reference genomes and transcript annotations

Reference genomes and annotations are stored on Synapse.
To download directly file directly to a server, we recommend using the
[Synapse command line](https://docs.synapse.org/articles/tutorial-download-data-portal.html#command-line).

## Genome References

### Spike-in sequences

Spike-ins are from the [Lexogen SIRV Set 4](https://www.lexogen.com/wp-content/uploads/2020/07/SIRV_Set4_Sequences_200709a.zip),
consisting of both ERCCs and SIRVs.  Poly(A) tails are removed from the
sequences to form genomic sequences and they are included in the reference
genomes as individual sequences.  For multi-exon SIRVs, a single sequence is
included converting all isoforms of the gene, as well as introns.

The SIRVs GTF has been edit to modify gene ids so that there are no genes with transcripts on
non-overlapping strands or genes not joined by any transcript.

The spike-in genomic sequences are available from [lrgasp_sirvs4.fasta.gz (syn25683367)](https://www.synapse.org/#!Synapse:syn25683367)
with the annotations in GTF format [lrgasp_sirvs4.gtf.gz (syn25683630)](https://www.synapse.org/#!Synapse:syn25683630).

### GRCh38-based human reference genome

* [lrgasp_grch38_sirvs.fasta.gz (syn25683364)](https://www.synapse.org/#!Synapse:syn25683364)
* UCSC/ENCODE/GENCODE style names
* excludes alt-locus sequences
* includes ERCC/SIRV spike-in genomic sequences
* FASTA format compressed with bgzip for indexing with samtools
* based on GRCh38 without alts: [ENCSR425FOI GRCh38_no_alt_analysis_set_GCA_000001405](https://www.encodeproject.org/files/GRCh38_no_alt_analysis_set_GCA_000001405.15/@@download/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta.gz)

### GRCm39 based mouse

* [lrgasp_grcm39_sirvs.fasta.gz (syn25683365)](https://www.synapse.org/#!Synapse:syn25683365)
* UCSC/ENCODE/GENCODE style names
* includes ERCC/SIRV spike-in genomic sequences
* FASTA format compressed with bgzip for indexing with samtools
* based on [GRCm39 mm39.fa.gz](https://hgdownload.soe.ucsc.edu/goldenPath/mm39/bigZips/mm39.fa.gz)

### De novo ONT-based manatee genome

* [lrgasp_manatee_sirv1.fasta.gz (syn25683366)](https://www.synapse.org/#!Synapse:syn25683366)
* *De novo* assembly at the contig level of manatee genome using ONT sequencing.
* includes ERCC/SIRV spike-in genomic sequences
* FASTA format compressed with bgzip for indexing with samtools
* genomic material used came from the same individual (Lorelei) that was sequenced by the Broad Institute in 2012 for the [current reference genome of the manatee](https://www.ncbi.nlm.nih.gov/assembly/GCF_000243295.1/).

## Transcriptome References

### GENCODE V38-based human annotation set

* [lrgasp_gencode_v38_sirvs.gtf.gz (syn25683628)](https://www.synapse.org/#!Synapse:syn25683628)
* UCSC/ENCODE/GENCODE style names
* includes ERCC/SIRV spike-in annotations
* excludes alt-locus and patch sequences
* [GTF format](https://www.ensembl.org/info/website/upload/gff.html)
* based on [gencode.v38.annotation.gtf.gz](http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_38/gencode.v38.annotation.gtf.gz)

### GENCODE VM27-based mouse annotation set

* [lrgasp_gencode_vM27_sirvs.gtf.gz (syn25683629)](https://www.synapse.org/#!Synapse:syn25683629)
* UCSC/ENCODE/GENCODE style names
* includes ERCC/SIRV spike-in annotations
* excludes patch sequences
* [GTF format](https://www.ensembl.org/info/website/upload/gff.html)
* base on [gencode.vM27.annotation.gtf.gz](http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M27/gencode.vM27.annotation.gtf.gz)


