testrootdir = .
include ${testrootdir}/testing.mk

subdirs = gtf read_model_map expression_matrix team_meta experiment_meta entries

test: ${subdirs:%=%_test}
%_test:
	cd $* && ${MAKE} test

clean: ${subdirs:%=%_clean}
%_clean:
	cd $* && ${MAKE} clean


