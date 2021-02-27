PYTHON = python3
FLAKE8 = python3 -m flake8


pyprogs = $(shell file -F $$'\t' bin/* | awk '/Python script/{print $$1}')
pypi_url = https://upload.pypi.org/simple/
pypitest_url = https://test.pypi.org/simple/
testenv = testenv

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "install - install the package to the active Python's site-packages"
	@echo "dist - package"
	@echo "test-pip - test install the package using pip"
	@echo "release-test - test upload to pypitest"
	@echo "test-release-pip - install from pypitest"
	@echo "release - package and upload a release"


lint: lint_code lint_doc
lint_code:
	${FLAKE8} ${pyprogs} lib
lint_doc:

test:
	cd tests && ${MAKE} test

clean: test_clean
	rm -rf build/ dist/ ${testenv}/ lib/lrgasp.egg-info/ lib/lrgasp/__pycache__/

test_clean:
	cd tests && ${MAKE} clean

define envsetup
	@rm -rf ${testenv}/
	mkdir -p ${testenv}
	${PYTHON} -m virtualenv --quiet ${testenv}
endef
envact = source ${testenv}/bin/activate

dist: clean
	${PYTHON} setup.py sdist
	${PYTHON} setup.py bdist_wheel
	ls -l dist

# test install locally
test-pip: dist
	${envsetup}
	${envact} && pip install --no-cache-dir dist/lrgasp-*.tar.gz
	${envact} && ${MAKE} test

# test release to pypitest
release-test: dist
	${twine} upload --repository=testpypi dist/lrgasp-*.whl dist/lrgasp-*.tar.gz

# test release install from pypitest
test-release-pip:
	${envsetup}
	${envact} && pip install --no-cache-dir --index-url=${pypitest_url} lrgasp
	${envact} && ${MAKE} test

release: dist
	${twine} upload --repository=pypi dist/lrgasp-*.whl dist/lrgasp-*.tar.gz

