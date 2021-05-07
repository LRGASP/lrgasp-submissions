# Transcript expression matrix format

The format required for providing quantification results by the user should be a **tab-separated** matrix in which long read-defined transcripts will be the rows and biological replicates will be columns.

Expression matrix files must be gzip-compressed and named ```expression.tsv.gz```.

## Key features

* **Header**: The first field must be `ID`, and the rest of the column names should be the replicate labels.
* **ID column**: Transcripts should have the same IDs as ones provided in GTF, and must be a conforming [feature identifier](metadata-identifiers.md#feature-and-read-identifiers).
* **Replicates**: Should refer to the Biosample ID of the biological replicate or the file accession. This can be found in the [RNA-Seq Data Matrix](rnaseq-data-matrix.md)
* **Quantification values reported**: Units must be TPM, `NA` values are allowed when no expression is observed.

Gene expression will be calculated by summing up all the transcripts' expression values coming from the same locus.

## Expression matrix example

```
ID	rep1	rep2	rep3
PB.1.1	49.98	49.22	75.64
PB.10.1	39.67   42.66   4.74
PB.10.2	33.08   29.32   5.37
PB.10.3	0.38    0.77    1.54
PB.100.1        37.57   36.33   18.97
PB.1000.1       184.49  157.44  44.97
PB.1000.3       1.46    1.46    0.43
PB.1000.4       7.21    7.50    4.95
PB.1000.5       13.38   14.55   0.33
PB.1000.6       2.53    6.68    8.29
PB.1000.7       3.44    2.14    2.31
PB.1000.9       48.80   66.51   31.94
PB.1001.1       1044.55 1134.42 382.44
PB.1002.1       342.16  348.46  148.90
PB.1002.2       882.45  926.07  575.31
PB.1003.1       19.04   21.93   30.88
PB.1003.2       22.54   15.69   76.57

```
