#!/usr/bin/env python

from setuptools import setup

setup(
  name = 'labqr',
  version = '0.1',
  packages = ['labqr'],
  entry_points = {'console_scripts': ['labqr=labqr:main']}
)
