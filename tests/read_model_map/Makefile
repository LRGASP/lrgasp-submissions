testrootdir = ..
include ${testrootdir}/testing.mk

bad_tsvs = $(wildcard input/bad_*.tsv)
bad_tests = $(basename $(notdir ${bad_tsvs}))

good_tsvs = $(wildcard input/good_*.tsv)
good_tests = $(basename $(notdir ${good_tsvs}))

test: test_ref_example test_de_novo_example test_example_gz bad_tests good_tests

ref_example_dir = ${darwindir}/iso_detect_ref_ont_drna/WTC11_drna_ont_long
test_ref_example:
	${lrgasp_validate_read_model_map} ${ref_example_dir}/read_model_map.tsv --model_gtf=${ref_example_dir}/models.gtf

de_novo_example_dir = ${darwindir}/iso_detect_de_novo_pb/pbManteeBlood
test_de_novo_example:
	${lrgasp_validate_read_model_map} ${de_novo_example_dir}/read_model_map.tsv --rna_fasta=${de_novo_example_dir}/rna.fasta

test_example_gz: output/read_model_map.tsv.gz
	${lrgasp_validate_read_model_map} $<

output/read_model_map.tsv.gz: ${darwindir}/iso_detect_ref_ont_drna/WTC11_drna_ont_long/read_model_map.tsv
	@mkdir -p output	
	gzip -c $< >$@


bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgasp_validate_read_model_map} input/bad$*.tsv  "(should fail)"
	@if ! ${lrgasp_validate_read_model_map} input/bad$*.tsv 2>output/$@.err ; then exit 0 ; else echo Error Test $@ should have failed >&2; exit 1 ; fi
	diff expected/$@.err output/$@.err

good_tests: ${good_tests:%=test_%}

test_good%: mkout
	${lrgasp_validate_read_model_map} input/good$*.tsv --model_gtf=input/good$*.gtf

clean:
	rm -rf output

mkout:
	@mkdir -p output
