testrootdir = ..
include ${testrootdir}/testing.mk

# debug in expect ok cases
# debug=--logDebug

# debug in expected error cases
# err_debug=--logDebug

bad_jsons = $(wildcard input/bad_*.json)
bad_tests = $(basename $(notdir ${bad_jsons}))

good_jsons = $(wildcard input/good_*.json)
good_tests = $(basename $(notdir ${good_jsons}))

example_exprs = $(wildcard ${darwindir}/*/*/experiment.json)

test: example_tests bad_tests good_tests

example_tests: ${example_exprs:%=example_test/%}

example_test/%: mkout
	${lrgasp_validate_experiment_metadata} ${debug} $*

bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgasp_validate_experiment_metadata} input/bad$*.json  "(should fail)"
	@if ! ${lrgasp_validate_experiment_metadata} ${err_debug} input/bad$*.json 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

good_tests: ${good_tests:%=test_%}

test_good%: mkout
	${lrgasp_validate_experiment_metadata} ${debug} input/good$*.json

clean:
	rm -rf output

mkout:
	@mkdir -p output
