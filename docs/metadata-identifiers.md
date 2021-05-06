# Metadata identifiers

This page describes various identifiers used in the metadata.

## Symbolic identifiers

Various components of the submission system have symbolic identifiers.  These identifiers consist of [ASCII](https://en.wikipedia.org/wiki/ASCII) upper- and lower-case alphabetic characters, numbers, and underscores.  They must not begin with numbers.  In some cases, specific prefixes are required.

## Feature and read identifiers

Feature identifiers (transcripts and genes) and read identifiers may contain any combination of printing, non-whitespace characters [ASCII](https://en.wikipedia.org/wiki/ASCII).  This requirement is more restrictive than allowed by GTF.

## Synapse identifiers

Identifiers assigned by Synapse are in the form ```syn123456``.

## Challenge identifiers

* ``iso_detect_ref`` - Challenge 1: transcript isoform detection with a high-quality genome
* ``iso_quant`` - Challenge 2: transcript isoform quantification
* ``iso_detect_de_novo`` - Challenge 3: de novo transcript isoform detection

## Species identifiers

* ``human`` - taxon 9606
* ``mouse`` - taxon 10090
* ``manatee`` - taxon 127582
* ``synthetic`` - generated synthetic reads

## Sample identifiers

* ``WTC11`` - human WTC11 iPSC cell line
* ``H1_mix`` - human H1 ES cell line mixed with human Definitive Endoderm derived from H1
* ``ES`` - mouse Castaneus X S129/SvJae F121-9 ES cell line
* ``Manatee`` - manatee whole blood

## Experiment data categories

They following symbols identify the data category to which the experiment belongs:

* ``long-only`` - uses only LGRASP-provided long-read RNA-Seq data from a single sample, library preparation method and sequencing platform.
* ``short-only`` - uses only LGRASP-provided short-read Illumina RNA-Seq data from a single sample. This is to compare with long-read  approaches.
* ``long and short`` - uses only LGRASP-provided long-read and short-read RNA-Seq data from a single long-read library preparation method and the Illumina platform. Additional accessioned data in public genomics data repositories can also be used.
* ``kitchen sink`` - any combination of at least one LRGASP data set as well as any other accessioned data in public genomics data repositories. For example, multiple library methods can be combined (e.g. PacBio cDNA + PacBio CapTrap, ONT cDNA + ONT CapTrap+ ONT R2C2+ ONT dRNA, all data, etc.).  LRGASP simulated reads may not be used in *kitchen sink* experiments.

## Public repository identifiers

The following public data repositories symbols are used to specify where non-LRGASP
data used in experiments has been obtained, as specified in the experiment
[experiment JSON ``extra_libraries`` field](metadata.md#experimentjson).
If another public archive is needed, please create an  issue in the
[LRGASP submissions GitHub tracker](https://github.com/LRGASP/lrgasp-submissions/issues).

* ``SRA`` - [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra/), the SRA and ENA share an accession namespace and are periodically synchronized.  Please use the repository from which you obtained the data.
* ``ENA`` - [EMBL-EBI ENA](https://www.ebi.ac.uk/ena/), the ENA and SRA share an accession namespace and are periodically synchronized.  Please use the repository from which you obtained the data.
* ``INSDC`` - One of the [INSDC](http://www.insdc.org/) database (DBDB, EMBL-EBI/ENA, or NCBI).  These share an accession namespace and are synchronized daily.
* ``ENC`` - [ENCODE DCC](https://www.encodeproject.org/).

