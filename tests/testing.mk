# include with
#   testrootdir = ../..
#   include ${testrootdir}/testing.mk

rootdir=${testrootdir}/..
libdir=${rootdir}/lib
bindir=${rootdir}/bin

# disable builtin stuff
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

exampledir = ${rootdir}/examples
darwindir = ${exampledir}/darwin_lab

ifeq (${VIRTUAL_ENV},)
  export PYTHONPATH=${libdir}
  binpre = ${bindir}/
else
  binpre = 
endif

# pick up GNU sed with macports
ifeq ($(shell uname -s), Darwin)
   PATH := /opt/local/libexec/gnubin:${PATH}
   export PATH
   $(warning @@@@ ${PATH})
endif

lrgasp_validate_de_novo_rna = ${binpre}lrgasp-validate-de-novo-rna
lrgasp_validate_models = ${binpre}lrgasp-validate-models
lrgasp_validate_read_model_map = ${binpre}lrgasp-validate-read-model-map
lrgasp_validate_expression_matrix = ${binpre}lrgasp-validate-expression-matrix
lrgasp_validate_entry_metadata = ${binpre}lrgasp-validate-entry-metadata
lrgasp_validate_experiment_metadata = ${binpre}lrgasp-validate-experiment-metadata
lrgasp_validate_entry = ${binpre}lrgasp-validate-entry
lrgasp_upload_entry = ${binpre}lrgasp-upload-entry
lrgasp_synapse_download = ${binpre}lrgasp-synapse-download
