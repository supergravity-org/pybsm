#!/usr/bin/env python3

# from distutils.core import setup, find_packages
from setuptools import setup, find_packages

setup(name='pybsm',
      version='0.1',
      description='BSM-SG ',
      author='Supergravity Foundation',
      author_email='',
      url='https://github.com/supergravity-org/pybsm/',
      packages=find_packages(),
      test_suite='tests',
      setup_requires=[
        'pytest-runner',
        'cached_property'
      ],
      tests_require=[
        'pytest',
        'pylama'
      ],
      )
