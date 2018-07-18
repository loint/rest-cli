.PHONY: all test

all:
	python setup.py build

install:
	python setup.py install

test:
	pytest -vx

clean:
	rm -rf rest_cli.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .pytest_cache