# Reference genomes and transcript annotations

## Genome References

#### Spike-in sequences

Spike-ins are from the [Lexogne SIRV Set 4](https://www.lexogen.com/wp-content/uploads/2020/07/SIRV_Set4_Sequences_200709a.zip),
consisting of both ERCCs and SIRVs.  Ploy(A) tails are removed from the
sequences to form genomic sequences and they are included in the reference
genomes as individual sequences.  For multi-exon SIRVs, a single sequence is
included converting all isoforms of the gene, as well as introns.

The spike-in genomic sequences are available from [sirvs4.fasta.gz](syn2FIXME)
with the annotations in GTF format [sirvs4.gtf.gz](syn3FIXME).

### GRCh38-based human reference genome

* [lrgasp_grch38_sirvs.fasta.gz](syn25536103)
* UCSC style names
* excludes alt-locus sequences
* includes ERCC/SIRV spike-in genomic sequences
* FASTA format compressed with bgzip for indexing with samtools
* based on GRCh38 without alts: [ENCSR425FOI GRCh38_no_alt_analysis_set_GCA_000001405](https://www.encodeproject.org/files/GRCh38_no_alt_analysis_set_GCA_000001405.15/@@download/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta.gz)

### GRCm39 based mouse

* [lrgasp_grcm39_sirvs.fasta.gz](syn0FIXME)
* UCSC style names
* includes ERCC/SIRV spike-in genomic sequences
* FASTA format compressed with bgzip for indexing with samtools
* based on [GRCm39 mm39.fa.gz](https://hgdownload.soe.ucsc.edu/goldenPath/mm39/bigZips/mm39.fa.gz)

## Transcriptome References

### GENCODE V38-based human annotation set

* [lrgasp-gencode-v38.gtf.gz](syn0FIXME)
* [GTF format](https://uswest.ensembl.org/info/website/upload/gff.html)
* excludes alt-locus sequences
* includes ERCC/SIRV spike-in annotations
* based on [gencode.v37.chr_patch_hapl_scaff.annotation.gtf.gz](ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_37/gencode.v37.chr_patch_hapl_scaff.annotation.gtf.gz) with alts loci sequence removed

### GENCODE VM27-based mouse annotation set

* [lrgasp-gencode-vm27.gtf.gz](syn0FIXME)
* [GTF format](https://uswest.ensembl.org/info/website/upload/gff.html)
* includes ERCC/SIRV spike-in annotations
* based on [gencode.vm27.chr_patch_hapl_scaff.annotation.gtf.gz](ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M26/gencode.vM27.chr_patch_hapl_scaff.annotation.gtf.gz)

