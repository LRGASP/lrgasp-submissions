testrootdir = ..
include ${testrootdir}/testing.mk

debug = --debug
err_debug =  # --debug to get debug in expected error cases

bad_jsons = $(wildcard input/bad_*.json)
bad_tests = $(basename $(notdir ${bad_jsons}))

good_jsons = $(wildcard input/good_*.json)
good_tests = $(basename $(notdir ${good_jsons}))

test: iso_detect_ref_tests iso_quant_tests bad_tests good_tests

iso_detect_ref_tests: $(addsuffix _iso_detect_ref_test,$(dir $(wildcard ${darwindir}/iso_detect_ref_*/*/experiment.json)))

%_iso_detect_ref_test: mkout
	${lrgasp_validate_experiment_metadata} ${debug} $*/experiment.json

iso_quant_tests: $(addsuffix _iso_quant_test,$(dir $(wildcard ${darwindir}/iso_quant_*/*/experiment.json)))

%_iso_quant_test: mkout
	${lrgasp_validate_experiment_metadata} ${debug} $*/experiment.json

bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgasp_validate_experiment_metadata} input/bad$*.json  "(should fail)"
	@if ! ${lrgasp_validate_experiment_metadata} ${err_debug} input/bad$*.json 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

good_tests: ${good_tests:%=test_%}

test_good%: mkout
	${lrgasp_validate_experiment_metadata} ${debug} input/good$*.json

clean:
	rm -rf output

mkout:
	@mkdir -p output
