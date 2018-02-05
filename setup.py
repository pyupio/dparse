#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import sys

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "packaging",
    "six",
    "pyyaml",
    "pipenv"
]

# make pytest-runner a conditional requirement, per: https://pypi.org/project/pytest-runner/
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup_requirements = [
    # other setup requirements
] + pytest_runner

test_requirements = [
    'pytest',
]

setup(
    name='dparse',
    version='0.2.1',
    description="A parser for Python dependency files",
    long_description=readme + '\n\n' + history,
    author="Jannis Gebauer",
    author_email='ja.geb@me.com',
    url='https://github.com/jayfk/dparse',
    packages=find_packages(include=['dparse']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='dparse',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
