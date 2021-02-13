# Documentation for LRGASP organizers



## build pip installable packages

To build and test package
```
python3 setup.py build
python3 -m virtualenv env
source env/bin/activate
python3 setup.py install
make test -j 8
```
