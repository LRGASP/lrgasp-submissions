lrgasp_validate_gtf = ../../bin/lrgasp-validate-gtf

bad_gtfs = $(wildcard input/bad_*.gtf)
bad_tests = $(basename $(notdir ${bad_gtfs}))

test: test_example bad_tests

test_example:
	${lrgasp_validate_gtf} ../../examples/models.gtf 

bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgasp_validate_gtf} input/bad$*.gtf  "(should fail)"
	@if ! ${lrgasp_validate_gtf} input/bad$*.gtf 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

clean:
	rm -rf output

mkout:
	@mkdir -p output
