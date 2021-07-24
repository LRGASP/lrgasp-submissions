# Known Issues
* Replicate 3 of the H1_mix sample appears to be an outlier among the CapTrap ONT library type. This was identified by looking at concordance between expected 5' and 3' adapter sequences and the strandedness (directionality) of minimap2-aligned spliced reads by looking at splice site sequences.
* Replicate 3 of the H1 mix has two paired-end fastq files for the Illumina library type. These should be combined in analyses, as they come from the same mix of biosamples.
