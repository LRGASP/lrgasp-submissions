lrgaspValidateGtf = ../../bin/lrgaspValidateGtf

bad_gtfs = $(wildcard input/bad*.gtf)
bad_tests = $(basename $(notdir ${bad_gtfs}))

test: test_example bad_tests

test_example:
	${lrgaspValidateGtf} ../../examples/models.gtf 

bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgaspValidateGtf} input/bad$*.gtf  "(should fail)"
	@if ! ${lrgaspValidateGtf} input/bad$*.gtf 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

clean:
	rm -rf output

mkout:
	@mkdir -p output
