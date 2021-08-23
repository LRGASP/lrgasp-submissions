# Documentation for LRGASP organizers

## Development

Running tests set PYTHONPATH and don't require a virtualenv

```
make test
```

## Data matrix

```
  ./devs/bin/getEncodeMetadata ../metadata-dumps/encode-all.json
  ./devs/bin/buildEncodeMetadata  --dataset_json=lib/lrgasp/data/encode-metadata.json ../metadata-dumps/encode-all.json
  make doc
```

If on the UCSC hgwdev system the data matrix is written to
`~/public_html/lrgasp/rnaseq-data-matrix.html`.  To build
data matrix in another directory:
```
  make doc htmldir=the/html/dir
```


## lint

Python can be validated with flake8 using `make lint`

Markdown doc is validated if the following packages are installed:
* markdownlint (mdl) - Ruby package: `gem install mdl`
* markdown-link-check - Node.js package: `npm install -g markdown-link-check`
* LinkChecker - `pip3 install LinkChecker`

Run `make lint-all` to run local lint both source and documentation lint.

To verify the generate web documentation at [https://lrgasp.github.io/lrgasp-submissions/docs/](https://lrgasp.github.io/lrgasp-submissions/docs/),
run `make lint-pages`.

Checking  [https://lrgasp.github.io/lrgasp-submissions/docs/](https://lrgasp.github.io/lrgasp-submissions/docs/)
against the [W3C Link Validator](http://validator.w3.org/) is also useful, as it finds
broken HTML fragment links.  Set `Check linked documents recursively, recursion depth:` to 2.

## Build pip installable packages

Setup your build environment (either global or virtualenv):
```
pip install -r requirements-dev.txt
```

To build and test package

```
make test-pip
```

### make sure data matrix documentation is current

Ensure data matrix documentation is up-to-date:
```
make doc
commit -am 'updated data matrix doc'
```

### pypitest

* WARNING: commit any changes first
* WARNING: [make sure data matrix documentation is current](#make_sure_data_matrix_documentation_is_current)

Test without committing version number:
```
bump2version --allow-dirty --no-commit --no-tag (major|minor|patch)
make release-testpypi
make test-release-testpypi
git reset --hard
```

Note: might have to wait for test-release-testpypi, it seems there might be 
a slight delay in index update.

## Release to pypi


```
bump2version (major|minor|patch)
git push origin --tags
git push
make release
make release-test
```


# Data builds

* 2021-04-18 upload genome fastas to references directory
```
synapse add --parentid syn25536060 lrgasp_sirv4.fasta.gz
synapse add --parentid syn25536060 lrgasp_grch38_sirvs.fasta.gz
synapse add --parentid syn25536060 lrgasp_grcm39_sirvs.fasta.gz
```

```
faSize -detailed ../../lrgasp-data/references/lrgasp_grch38_sirvs.fasta.gz > lib/lrgasp/data/lrgasp_grch38_sirvs.tsvfaSize -detailed ../../lrgasp-data/references/lrgasp_grcm39_sirvs.fasta.gz  > lib/lrgasp/data/lrgasp_grcm39_sirvs.ts
```



