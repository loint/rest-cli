.PHONY: all test

all:
	python setup.py build

install:
	python setup.py install

test:
	pytest

clean:
	rm -rf rest.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .pytest_cache