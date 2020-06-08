# Transcript expression matrix format

The format required for providing quantification results by the user should be a **tab-separated** matrix in which long read-defined transcripts will be the rows and samples/replicates will be columns.

### Key features

* **Header**: First field must be `ID` and the rest of the column names should be the sample/replicates labels.
* **ID column**: Transcripts should have the same IDs as ones provided in GTF.
* **Quantification values reported**: Any metric is acceptable as long as they correlate with RNA concentration. This can be evaluated using known concentration of SIRVs

Gene expression will be calculated summing up the expression values of all the transcripts coming from the same locus.

### Expression matrix example:

```
ID	sample1	sample2	sample3	 sample4
PB.1.1	49.98	49.22	75.64	60.10
PB.10.1	39.67   42.66   4.74    4.68
PB.10.2	33.08   29.32   5.37    8.42
PB.10.3	0.38    0.77    1.54    1.03
PB.100.1        37.57   36.33   18.97   22.78
PB.1000.1       184.49  157.44  44.97   71.41
PB.1000.3       1.46    1.46    0.43    0.83
PB.1000.4       7.21    7.50    4.95    1.65
PB.1000.5       13.38   14.55   0.33    3.32
PB.1000.6       2.53    6.68    8.29    11.26
PB.1000.7       3.44    2.14    2.31    1.99
PB.1000.9       48.80   66.51   31.94   30.00
PB.1001.1       1044.55 1134.42 382.44  314.14
PB.1002.1       342.16  348.46  148.90  240.40
PB.1002.2       882.45  926.07  575.31  715.36
PB.1003.1       19.04   21.93   30.88   43.33
PB.1003.2       22.54   15.69   76.57   79.59

```
