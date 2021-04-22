testrootdir = ..
include ${testrootdir}/testing.mk

devs_bin = ${rootdir}/devs/bin

test: fixSirvGtfTest


fixSirvGtfTest: mkout
	${devs_bin}/fixLexogenSirvGtf input/problem_sirv.gtf output/$@.gtf
	diff expected/$@.gtf output/$@.gtf

clean:
	rm -rf output

mkout:
	@mkdir -p output
