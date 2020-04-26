#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "packaging",
    "pyyaml",
    "toml",
]

setup(
    name='dparse',
    version='0.5.2a',
    description="A parser for Python dependency files",
    long_description=readme + '\n\n' + history,
    author="Jannis Gebauer",
    author_email='support@pyup.io',
    url='https://github.com/pyupio/dparse',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires=">=3.5",
    extras_require={
        'pipenv':  ["pipenv"],
    }
)
