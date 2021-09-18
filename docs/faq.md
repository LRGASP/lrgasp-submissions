# FAQ: Frequently asked questions

## How do I submit predictions for the LRGASP challenges?

- Register on [Synapse](https://www.synapse.org/#!Synapse:syn25007472/wiki/608702) for the challenge
- Read the [documentation](https://lrgasp.github.io/lrgasp-submissions/) for challenge and submission instructions

## I would like to submit a Challenge 1 entry for the "long-only" category from PacBio sequencing? Can you clarify how many files and for which samples would be included in the entry?

You should select the challenge, data category, library prep, and sequencing platform, and then submit predictions for all samples that fit that selection criteria (See [Challenges](https://lrgasp.github.io/lrgasp-submissions/docs/challenges.html) for more details). In almost all cases, there are multiple replicates per sample; however only one GTF should be returned for each sample. Different pipelines may treat replicates differently: for example the data could be combined or replicate information used to determine high-confidence transcripts. That will be up to the submitter.

For this inquiry, it would be important to also specify the library prep as the CapTrap method was also sequenced with PacBio. Let's assume the selection is "Challenge 1, long-reads only, cDNA, PacBio". A helpful way to know which samples are included for this is to use the [HTML table](https://hgwdev.gi.ucsc.edu/~markd/lrgasp/rnaseq-data-matrix.html) of the LRGASP data to search for the samples.

On the HTML table, you can input a "1" to filter the "challenges" column, "cdna" to filter the "library_prep" column, and "pacbio" to filter the "platform" column. We also have this data matrix in [TSV format](https://lrgasp.github.io/lrgasp-submissions/docs/rnaseq-data-matrix.tsv) to help with programmatic selection.

These selections give the following samples that are used for Challenge 1 with a cDNA prep, sequenced on PacBio.

- human WTC11 (three biological replicates. biosample IDs: ENCBS944CBA; ENCBS593PKA; ENCBS474NOC)
- human H1_mix (three biological replicates of a cell line mixture, biosample IDs: ENCBS464AKI,ENCBS664DSZ; ENCBS012DYC,ENCBS872CFG; ENCBS667PZC,ENCBS971DDS)
- human human_simulation (one replicate). Synthetic data can be found with the associated Synapse ID syn25591693 through our [Synapse](https://www.synapse.org/LRGASP) page
- mouse ES (three biological replicates. biosample IDs: ENCBS648HXY; ENCBS951CRC; ENCBS418RDP)
- mouse mouse_simulation (one replicate). syn25591622

We want to make sure we collect simulated and real data results from each computational pipeline and we would like to ensure that tools are robust to different organisms.

So in this scenario, you would be submitting five GTF files and five corresponding read map files for each of the five samples. This page gives an overview of the file structure for the submission that would contain subfolders for each of these samples: [https://lrgasp.github.io/lrgasp-submissions/docs/submission.html](https://lrgasp.github.io/lrgasp-submissions/docs/submission.html).

## I notice some libraries have multiple files. I also notice other oddities of the data. Are these known issues?

- Please visit our [known issues](https://lrgasp.github.io/lrgasp-submissions/docs/known-issues.html) page, which highlights known issues or answers common questions about the LRGASP data.
