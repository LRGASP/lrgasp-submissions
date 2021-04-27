testrootdir = ..
include ${testrootdir}/testing.mk

debug = --debug

# set to get debug on error test cases
#  err_debug == --debug

entries = iso_detect_ref_ont_drna iso_quant_ont_drna1 iso_detect_de_novo_pb1 iso_quant_pb1
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
bad_quant_tests = $(basename $(notdir $(wildcard input/bad_quant_*.sh)))
bad_de_novo_tests = $(basename $(notdir $(wildcard input/bad_de_novo_*.sh)))

bad_isoform_tests: ${bad_isoform_tests:%=test_%}

test_bad_isoform%: mkout
	rm -rf output/$@
	mkdir output/$@
	cat input/iso_detect_ref_ont_drna.files | (cd ../../examples/darwin_lab && cpio --quiet -pduml ../../tests/complete/output/$@/)
	bash -e input/bad_isoform$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_ref_ont_drna "(should fail)"
	@if ! ${lrgasp_validate_entry} ${err_debug} output/$@/iso_detect_ref_ont_drna 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

bad_quant_tests: ${bad_quant_tests:%=test_%}

test_bad_quant%: mkout
	rm -rf output/$@
	mkdir output/$@
	cat input/iso_quant_ont_drna1.files | (cd ../../examples/darwin_lab && cpio --quiet -pduml ../../tests/complete/output/$@/)
	bash -e input/bad_quant$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_quant_ont_drna1 "(should fail)"
	@if ! ${lrgasp_validate_entry} ${err_debug} output/$@/iso_quant_ont_drna1 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

bad_de_novo_tests: ${bad_de_novo_tests:%=test_%}

test_bad_de_novo%: mkout
	rm -rf output/$@
	mkdir output/$@
	cat input/iso_detect_de_novo_pb1.files | (cd ../../examples/darwin_lab && cpio --quiet -pduml ../../tests/complete/output/$@/)
	bash -e input/bad_de_novo$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_de_novo_pb1 "(should fail)"
	@if ! ${lrgasp_validate_entry} ${err_debug} output/$@/iso_detect_de_novo_pb1 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err


clean:
	rm -rf output

mkout:
	@mkdir -p output
