# Challenges

* Challenge 1: transcript isoform detection with a high-quality genome (`iso_detect_ref`)
  * Samples
    * `WTC11` (human iPSC cell line)
    * `H1_mix` (human H1 ES cell line mixed with human Definitive Endoderm derived from H1)
    * `ES` (mouse ES cell line)
* Challenge 2: transcript isoform quantification (`iso_quant`)
  * Samples
    * `WTC11` (human iPSC cell line)
    * `H1_mix` (human H1 ES cell line mixed with human Definitive Endoderm derived from H1)
* Challenge 3: de novo transcript isoform detection (`iso_detect_de_novo`)
  * Samples
    * manatee whole blood
    * `ES` (mouse ES cell line)
## Challenge data requirements

A submission to a challenge is an *entry*, consisting of
one or more *experiments*.  Each *entry* must meet the following requirements:

### Requirements for Challenge 1 and 2
* At least one *experiment* must be supplied for each *sample* available for
  a given challenge. Human and mouse samples will have biological replicates that should be used for the entry.
* The data used for a given *experiment* must fit in one of the following categories:
  * *long-only* - Use only LGRASP-provided long-read RNA-Seq data from a single sample, library preparation method and sequencing platform.
  * *short-only* - Use only LGRASP-provided short-read Illumina RNA-Seq data from a single sample, library preparation method. This is to compare with long-read  approaches
  * *long and short* - Use only LGRASP-provided long-read and short-read RNA-Seq data from a single long-read library preparation method and the Illumina platform. Additional accessioned data in public genomics data repositories can also be used. 
  * *kitchen sink* - Any combination of at least one LRGASP data set as well as any other accessioned data in public genomics data repositories. For example, multiple library methods can be combined (e.g. PacBio cDNA + PacBio CapTrap, ONT cDNA + ONT CapTrap+ ONT R2C2+ ONT dRNA, all data, etc.).

In all the above categories, the genome and transcriptome references specified by LRGASP should be used. For the *long and short* and *kitchen sink* category, additional transcriptome references can be used.

Each team can only submit one entry per category.

* The type of platform and libraries preparation method used in a given *experiment*, except for *kitchen sink* experiments, is limited to data from a single library preparation method plus sequencing technology.  LRGASP Illumina short-read data of the same sample may optionally be used in an experiment with the LRGASP long-read data
  * Illumina cDNA - *short-only*
  * Pacbio cDNA - *long-only* or *long and short*
  * Pacbio CapTrap - *long-only* or *long and short*
  * ONT cDNA - *long-only* or *long and short*
  * ONT CapTrap - *long-only* or *long and short*
  * ONT R2C2 - *long-only* or *long and short*
  * ONT dRNA - *long-only* or *long and short*

### Requirements for Challenge 3
* At least one *experiment* must be supplied for each *sample* available for
  a given challenge. Mouse samples will have biological replicates that should be used for the entry.
* The data used for a given *experiment* must fit in one of the following categories:
  * *long-only* - Use only LGRASP-provided long-read RNA-Seq data from a single sample, library preparation method and sequencing platform.
  * *short-only* - Use only LGRASP-provided short-read Illumina RNA-Seq data from a single sample, library preparation method. This is to compare with long-read  approaches
  * *long and short* - Use only LGRASP-provided long-read and short-read RNA-Seq data from a single long-read library preparation method and the Illumina platform. Additional accessioned data in public genomics data repositories can also be used. 
  * *kitchen sink* - Any combination of at least one LRGASP data set as well as any other accessioned data in public genomics data repositories. For example, multiple library methods can be combined (e.g. PacBio cDNA + PacBio CapTrap, ONT cDNA + ONT CapTrap+ ONT R2C2+ ONT dRNA, all data, etc.).
