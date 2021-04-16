# Reference genomes and transcript annotations

## Genome References

#### Spike-in sequences

Spike-ins are from the [Lexogne SIRV Set 4](https://www.lexogen.com/wp-content/uploads/2020/07/SIRV_Set4_Sequences_200709a.zip),
consisting of both ERCCs and SIRVs.  Ploy(A) tails are removed from the
sequences to form genomic sequences and they are included in the reference
genomes as individual sequences.  For multi-exon SIRVs, a single sequence is
included converting all isoforms of the gene, as well as introns.

The spike-in genomic sequences are available from [sirvs4.fasta.gz](syn2FIXME).

### GRCh38-based human reference genome

* [lrgasp_grch38_sirvs.fasta.gz](syn25536103)
* UCSC style names
* excludes alt-locus sequences and includes SIRVs
* compressed with bgzip for indexing with samtools
* composed of:
  * GRCh38 without alts: [ENCSR425FOI GRCh38_no_alt_analysis_set_GCA_000001405](https://www.encodeproject.org/files/GRCh38_no_alt_analysis_set_GCA_000001405.15/@@download/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta.gz)
  * includes the spike-in genomic sequences.

### GRCm39 based mouse

* [lrgasp_grcm39_sirvs.faata.gz](syn0FIXME)
* UCSC style names
* compressed with bgzip for indexing with samtools
* composed of:
  * GRCm39: [mm39.fa.gz](https://hgdownload.soe.ucsc.edu/goldenPath/mm39/bigZips/mm39.fa.gz)
  * includes the spike-in genomic sequences.

## Transcriptome References

### GENCODE V38 human 

* [lrgasp-gencode-v38.gtf.gz](syn0FIXME)
* composed of:

* mouse
  * composed of:
    * GENCODE-VM28
    * spike-ins 1: FIXME: needed
    * spike-ins 2: FIXME: needed
