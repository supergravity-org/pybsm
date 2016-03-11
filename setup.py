#!/usr/bin/env python3

# from distutils.core import setup, find_packages
from setuptools import setup, find_packages
from pybsm.__init__ import __version__
import os.path

with open(os.path.join(os.path.dirname(__file__),
                       'requirements.txt')) as f:
    required = f.read().splitlines()

setup(name='pybsm',
      version=__version__,
      description='BSM-SG ',
      author='Supergravity Foundation',
      author_email='',
      url='https://github.com/supergravity-org/pybsm/',
      packages=find_packages(exclude=["tests"]),
      test_suite='tests',
      setup_requires=[
        'pytest-runner',
        'pytest',
        'pytest-cov',
        'sphinx'
      ],
      test_args=[
        '--cov=pybsm'
      ],
      install_requires=required,
      tests_require=required + [
        'pytest',
        'pylama',
        'pytest-cov',
      ],
      )
