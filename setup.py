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
    "tomli; python_version < '3.11'",
]

setup(
    name='dparse',
    version='0.6.2',
    description="A parser for Python dependency files",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
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
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires=">=3.6",
    extras_require={
        'pipenv': ["pipenv<=2022.12.19"],
        'conda': ["pyyaml"]
    }
)
