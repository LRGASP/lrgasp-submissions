testrootdir = ..
include ${testrootdir}/testing.mk

bad_jsons = $(wildcard input/bad_*.json)
bad_tests = $(basename $(notdir ${bad_jsons}))

good_jsons = $(wildcard input/good_*.json)
good_tests = $(basename $(notdir ${good_jsons}))

test: test_model_example test_quant_example bad_tests good_tests

test_model_example:
	${lrgasp_validate_experiment_metadata} ${exampledir}/our_entry/model_try/experiment.json

test_quant_example:
	${lrgasp_validate_experiment_metadata} ${exampledir}/our_entry/quant_try/experiment.json

bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgasp_validate_experiment_metadata} input/bad$*.json  "(should fail)"
	@if ! ${lrgasp_validate_experiment_metadata} input/bad$*.json 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

good_tests: ${good_tests:%=test_%}

test_good%: mkout
	${lrgasp_validate_experiment_metadata} input/good$*.json

clean:
	rm -rf output

mkout:
	@mkdir -p output
