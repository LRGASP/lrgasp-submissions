testrootdir = .
include ${testrootdir}/testing.mk

subdirs = models de_novo_rna read_model_map expression_matrix entry_meta experiment_meta complete dev_tools

test: ${subdirs:%=%_test}
%_test:
	cd $* && ${MAKE} test

clean: ${subdirs:%=%_clean}
%_clean:
	cd $* && ${MAKE} clean


