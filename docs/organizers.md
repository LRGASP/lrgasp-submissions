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
make release-test
make test-release-pip
```

## release to pypi
```
bumpversion major|minor|patch
commit to master
git push origin --tags
git push
make release
```

Test release install!!
