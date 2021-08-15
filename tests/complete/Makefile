testrootdir = ..
include ${testrootdir}/testing.mk

# to get error logging, run with
# make debug=--logDebug

entries = iso_detect_ref_darwin_drna_ont iso_detect_ref_darwin_captrap_ont iso_quant_drna_ont_darwin iso_detect_de_novo_darwin iso_detect_ref_freestyle_darwin
test: entry_tests bad_tests

##
# full validation of each entry
##
entry_tests: ${entries:%=entry_test_%}

entry_test_%:
	${lrgasp_validate_entry} ${debug} ${darwindir}/$*

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
	rm -rf output/$@
	mkdir output/$@
	(cd ../../examples/darwin_lab && find iso_detect_ref_darwin_drna_ont | cpio --quiet -pduml ../../tests/complete/output/$@/)
	bash -e input/bad_isoform_$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_ref_darwin_drna_ont "(should fail)"
	@if ! ${lrgasp_validate_entry} ${debug} output/$@/iso_detect_ref_darwin_drna_ont 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

# uses iso_detect_ref_darwin_captrap_ont entry
test_bad_isoform2_%: mkout
	rm -rf output/$@
	mkdir output/$@
	(cd ../../examples/darwin_lab && find iso_detect_ref_darwin_captrap_ont | cpio --quiet -pduml ../../tests/complete/output/$@/)
	bash -e input/bad_isoform2_$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_ref_darwin_captrap_ont "(should fail)"
	@if ! ${lrgasp_validate_entry} ${debug} output/$@/iso_detect_ref_darwin_captrap_ont 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

bad_quant_tests: ${bad_quant_tests:%=test_%}

test_bad_quant%: mkout
	rm -rf output/$@
	mkdir output/$@
	(cd ../../examples/darwin_lab && find iso_quant_drna_ont_darwin | cpio --quiet -pduml ../../tests/complete/output/$@/)
	bash -e input/bad_quant$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_quant_drna_ont_darwin "(should fail)"
	@if ! ${lrgasp_validate_entry} ${debug} output/$@/iso_quant_drna_ont_darwin 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

bad_de_novo_tests: ${bad_de_novo_tests:%=test_%}

test_bad_de_novo%: mkout
	rm -rf output/$@
	mkdir output/$@
	(cd ../../examples/darwin_lab && find iso_detect_de_novo_darwin | cpio --quiet -pduml ../../tests/complete/output/$@/)
	bash -e input/bad_de_novo$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_de_novo_darwin "(should fail)"
	@if ! ${lrgasp_validate_entry} ${debug} output/$@/iso_detect_de_novo_darwin 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err


clean:
	rm -rf output

mkout:
	@mkdir -p output
