testrootdir = .
include ${testrootdir}/testing.mk

subdirs = models read_model_map expression_matrix entry_meta experiment_meta complete

test: ${subdirs:%=%_test}
%_test:
	cd $* && ${MAKE} test

clean: ${subdirs:%=%_clean}
%_clean:
	cd $* && ${MAKE} clean


