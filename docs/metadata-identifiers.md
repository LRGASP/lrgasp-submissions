# Metadata identifiers

This page describes various identifiers used in the metadata.

## Symbolic identifiers

Various components of the submission system have symbolic identifiers.  These identifiers consist of [ASCII](https://en.wikipedia.org/wiki/ASCII) upper- and lower-case alphabetic characters, numbers, and underscores.  They must not begin with numbers.  In some cases, specific prefixes are required.

## Feature and read identifiers

Feature identifiers (transcripts and genes) and read identifiers may contain any combination of printing, non-whitespace characters [ASCII](https://en.wikipedia.org/wiki/ASCII).  This requirement is more restrictive than allowed by GTF.

## Synapse identifiers

Identifiers assigned by Synapse are in the form ```syn123456``.

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

## Public repository identifiers

The following public data repositories symbols are used to specify where non-LRGASP
data used in experiments has been obtained, as specified in the experiment
[experiment JSON ``extra_libraries`` field](metadata.md#experiment_json).
If another public archive is needed, please create an  issue in the
[LRGASP submissions GitHub tracker](https://github.com/LRGASP/lrgasp-submissions/issues).

* ``SRA`` - [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra/), the SRA and ENA share an accession namespace and are periodically synchronized.  Please use the repository from which you obtained the data.
* ``ENA`` - [EMBL-EBI ENA](https://www.ebi.ac.uk/ena/), the ENA and SRA share an accession namespace and are periodically synchronized.  Please use the repository from which you obtained the data.
* ``INSDC`` - One of the [INSDC](http://www.insdc.org/) database (DBDB, EMBL-EBI/ENA, or NCBI).  These share an accession namespace and are synchronized daily.
* ``ENC`` - [ENCODE DCC](https://www.encodeproject.org/).

## Expression unit identifiers

LRGAPS accepts various expression units.  See
[Renesh Bedre's blog](https://www.reneshbedre.com/blog/expression_units.html)
for a good overview of expression units.

*``RPM`` - reads per million mapped reads
*``RPKM`` - reads per kilobase per million mapped reads
*``FPKM`` - fragments per kilobase per million mapped read
*``TPM`` - transcripts per million
*``counts`` - raw counts
