testrootdir = ..
include ${testrootdir}/testing.mk

team_meta = input/team.json
mods = mod_ont_drna1 mod_ont_drna2 mod_pb1 mod_pb2
exps = exp_ont_drna1 exp_ont_drna2 exp_pb1 exp_pb2
exprs = ${mod} ${exps}

test: test_team \
	${exprs:%=test_expr_meta_%} \
	${mods:%=test_gtf_%} \
	${mods:%=test_map_%} \
	${exprs:%=test_expression_%} \

test_team: input/team.json
	${lrgasp_validate_team_metadata} $<

test_expr_meta_%:
	${lrgasp_validate_experiment_metadata} input/$*/experiment.json

test_gtf_%:
	${lrgasp_validate_gtf} input/$*/transcript_models.gtf

test_map_%:
	${lrgasp_validate_read_model_map} input/$*/reads_transcript_map.tsv

test_expression_%:
	${lrgasp_validate_expression_matrix} input/$*/expression.tsv

clean:
	rm -rf output

mkout:
	@mkdir -p output
