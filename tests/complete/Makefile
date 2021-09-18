testrootdir = ..
include ${testrootdir}/testing.mk

# debug in expect ok cases
# debug=--logDebug

# debug in expected error cases
# err_debug=--logDebug

# macros to clone examples for destructive tests
define clone_iso_detect_ref_darwin_drna_ont
rm -rf output/$@
mkdir output/$@
(cd ../../examples/darwin_lab && find iso_detect_ref_darwin_drna_ont | cpio --quiet -pduml ../../tests/complete/output/$@/)
endef

define clone_iso_detect_ref_darwin_captrap_ont
rm -rf output/$@
mkdir output/$@
(cd ../../examples/darwin_lab && find iso_detect_ref_darwin_captrap_ont | cpio --quiet -pduml ../../tests/complete/output/$@/)
endef

define clone_iso_quant_drna_ont_darwin
rm -rf output/$@
mkdir output/$@
(cd ../../examples/darwin_lab && find iso_quant_drna_ont_darwin | cpio --quiet -pduml ../../tests/complete/output/$@/)
endef

define clone_iso_detect_de_novo_darwin
rm -rf output/$@
mkdir output/$@
(cd ../../examples/darwin_lab && find iso_detect_de_novo_darwin | cpio --quiet -pduml ../../tests/complete/output/$@/)
endef

define clone_iso_detect_ref_freestyle_darwin
rm -rf output/$@
mkdir output/$@
(cd ../../examples/darwin_lab && find iso_detect_ref_freestyle_darwin | cpio --quiet -pduml ../../tests/complete/output/$@/)
endef

entries = iso_detect_ref_darwin_drna_ont iso_detect_ref_darwin_captrap_ont iso_quant_drna_ont_darwin iso_detect_de_novo_darwin iso_detect_ref_freestyle_darwin

test: entry_tests metadata_only_tests gz_tests bad_tests

##
# full validation of each entry
##
entry_tests: ${entries:%=entry_test_%}

entry_test_%:
	${lrgasp_validate_entry} ${debug} ${darwindir}/$*

##
# only check metadata
##
metadata_only_tests: test_metadata_only_good test_metadata_only_bad

test_metadata_only_good: mkout
	${clone_iso_detect_ref_darwin_drna_ont}
	find output/$@ -type f -not -name '*.json' | xargs rm
	${lrgasp_validate_entry} ${debug} --metadata_only output/$@/iso_detect_ref_darwin_drna_ont/

test_metadata_only_bad: mkout
	${clone_iso_detect_ref_darwin_drna_ont}
	bash -e input/bad_isoform_library_prep_mismatch.sh output/$@
	@echo ${lrgasp_validate_entry} --metadata output/$@/iso_detect_ref_darwin_drna_ont "(should fail)"
	@if ! ${lrgasp_validate_entry} ${err_debug} --metadata output/$@/iso_detect_ref_darwin_drna_ont 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

# compressed tests
gz_tests:  ${entries:%=gz_test_%}

gz_test_%: mkout
	${clone_${*}}
	find output/$@ -type f ! -name '*.json' | xargs gzip -f
	${lrgasp_validate_entry} ${debug} output/$@/$*



# bad entry tests clones examples, using hardlinks, then edits them with script that runs sed.
# Added new edit programs adds new testss.
bad_tests: bad_isoform_tests bad_quant_tests bad_de_novo_tests

bad_isoform_tests = $(basename $(notdir $(wildcard input/bad_isoform_*.sh)))
bad_isoform2_tests = $(basename $(notdir $(wildcard input/bad_isoform2_*.sh)))
bad_quant_tests = $(basename $(notdir $(wildcard input/bad_quant_*.sh)))
bad_de_novo_tests = $(basename $(notdir $(wildcard input/bad_de_novo_*.sh)))

bad_isoform_tests: ${bad_isoform_tests:%=test_%} ${bad_isoform2_tests:%=test_%}

# uses iso_detect_ref_darwin_drna_ont entry
test_bad_isoform_%: mkout
	${clone_iso_detect_ref_darwin_drna_ont}
	bash -e input/bad_isoform_$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_ref_darwin_drna_ont "(should fail)"
	@if ! ${lrgasp_validate_entry} ${err_debug} output/$@/iso_detect_ref_darwin_drna_ont 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

# uses iso_detect_ref_darwin_captrap_ont entry
test_bad_isoform2_%: mkout
	${clone_iso_detect_ref_darwin_captrap_ont}
	bash -e input/bad_isoform2_$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_ref_darwin_captrap_ont "(should fail)"
	@if ! ${lrgasp_validate_entry} ${err_debug} output/$@/iso_detect_ref_darwin_captrap_ont 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

bad_quant_tests: ${bad_quant_tests:%=test_%}

test_bad_quant%: mkout
	${clone_iso_quant_drna_ont_darwin}
	bash -e input/bad_quant$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_quant_drna_ont_darwin "(should fail)"
	@if ! ${lrgasp_validate_entry} ${err_debug} output/$@/iso_quant_drna_ont_darwin 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

bad_de_novo_tests: ${bad_de_novo_tests:%=test_%}

test_bad_de_novo%: mkout
	${clone_iso_detect_de_novo_darwin}
	bash -e input/bad_de_novo$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_de_novo_darwin "(should fail)"
	@if ! ${lrgasp_validate_entry} ${err_debug} output/$@/iso_detect_de_novo_darwin 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err


clean:
	rm -rf output

mkout:
	@mkdir -p output
