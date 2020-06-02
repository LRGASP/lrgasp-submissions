PYTHON = python3
FLAKE8 = python3 -m flake8


pyprogs = $(shell file -F $$'\t' bin/* | awk '/Python script/{print $$1}')


all:


lint:
	${FLAKE8} ${pyprogs}
