# -*- coding: utf-8 -*-
import os
from re import search

from setuptools import setup, find_packages

def get_requirements(reqfile):
    with open(reqfile) as f:
        return f.read().splitlines()

extras = {
    "testing": get_requirements('requirements/requirements.test.txt')
}

setup(
    name='pipelines',
    version='0.0.1',
    description='Manage kubeflow pipelines.',
    license='Apache License 2.0',

    packages=find_packages(),
    install_requires=get_requirements('requirements/requirements.txt'),
    extras_require=extras,

    author='Miguel Figueira Ferraz',
    author_email='mferraz@cpqd.com.br',
    url='https://github.com/platiagro/pipelines',
)
