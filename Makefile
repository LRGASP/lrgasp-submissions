PYTHON = python3
FLAKE8 = python3 -m flake8


pyprogs = $(shell file -F $$'\t' bin/* | awk '/Python script/{print $$1}')

subdirs = tests

all:

lint:
	${FLAKE8} ${pyprogs} lib

test: ${subdirs:%=%_test}
%_test:
	cd $* && ${MAKE} test

clean: ${subdirs:%=%_clean}
	rm -rf build lib/lrgasp.egg-info
%_clean:
	cd $* && ${MAKE} clean


