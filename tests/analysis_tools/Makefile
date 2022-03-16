testrootdir = ..
include ${testrootdir}/testing.mk

test: read_use_tests entries_to_tsv_tests

read_use_tests: test_read_use test_read_use_star test_read_use_sum

test_read_maps = \
	${darwindir}/iso_detect_ref_darwin_captrap_ont/ES_captrap_ont/read_model_map.tsv \
	${darwindir}/iso_detect_ref_darwin_captrap_ont/WTC11_captrap_ont/read_model_map.tsv \
	${darwindir}/iso_detect_ref_darwin_captrap_ont/H1_mix_captrap_ont/read_model_map.tsv

test_read_use: mkout
	${read_model_map_use} --out=output/$@.tsv ${test_read_maps}
	diff expected/$@.tsv output/$@.tsv

test_read_use_star: mkout
	${read_model_map_use} --out=output/$@.tsv input/multi-use.rmm.tsv
	diff expected/$@.tsv output/$@.tsv

test_read_use_sum: mkout
	${read_model_map_use_sum} --out=output/$@.tsv expected/read_use_test.tsv expected/read_use_test.tsv
	diff expected/$@.tsv output/$@.tsv

entries_to_tsv_tests: test_entries_to_tsv

test_entries_to_tsv: mkout
	${lrgasp_entries_to_tsv} ${debug} --out=output/$@.tsv \
		${darwindir}/iso_detect_ref_darwin_captrap_ont/entry.json \
		${darwindir}/iso_detect_de_novo_darwin/entry.json

clean:
	rm -rf output

mkout:
	@mkdir -p output
