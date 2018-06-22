#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='rest-cli',
   version='0.0.1',
   author='Loi Nguyen',
   author_email='loinguyentrung@gmail.com',
   description='A perfect tool for creating restful web services',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/loint/rest-cli",
   packages=find_packages(),
   classifiers=(
      "Programming Language :: Python :: 2",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ),
   install_requires=[
      'pytest',
      'click',
      'mysql-connector-python'
   ],
   scripts=[
      'rest'
   ]
)