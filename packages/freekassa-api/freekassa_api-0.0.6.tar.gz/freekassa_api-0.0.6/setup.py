#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent


def get_description():
    with open(BASE_DIR / 'README.md') as f:
        return f.read()


def get_requirements():
    with open(BASE_DIR / 'requirements.txt') as reqs:
        return [r.strip() for r in reqs]


setup(
    name='freekassa_api',
    version='0.0.6',
    url='https://github.com/LDmitriy7/freekassa_api.git',

    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    install_requires=[
        'certifi==2021.10.8',
        'charset-normalizer==2.0.9',
        'idna==3.3',
        'pydantic==1.8.2',
        'requests==2.26.0',
        'typing-extensions==4.0.1',
        'urllib3==1.26.7',
    ],

    license='MIT',
    author='LDmitriy7',
    author_email='ldm.work2019@gmail.com',

    description='Freekassa API',
    long_description=get_description(),
)
