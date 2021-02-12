lrgasp_validate_expression_matrix = ../../bin/lrgasp-validate-expression-matrix

bad_tsvs = $(wildcard input/bad_*.tsv)
bad_tests = $(basename $(notdir ${bad_tsvs}))

test: test_example test_with_NA bad_tests

test_example:
	${lrgasp_validate_expression_matrix} ../../examples/experts/exp_try/expression-matrix.tsv

test_with_NA:
	${lrgasp_validate_expression_matrix} input/with_NA.tsv

bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgasp_validate_expression_matrix} input/bad$*.tsv  "(should fail)"
	@if ! ${lrgasp_validate_expression_matrix} input/bad$*.tsv 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

clean:
	rm -rf output

mkout:
	@mkdir -p output
