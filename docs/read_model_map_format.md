# Read to transcript model map format

This describes the submission format for mapping the initial reads to the final transcript model,

In order to understand better how each pipeline deals differently with the same initial input, it will be asked to the participants to submit a **.tsv file** that relates the starting point (the reads provided by LRGASP) to their final transcript models. This file will have two columns:
* ``read_id`` It will contain the ID of the "raw" sequence and it must be as it is in the initial FASTQ file.
* ``transcript_id`` It will show the ID of the transcript model built using the read in the previous column. The transcript ID must be as it is in the GTF submitted by the participant. 

If a read is not used at all to generate any transcript model, it may be show in its second column a `*`. However, we should check if all the read IDs present in the initial FASTQ file are included or not in this *read-model* file.

##### Example
Here the first column are the IDs of the reads in the [FASTQ rep1](https://www.encodeproject.org/files/ENCFF450VAU/@@download/ENCFF450VAU.fastq.gz) of ENCODE pilot data set. It is just an example, the relations between ccs read and transcript models are "made up".

```
read_id	transcript_id
m54284U_191110_105540/6/ccs     ENCODEHT000595433
m54284U_191110_105540/8/ccs     ENST00000329251.4
m54284U_191110_105540/9/ccs     ENST00000392222.6
m54284U_191110_105540/13/ccs    ENCODEHT000420932
m54284U_191110_105540/18/ccs    ENCODEHT000260030
m54284U_191110_105540/19/ccs    ENST00000336023.9
m54284U_191110_105540/21/ccs    ENST00000468812.5
m54284U_191110_105540/33/ccs    ENST00000234590.10
m54284U_191110_105540/35/ccs    ENST00000398598.7
m54284U_191110_105540/41/ccs    ENST00000392246.6
m54284U_191110_105540/49/ccs    ENST00000238561.9
m54284U_191110_105540/50/ccs    ENST00000558083.2
m54284U_191110_105540/54/ccs    ENST00000216146.8
m54284U_191110_105540/56/ccs    ENST00000374479.3
m54284U_191110_105540/57/ccs    ENST00000301821.10
m54284U_191110_105540/59/ccs    *
m54284U_191110_105540/60/ccs    ENST00000247655.3
```

There is not any limitation about reporting one single read linked to several transcript models, and vice versa. However, it is still unclear how this might be evaluated (or even if it should be evaluated).

Additionally, participants may want to submit a BED12 format in which they map the initial sequences to the reference genome. To provide or not this information is up to the submitters, because this might be a bit complicated with some pipelines.
