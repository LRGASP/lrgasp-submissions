# Description of LRGASP simulated data

Data was simulated using the following tools:
- [IsoSeqSim](https://github.com/yunhaowang/IsoSeqSim) for Illumina paired-end data
- [Trans-NanoSim](https://github.com/bcgsc/NanoSim) for PacBio CCS data
- [RSEM simulator](http://deweylab.biostat.wisc.edu/rsem/README.html) for ONT cDNA/dRNA data

Transcripts were generated with the same [reference genomes and annotations](reference-genomes.md) 
that are used for the LRGASP challenge. 
Prior to simulation, polyA tails were appended to all transcript sequences, and
artificial novel isoforms were inserted into the reference transcriptome.

PacBio error rate was estimated from the real LRGASP PacBio CCS data and expected to be ~1.6%.
For ONT data default pre-trained models contained in NanoSim package were used. 
Expected error rates are ~16% for ONT cDNA and ~11% ONT dRNA.

Detailed parameters usd for data simulation will remain undisclosed to *all* participants during the entire LRGAPS challenge.

For convenience of the LRGASP challenge participants we created a [simulation wrapper](https://github.com/LRGASP/lrgasp-simulation), which allows to easily 
generate synthetic data with described parameters. Thus, any participant may simulate data and perfrom their
own benchmarks prior to submission. The wrapper is available [here](https://github.com/LRGASP/lrgasp-simulation).