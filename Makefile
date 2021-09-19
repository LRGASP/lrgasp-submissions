PYTHON = python3
FLAKE8 = python3 -m flake8
export PYTHONPATH = lib
TWINE = ${PYTHON} -m twine
VULTURE = vulture

pyprogs = $(shell file -F $$'\t' bin/* | awk '/Python script/{print $$1}')
pyotherprogs = $(shell file -F $$'\t' devs/bin/* tests/*/bin/* | awk '/Python script/{print $$1}')
pypi_url = https://upload.pypi.org/simple/
testpypi_url = https://test.pypi.org/simple/
testenv = testenv

version = $(shell PYTHONPATH=lib ${PYTHON} -c "import lrgasp; print(lrgasp.__version__)")

# mdl is an uncommon program to verify markdown
have_mdl = $(shell which mdl >&/dev/null && echo yes || echo no)
have_mdlinkcheck = $(shell which markdown-link-check >&/dev/null && echo yes || echo no)

github_pages_url = https://lrgasp.github.io/lrgasp-submissions/docs/


help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "doc - build various pieces of the doc"
	@echo "lint - check style with flake8"
	@echo "lint-doc - check documentation"
	@echo "lint-all - lint plus lint-doc"
	@echo "lint-pages - lint github pages, must have been pushed first"
	@echo "vulture - find unused code"
	@echo "test - run tests quickly with the default Python"
	@echo "install - install the package to the active Python's site-packages"
	@echo "dist - package"
	@echo "test-pip - test install the package using pip"
	@echo "release-testpypi - test upload to testpypi"
	@echo "test-release-testpypi - install from testpypi"
	@echo "release - package and upload a release"
	@echo "test-release - test final release"


data_matrix_tsv =  docs/rnaseq-data-matrix.tsv
submit_tree_png =  docs/submit_tree.png

# data matrix HTML is only built on hgwdev or if htmldir is set on the commandline
ifeq ($(shell hostname),hgwdev)
    htmldir = ${HOME}/public_html/lrgasp
endif
ifneq (${htmldir},)
    data_matrix_html = ${htmldir}/rnaseq-data-matrix.html
endif
doc: ${data_matrix_tsv} ${data_matrix_html} ${submit_tree_png}


${data_matrix_tsv}: $(wildcard lib/lrgasp/data/*.json) \
	lib/lrgasp/data_sets.py devs/bin/generateRnaSeqDataMatrix
	./devs/bin/generateRnaSeqDataMatrix

${data_matrix_html}: ${data_matrix_tsv} devs/bin/make_html_table.R 
	Rscript devs/bin/make_html_table.R ${data_matrix_html}

${submit_tree_png}: devs/bin/genSubmitTree
	devs/bin/genSubmitTree $@

# edit function also validates format and field names
lint:
	${FLAKE8} ${pyprogs} ${pyotherprogs} lib
	devs/bin/editExampleJson --clean entry templates/entry.json
	devs/bin/editExampleJson --clean experiment templates/experiment.json

# requires the NPM packages:
#   remark-cli remark-lint remark-preset-lint-recommended markdown-link-check


lint-doc:  check-doc-format check-doc-links

lint-all: lint lint-doc

ifeq (${have_mdl},yes)
check-doc-format:
	mdl --style=mdl-style.rb README.md docs
else
check-doc-format:
	@echo "Note: mdl not installed, not linting markdown" >&2
endif

ifeq (${have_mdlinkcheck},yes)
mdfiles = $(wildcard README.md docs/*.md)
check-doc-links: ${mdfiles:%=check-doc-links_%}
check-doc-links_%:
	markdown-link-check --config=markdown-link-check.json $*
check-doc-links_docs/%:
	markdown-link-check --config=markdown-link-check.json docs/$*
else
check-doc-links:
	@echo "Note: markdown-link-check not installed, not checking markdown links" >&2
endif

lint-pages:
	linkchecker ${github_pages_url}

# this gets a lot of false-positive, just use for code cleanup rather than making it
# standard
vulture:
	${VULTURE} ${pyprogs} lib

test:
	cd tests && ${MAKE} test

clean: test_clean
	rm -rf build/ dist/ ${testenv}/ lib/lrgasp_tools.egg-info/ lib/lrgasp/__pycache__/

test_clean:
	cd tests && ${MAKE} clean

define envsetup
	@rm -rf ${testenv}/
	mkdir -p ${testenv}
	${PYTHON} -m venv ${testenv}
endef
envact = source ${testenv}/bin/activate

dist_tar = dist/lrgasp-tools-${version}.tar.gz
dist_whl = dist/lrgasp_tools-${version}-py3-none-any.whl
pkgver_spec = lrgasp-tools==${version}

dist: clean
	${PYTHON} setup.py sdist
	${PYTHON} setup.py bdist_wheel
	@ls -l ${dist_tar}
	@ls -l ${dist_whl}

# test install locally
test-pip: dist
	${envsetup}
	${envact} && cd ${testenv} && pip install --no-cache-dir $(realpath ${dist_tar})
	${envact} && cd tests ${MAKE} test

# test release to testpypi
release-testpypi: dist
	${TWINE} upload --repository=testpypi ${dist_whl} ${dist_tar}

# test release install from testpypi
# for some reason, pip sees lrgasp in lib directory and doesn't install it, so cd to virtualenv
test-release-testpypi:
	${envsetup}
	${envact} && cd ${testenv} && pip install --no-cache-dir --index-url=${testpypi_url} --extra-index-url=https://pypi.org/simple ${pkgver_spec}
	${envact} && cd tests && ${MAKE} test

release: dist
	${TWINE} upload --repository=pypi ${dist_whl} ${dist_tar}

test-release:
	${envsetup}
	${envact} && cd ${testenv} && pip install --no-cache-dir ${pkgver_spec}
	${envact} && cd tests && ${MAKE} test

