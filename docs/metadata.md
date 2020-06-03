# Metadata submission format

Metadata files are in [JSON](https://www.json.org/json-en.html) format.  JSON
provides a good compromise between able to store structured data and easy of
use.  Templates and a validator are provided.  The metadata is contained in a
directory `metadata` in the submission.  All of the below files are required.

## ``submitter.json``
This file contains information about the submitting group.  This must accompany
each submission, even if unchanged. 
See [``submitter.json``](../examples/metadata/submitter.json) for an example.
An empty template is also available: [``submitter.json``](../templates/submitter.json).

* ``submitter_id`` - symbolic name for the submitter, assigned when the user registers for LRGASP.  This will be a valid Python-style identifier names.
* ``group_name`` - name of the submitting lab
* ``group_url`` - URL of the submitting lab page (optional)
* ``notes`` - notes (optional)
* ``contacts`` - array of contacts, with the first entry considered the primary contact
  * ``name`` - name of the contact
  * ``email`` - e-mail of the contact, which can be an e-mail list
  * ``notes`` - notes about the contact (optional)
* ``submit_time`` - time file was received (add by LRGASP submission)

## ``submission.json``
This describes the submission, specifying all data files.  Data files are assumed
to be in a directory ``data``, that is adjacent to the ``metadata`` directory
containing this file.
See [``submission.json``](../examples/metadata/submission.json) for an example.
An empty template is also available: [``submission.json``](../templates/submission.json).

* ``submitter_id`` - must match the ``submitter_id`` in ``submitter.json``.
* ``submission_id`` - submitter-define identifier, unique to that submitter and must be a valid Python-style identifier
* ``description`` - description of submission
* ``notes`` - notes (optional)
* ``model_results`` - if this submission contains annotation models, this a results sections defined below.
  This will describe files conforming to the [Genome annotation submission format specification](annotation-format.md).
* ``expression_results`` - if this submission contains expression, this a results sections defined below.
  This will describe files conforming to the [Transcript expression matrix submission format specification](expression_matrix_format.md)
* ``submit_time`` - time submission was received (add by LRGASP submission).
  
### Results sections
Both model and expression results use the same basic set of fields, with some
field or values only applicable to a certain types of results.

* ``analysis_id`` - submitter-define identifier, unique to that submitter and must be a valid Python-style identifier
* ``description`` - description of analysis
* ``technology`` - sequencing technology, one of ``PacBio`` or ``ONT``.
* ``protocol`` - library preparation protocol, values will be defined later
* ``samples`` - list of sample names
* ``notes`` - notes about software or how it was used (optional)
* ``results`` - list of files in ``data`` directory
  * ``fname`` - name of file (without directory), compressed with required extensions
  * ``ftype`` - type of file: ``GTF``, ``expressionMatrix``
  * ``md5`` - md5 sum of file, as a hexadecimal string (standard output from ``md5sum`` command)
  * ``units`` - Expression units for expression results: ``RPM``, ``RPKM``, ``FPKM``,or ``TPM``.
  * ``notes`` - notes about software or how it was used (optional)
* ``software`` - list of software used in pipeline:
  * ``name`` - name of software package
  * ``description`` - description of software (optional)
  * ``version`` - version of software
  * ``url``  - URL to software repository
  * ``notes`` - notes about software or how it was used (optional)

## Open issues
- How is a submission structure?  Can multiple model and expression results both be include in a single submission?
  should only type be allowed?
- How are updates and multiple version to both metadata and data handled?
- Do we require a specific naming convection for submitted files or just drive it off of metadata?
  Ridged encoding metadata in file names can be problematic, such as find an error in metadata or differing by a parameter not encode in the name.
