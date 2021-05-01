# Developer support

For developers of this package, not of general interest.

## Files

* [build.md](build.md) - build, test and release instructions
* bin/genSubmitTree - generate plot images for documentation
* bin/editExampleJson - make ad-hoc edits to examples
* bin/buildEncodeMetadata - converts dumps of ENCODE metadata to internal subset
* bin/generateRnaSeqDataMatrix - generates RNA-Seq data matrix from RNA-Seq metadata
* bin/fixLexogenSirvGtf - fix various problems with Lexogen-provided GTF

## Notes:

* using some version use json_pp (perl 2.56) to reformat ENCODE JSON breaks unicode.
  Version perl 2.30 seems to work.
* to build encode-metadata.json
  ./devs/bin/buildEncodeMetadata  --dataset_json=lib/lrgasp/data/encode-metadata.json ../metadata-dumps/*.json
* to generate docs/rnaseq-data-matrix.md from above (run by make doc)
  ./devs/bin/generateRnaSeqDataMatrix
* to generate docs/rnaseq-data-matrix.html from above (run by make doc)
  ./devs/bin/make_html_table.R
  
  
