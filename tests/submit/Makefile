testrootdir = ..
include ${testrootdir}/testing.mk

# to run these tests, there must be a file test-conf.json in this directory
# that contains fields needed use test synapse projects from
# test-conf-template.json This should not be checked into git.  See doc in
# lib/lrgasp/synapse_access.py on what is required.

run_upload_entry = ${lrgasp_upload_entry} --test_config_json=test-conf.json ${debug}
run_download = ${lrgasp_synapse_download} --test_config_json=test-conf.json ${debug}

ref_ont_drna_entry = ${darwindir}/iso_detect_ref_darwin_drna_ont
upload_proj_name = 'LRPLAYER Submit'

.PHONEY: test
ifeq ($(wildcard test-conf.json),)
test:
	@echo 'WARNING submit/test-conf.json DOES NOT EXIST, SYNAPSE TESTS SKIPPED' >&2
else
test: upload_tests
endif

upload_tests: test_upload_bad_name test_upload_ok

test_upload_bad_name: mkout
	if ! ${run_upload_entry} ${ref_ont_drna_entry} fred 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

##
# tests initial upload
##

# function to link input tree, less .emacs.bak files
link_entry = (cd ${darwindir} && find iso_detect_ref_darwin_drna_ont | fgrep -v .emacs.bak | cpio --quiet -pduml ../../tests/submit/$(1))

# clean entry
test_upload_ok: mkout
	rm -rf output/$@.*
	# copy test data
	$(call link_entry,output/$@.up/)
	# remove existing synapse data
	bin/clean-test-project --test_config_json=test-conf.json ${upload_proj_name}
	# upload, download, and compare
	${run_upload_entry} output/$@.up/iso_detect_ref_darwin_drna_ont ${upload_proj_name}
	${run_download} ${upload_proj_name}/iso_detect_ref_darwin_drna_ont output/$@.down
	diff -r output/$@.up output/$@.down


clean:
	rm -rf output

mkout:
	@mkdir -p output
