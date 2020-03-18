# -*- coding: utf-8 -*-
import os
from re import search

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
NAME = 'pipelines'

with open('pipelines/__init__.py', 'rt', encoding='utf8') as f:
    VERSION = search(r'__version__ = "(.*?)"', f.read()).group(1)

DESCRIPTION = 'Manage kubeflow pipelines.'

with open(os.path.join(HERE, 'README.md'), 'rt', encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

def get_requirements(reqfile):
    path = os.path.join(HERE, reqfile)
    with open(path) as f:
        return f.read().splitlines()

extras = {
    "testing": get_requirements('requirements/requirements.test.txt')
}

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',

    packages=find_packages(),
    install_requires=get_requirements('requirements/requirements.txt'),
    extras_require=extras,

    author='Miguel Figueira Ferraz',
    author_email='mferraz@cpqd.com.br',
    url='https://github.com/platiagro/pipelines',
)
