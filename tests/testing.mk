# include with
#   testrootdir = ../..
#   include ${testrootdir}/testing.mk

rootdir=${testrootdir}/..
libdir=${rootdir}/lib
bindir=${rootdir}/bin

ifeq (${VIRTUAL_ENV},)
  export PYTHONPATH=${libdir}
  binpre = ${bindir}/
else
  binpre = 
endif

lrgasp_validate_gtf = ${binpre}lrgasp-validate-gtf
lrgasp_validate_read_model_map = ${binpre}lrgasp-validate-read-model-map
lrgasp_validate_expression_matrix = ${binpre}lrgasp-validate-expression-matrix
lrgasp_validate_team_metadata = ${binpre}lrgasp-validate-team-metadata
lrgasp_validate_experiment_metadata = ${binpre}lrgasp-validate-experiment-metadata
