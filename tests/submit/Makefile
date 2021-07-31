testrootdir = ..
include ${testrootdir}/testing.mk

# to run these tests, there must be a file test-conf.json in this directory
# that contains fields needed use test synapse projects.  this should not be
# checked into git.  See doc in lib/lrgasp/synapse_access.py on what is required.

run_upload_entry = ${lrgasp_upload_entry} --test_config_json=test-conf.json ${debug}

upload_proj_name = upload_test
ref_ont_drna_entry = ${darwindir}/iso_detect_ref_ont_drna

define should_fail
 then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
endef

test: upload_tests

upload_tests: test_upload_bad_synid test_upload_ok

test_upload_bad_synid: mkout
	if ! ${run_upload_entry} ${ref_ont_drna_entry} syn123 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

# tests initial and modified upload
test_upload_ok: mkout
	bin/remake-test-project --test_config_json=test-conf.json ${upload_proj_name}
	${run_upload_entry} ${ref_ont_drna_entry} ${upload_proj_name}
	${run_upload_entry} ${ref_ont_drna_entry} ${upload_proj_name}


clean:
	rm -rf output

mkout:
	@mkdir -p output
