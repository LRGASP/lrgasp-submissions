# Documentation for LRGASP organizers

## Development

Running test set PYTHONPATH and don't require a virtualenv

```
make test
```

## Build pip installable packages

To build and test package

```
make test-pip
```

### pypitest

```
bumpversion --allow-dirty --no-commit --no-tag major|minor|patch
make release-testpypi
make test-release-testpypi
```

## Release to pypi

```
bumpversion major|minor|patch
git push origin --tags
git push
make release
make release-test
```


