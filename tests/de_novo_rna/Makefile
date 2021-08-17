testrootdir = ..
include ${testrootdir}/testing.mk

debug = --logDebug
err_debug =  # --logDebug to get debug in error cases

bad_fastas = $(wildcard input/bad_*.fasta)
bad_tests = $(basename $(notdir ${bad_fastas}))

good_fastas = $(wildcard input/good_*.fasta)
good_tests = $(basename $(notdir ${good_fastas}))

test:  bad_tests good_tests compressed_tests

bad_tests: ${bad_tests:%=test_%}

test_bad%: mkout
	@echo ${lrgasp_validate_de_novo_rna} input/bad$*.fasta  "(should fail)"
	@if ! ${lrgasp_validate_de_novo_rna} ${err_debug} input/bad$*.fasta 2>output/$@.err ; ${should_fail}
	diff expected/$@.err output/$@.err

good_tests: ${good_tests:%=test_%}

test_good%: mkout
	${lrgasp_validate_de_novo_rna} ${debug} input/good$*.fasta

compressed_tests: compressed_test

compressed_test: mkout
	gzip -c input/good_rna.fasta > output/$@.fasta.gz
	${lrgasp_validate_de_novo_rna} ${debug} --rna_ids=output/$@.ids output/$@.fasta.gz
	diff expected/$@.ids output/$@.ids

clean:
	rm -rf output

mkout:
	@mkdir -p output
