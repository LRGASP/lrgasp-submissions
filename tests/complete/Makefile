testrootdir = ..
include ${testrootdir}/testing.mk

entries = ont_drna_model_finished ont_drna_expression pb_model_draft pb_expression
test: test_entries

##
# check metadata files
##
test_entries: ${entries:%=test_entries_%}

test_entries_%:
	${MAKE} test_entry entry=$*

# recursive target: entry=
test_entry: test_entry_${entry} \
	test_models \
	test_quants

test_entry_%:
	${lrgasp_validate_entry_metadata} input/$*/entry.json

# recurse over models
model_exprs = $(notdir $(wildcard input/${entry}/model_*))
test_models: ${model_exprs:%=test_models_%}

test_models_%:
	${MAKE} test_model entry=${entry} model=$*

# recursive target: entry= model=
test_model: test_model_meta test_gtf test_model_map

test_model_meta:
	${lrgasp_validate_experiment_metadata} input/${entry}/${model}/experiment.json

test_gtf:
	${lrgasp_validate_gtf} input/${entry}/${model}/transcript_models.gtf

test_model_map:
	${lrgasp_validate_read_model_map} input/${entry}/${model}/reads_transcript_map.tsv

# recurse over expression
quant_exprs = $(notdir $(wildcard input/${entry}/quant_*))
test_quants: ${quant_exprs:%=test_quants_%}

test_quants_%:
	${MAKE} test_quant entry=${entry} exp=$*

# recursive target: entry= exp=
test_quant: test_quant_meta test_express_matrix

test_quant_meta:
	${lrgasp_validate_experiment_metadata} input/${entry}/${exp}/experiment.json

test_express_matrix:
	${lrgasp_validate_expression_matrix} input/${entry}/${exp}/expression.tsv

clean:
	rm -rf output

mkout:
	@mkdir -p output
