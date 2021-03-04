testrootdir = ..
include ${testrootdir}/testing.mk

debug = --debug

entries = iso_detect_ref_ont_drna iso_quant_ont_drna1 iso_detect_de_novo_pb1 iso_quant_pb1
test: test_entry_meta test_entries test_bad_entries

##
# check metadata files
##
test_entry_meta: ${entries:%=test_entry_meta_%}

test_entry_meta_%:
	${MAKE} test_entry_meta entry=$*

ifneq (${entry},)
# recursive target: entry=
test_entry_meta: test_entry_meta_${entry} \
	test_models \
	test_quants

test_entry_meta_%:
	${lrgasp_validate_entry_metadata} ${debug} ${darwindir}/$*/entry.json

# recurse over models
model_exprs = $(notdir $(wildcard ${darwindir}/${entry}/model_*))
test_models: ${model_exprs:%=test_models_%}

test_models_%:
	${MAKE} test_model entry=${entry} model=$*

ifeq (${model},)
# recursive target: entry= model=
test_model: test_model_meta test_gtf test_model_map

test_model_meta:
	${lrgasp_validate_experiment_metadata} ${debug} ${darwindir}/${entry}/${model}/experiment.json

test_gtf:
	${lrgasp_validate_gtf} ${debug} ${darwindir}/${entry}/${model}/models.gtf

test_model_map:
	${lrgasp_validate_read_model_map} ${debug} ${darwindir}/${entry}/${model}/read_model_map.tsv

# recurse over expression
quant_exprs = $(notdir $(wildcard ${darwindir}/${entry}/quant_*))
test_quants: ${quant_exprs:%=test_quants_%}

test_quants_%:
	${MAKE} test_quant entry=${entry} exp=$*

# recursive target: entry= exp=
test_quant: test_quant_meta test_express_matrix

test_quant_meta:
	${lrgasp_validate_experiment_metadata} ${debug} ${darwindir}/${entry}/${exp}/experiment.json

test_express_matrix:
	${lrgasp_validate_expression_matrix} ${debug} ${darwindir}/${entry}/${exp}/expression.tsv
endif
endif

##
# full validation of each entry
##
test_entries: ${entries:%=test_%_entry}

test_%_entry:
	${lrgasp_validate_entry} ${debug} ${darwindir}/$*

# bad entry tests clones examples, using hardlinks, then edits them with script that runs sed.
# Added new edit programs adds new testss.
test_bad_entries: test_bad_isoforms test_bad_quants


bad_isoform_tests = $(basename $(notdir $(wildcard input/bad_isoform_*.sh)))
bad_quant_tests = $(basename $(notdir $(wildcard input/bad_quant_*.sh)))

test_bad_isoforms: ${bad_isoform_tests:%=test_%}

test_bad_isoform%: mkout
	mkdir output/$@
	cat input/iso_detect_ref_ont_drna.files | (cd ../../examples/darwin_lab | cpio -pduml ../tests/complete/output/$@/)
	bash input/bad_isoform$*.sh output/$@
	@echo ${lrgasp_validate_entry} output/$@/iso_detect_ref_ont_drna "(should fail)"
	diff expected/$@.err output/$@.err



clean:
	rm -rf output

mkout:
	@mkdir -p output
