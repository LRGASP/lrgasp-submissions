# Documentation for LRGASP organizers

## Development

Running tests set PYTHONPATH and don't require a virtualenv

```
make test
```

## lint

Markdown doc can be linted if the following packages are installed:

* markdownlint (mdl) - Ruby package: ``gem install mdl``
* markdown-link-check - Node.js package: ``npm install -g markdown-link-check`

## Build pip installable packages

To build and test package

```
make test-pip
```

### pypitest

WARNING: commit any changes first
```
bumpversion --allow-dirty --no-commit --no-tag (major|minor|patch)
make release-testpypi
make test-release-testpypi
git reset --hard
```

Note: might have to wait for test-release-testpypi, it seems there might be 
a slight delay in index update.

## Release to pypi

```
bumpversion (major|minor|patch)
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
faSize -detailed ../../lrgasp-data/references/lrgasp_grch38_sirvs.fasta.gz > lib/lrgasp/data/lrgasp_grch38_sirvs.tsvfaSize -detailed ../../lrgasp-data/references/lrgasp_grcm39_sirvs.fasta.gz  > lib/lrgasp/data/lrgasp_grcm39_sirvs.ts```



