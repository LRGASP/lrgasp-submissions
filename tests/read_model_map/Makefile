lrgasp_validate_read_model_map = ../../bin/lrgasp-validate-read-model-map

bad_tsvs = $(wildcard input/bad*.tsv)
bad_tests = $(basename $(notdir ${bad_tsvs}))

test: test_example bad_tests

test_example:
	${lrgasp_validate_read_model_map} ../../examples/read_model_map.tsv

bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgasp_validate_read_model_map} input/bad$*.tsv  "(should fail)"
	@if ! ${lrgasp_validate_read_model_map} input/bad$*.tsv 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

clean:
	rm -rf output

mkout:
	@mkdir -p output
