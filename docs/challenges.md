# Challenges

* Challenge 1: transcript isoform detection with a high-quality genome (`iso_detect_ref`)
  * human and mouse
* Challenge 2: transcript isoform quantification (`iso_quant`)
  * human and mouse
* Challenge 3: de novo transcript isoform detection (`iso_detect_de_novo`)
  * manatee

## Challenge data requirements

A submission to a challenge is an *entry*, consisting of
one or more *experiments*.  Each *entry* must meet the following requirements:

* At least one *experiment* must be supplied for each *sample* available for
  a given challenge.
* The data used for a given *experiment* must fit in one of the following categories:
  * *long-only* - Use only LGRASP-provided long-read RNA-Seq data from a single sample, library preparation method and sequencing platform.
  * *short-only* - Use only LGRASP-provided short-read RNA-Seq data from a single sample, library preparation method and the Illumina platform.
  * *long and short* - Use only LGRASP-provided long-read and short-read RNA-Seq data from a single library preparation method and one long-read platform and the Illumina platform.
  * *kitchen sink* - Any combination of at least one LRGASP data set as well as any other accessioned data in public genomics data repositories

* The type of platform and libraries preparation method used in a given *experiment*, except for *kitchen sink* experiments, is limited to date from a single library preparation method plus sequencing technology.  LRGASP Illumina short-read data of the same sample may optionally be used in an experiment with the LRGASP long-read data
  * Illumina cDNA - *short-only*
  * Pacbio cDNA - *long-only* or *long and short*
  * Pacbio CapTrap - *long-only* or *long and short*
  * ONT cDNA - *long-only* or *long and short*
  * ONT CapTrap - *long-only* or *long and short*
  * ONT R2C2 - *long-only* or *long and short*
  * ONT dRNA - *long-only* or *long and short*

