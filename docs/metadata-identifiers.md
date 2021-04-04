# Types of identifiers

## Symbolic identifiers

Various components of the submission system have symbolic identifiers.  These identifiers consist of [ASCII](https://en.wikipedia.org/wiki/ASCII) upper- and lower-case alphabetic characters, numbers, and underscores.  They must not begin with numbers.  In some cases, specific prefixes are required.

## Feature and read identifiers

Feature identifiers (transcripts and genes) and read identifiers may contain any combination of printing, non-whitespace characters [ASCII](https://en.wikipedia.org/wiki/ASCII).  This requirement is more restrictive than allowed by GTF.

## Synapse identifiers

Identifiers assigned by Synapse are in the form ```syn123456``.

## LRGASP challenge identifiers

* ``iso_detect_ref`` - challenge 1: transcript isoform detection with a high-quality reference genome
* ``iso_quant`` - challenge 2: transcript isoform quantification
* ``iso_detect_de_novo`` - challenge 3: de-novo transcript isoform detection without a reference genome.

## Species identifiers
* ``hs`` - human
* ``mm`` - mouse
* ``manatee`` - manatee

## Experiment data categories
* ``long_only`` - long read only, allowing for two replicates from same sample and library preparation method.
* ``long_short`` - long read as with ``long_only`` with the addition of LRGASP Illumina cDNA of the same sample.
* ``kitchen_sink`` - any combination of data, both LRGASP libraries and external, public data.

## Sample identifiers

* ``WTC11`` - human IPS cell line
* ``H1_mix`` - human H1 and DE cell lines
* ``ES`` - mouse ES cells
* ``Manatee`` - manatee

## Public repository identifiers

The following public data repositories symbols are used to specify where non-LRGASP
data used in experiments has been obtained, as specified in the experiment
[experiment JSON ``extra_libraries`` field](metadata.md#experiment_json).
If another public archive is needed, please create an  issue in the
[LRGASP submissions github tracker](https://github.com/LRGASP/lrgasp-submissions/issues).

* ``SRA`` - [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra/), the SRA and ENA share an accession name space and are periodically synchronized.  Please use the repository from which you obtained the data.
* ``ENA`` - [EMBL-EBI ENA](https://www.ebi.ac.uk/ena/), the ENA and SRA share an accession name space and are periodically synchronized.  Please use the repository from which you obtained the data.
* ``INSDC`` - One of the [INSDC](http://www.insdc.org/) database (DBDB, EMBL-EBI/ENA, or NCBI).  These  share an accession name space and are synchronized daily.
* ``ENC`` - [ENCODE DCC](https://www.encodeproject.org/).


## Expression unit identifiers
Various expression units accepted by LRGAPS.  See 
[Renesh Bedre's blog](https://www.reneshbedre.com/blog/expression_units.html)
for a good overview of expression units.

*``RPM`` - reads per million mapped reads
*``RPKM`` - reads per kilo base per million mapped reads
*``FPKM`` - fragments per kilo base per million mapped read
*``TPM`` - transcripts per million
*``counts`` - raw counts
