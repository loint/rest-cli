.PHONY: all test

all:
	python setup.py build

install:
	python setup.py install

test:
	pytest