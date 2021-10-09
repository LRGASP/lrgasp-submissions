* version 1.9.0
   - fixed bug generating error message
   - Ugly workaround problem validated long_short entries when the short samples have
     do not have all of the library preps used by the long samples.  Really hard to fix
     with current metadata structure, so change error to a warning for this case.
   
* version 1.8.0
   - Handle comma-separated sample headers in the expression matrix when multiple files are used as input
     in a given expression level estimate.
    
* version 1.7.0
   - It was discovered that the Synapse ids for the simulated data in the
     data matrix were for the staging project, not the released Synapse ids.
     The validation rules have been change to allow use of either the staging
     or released synapse ids.
   
* version 1.6.0
  - add ability to have``lrgasp-upload-entry`` upload multiple entries in one call.  Note that this changes the order of the arguments.
  - add ability to specify a sub-directory of a project to``lrgasp-upload-entry`` 
  
* version 1.5.0
  - disallow strand of `.` in GTF files, as validation tools can not handle unspecified strand.

* version 1.4.0
  - allow R2C2_subreads format library files
  - add instructions to change Synapse project to allow download by "LRGASP Evaluators"

* version 1.3.0
  - fixed but with validating full entry containing compressed data files
  - remove term_id field from metadata.  This id is no longer easy to find
    in the Synapse UI.  Instead, use team_name field.
  - document that team_name field should have user name, if not submitting as a team.

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
