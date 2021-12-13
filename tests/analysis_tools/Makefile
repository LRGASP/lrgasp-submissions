testrootdir = ..
include ${testrootdir}/testing.mk

test: read_use_test read_use_sum_test

test_read_maps = \
	${darwindir}/iso_detect_ref_darwin_captrap_ont/ES_captrap_ont/read_model_map.tsv \
	${darwindir}/iso_detect_ref_darwin_captrap_ont/WTC11_captrap_ont/read_model_map.tsv \
	${darwindir}/iso_detect_ref_darwin_captrap_ont/H1_mix_captrap_ont/read_model_map.tsv \
	${darwindir}/iso_detect_ref_darwin_drna_ont/H1_mix_drna_ont/read_model_map.tsv \
	${darwindir}/iso_detect_ref_darwin_drna_ont/WTC11_drna_ont/read_model_map.tsv

read_use_test: mkout
	${read_model_map_use} --out=output/$@.tsv ${test_read_maps}
	diff expected/$@.tsv output/$@.tsv

read_use_sum_test: mkout
	${read_model_map_use_sum} --out=output/$@.tsv expected/read_use_test.tsv expected/read_use_test.tsv
	diff expected/$@.tsv output/$@.tsv

clean:
	rm -rf output

mkout:
	@mkdir -p output
