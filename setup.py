#!/usr/bin/env python
'''
setup.py
'''

import os
import re
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

HERE = os.path.abspath(os.path.dirname(__file__))
NAME = 'pipeline-generator'
with open('pipeline/__init__.py', 'rt', encoding='utf8') as f:
    VERSION = re.search(r'__version__ = "(.*?)"', f.read()).group(1)
DESCRIPTION = 'Generate kubeflow pipelines.'
with open(os.path.join(HERE, 'README.md'), 'rt', encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Miguel Figueira Ferraz',
    url='https://github.com/platiagro/pipeline-generator',
    packages=find_packages('pipeline'),
    package_dir={'': 'pipeline'},
    license='Apache License 2.0',
    install_requires=requirements
)
