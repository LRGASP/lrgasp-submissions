* version 1.2.0
  - added option to lrgasp-validate-entry to skip data validation and only check metadata for consistency
  - lrgasp-validate-expression-matrix takes optional models GTF as an option rather than a optional positional

* version 1.1.0 2021-08-16
  - Renamed kitchen_sink data category to freestyle.
  - Clarified definition of entry to be consistent with the intended organization of the challenges.
    Multiple entries using different data categories may be submitted to a given challenge.
  - Add samples, library_prep, and platforms to entry.json and experiment.json
    to make them explicit rather than implicit from the files used.
  
* version 1.0.0 2021-08-09
  - Add commands and instructions for submitting to synapse.
