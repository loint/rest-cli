#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
   name='rest',
   version='1.0',
   description='',
   author='Loi Nguyen',
   author_email='loinguyentrung@gmail.com',
   packages=find_packages(),
   install_requires=[
      'click',
      'mysql-connector-python'
   ],
   scripts=[
        'rest'
   ]
)