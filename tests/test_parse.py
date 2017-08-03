#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""Tests for `dparse.parser`"""

from packaging.specifiers import SpecifierSet

from dparse.parser import parse, Parser
from dparse import filetypes


def test_dockerfile_from():
    content = "ARG CODE_VERSION=99.88.77\n" \
              "ARG FLAVOR=alpine\n" \
              "ARG INV_==A=LID\n" \
              "FROM postgres\n" \
                "FROM postgres as mysql\n" \
              "FROM postgres:9.2\n" \
              "FROM postgres:9.3-alpine\n" \
              "FROM postgres:alpine\n" \
              "FROM postgres:latest\n" \
              "FROM postgres:9.2 as mysql\n" \
              "FROM postgres:9.3-alpine as mysql\n" \
              "FROM postgres:alpine as mysql\n" \
              "FROM postgres:latest as mysql\n" \
              "FROM postgres:${CODE_VERSION}\n" \
              "FROM postgres:${CODE_VERSION}-alpine\n" \
              "FROM postgres:${FLAVOR}-latest\n" \
              "FROM postgres:${CODE_VERSION} as mysql\n" \
              "FROM postgres:${CODE_VERSION}-alpine as mysql\n" \
              "FROM postgres:${FLAVOR}-latest as mysql\n" \
              "FROM postgres@1234567"

    dep_file = parse(content, file_type=filetypes.dockerfile)

    # FROM postgres
    dep = dep_file.dependencies[0]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet()

    assert dep.extras['as'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is True

    # FROM postgres as mysql
    dep = dep_file.dependencies[1]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet()

    assert dep.extras['as'] == "mysql"
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is True

    # FROM postgres:9.2
    dep = dep_file.dependencies[2]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==9.2')

    assert dep.extras['as'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is False

    # FROM postgres:9.3-alpine
    dep = dep_file.dependencies[3]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==9.3')

    assert dep.extras['as'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] == "alpine"
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is False

    # FROM postgres:alpine
    dep = dep_file.dependencies[4]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet()

    assert dep.extras['as'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] == "alpine"
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is True

    # FROM postgres:latest
    dep = dep_file.dependencies[5]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet()

    assert dep.extras['as'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is True

    # FROM postgres:9.2 as mysql
    dep = dep_file.dependencies[6]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==9.2')

    assert dep.extras['as'] == 'mysql'
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is False

    # FROM postgres:9.3-alpine as mysql
    dep = dep_file.dependencies[7]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==9.3')

    assert dep.extras['as'] == 'mysql'
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] == 'alpine'
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is False

    # FROM postgres:alpine as mysql
    dep = dep_file.dependencies[8]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet()

    assert dep.extras['as'] == 'mysql'
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] == 'alpine'
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is True

    # FROM postgres:latest as mysql
    dep = dep_file.dependencies[9]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet()

    assert dep.extras['as'] == 'mysql'
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is True

    # FROM postgres:${CODE_VERSION}
    dep = dep_file.dependencies[10]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==99.88.77')

    assert dep.extras['as'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is False

    # FROM postgres:${CODE_VERSION}-alpine
    dep = dep_file.dependencies[11]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==99.88.77')

    assert dep.extras['as'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] == 'alpine'
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is False

    # FROM postgres:${FLAVOR}-latest
    dep = dep_file.dependencies[12]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet()

    assert dep.extras['as'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] == 'alpine'
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is True

    # FROM postgres:${CODE_VERSION} as mysql
    dep = dep_file.dependencies[13]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==99.88.77')

    assert dep.extras['as'] == 'mysql'
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] is None
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is False

    # FROM postgres:${CODE_VERSION}-alpine as mysql
    dep = dep_file.dependencies[14]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==99.88.77')

    assert dep.extras['as'] == 'mysql'
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] == 'alpine'
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is False

    # FROM postgres:${FLAVOR}-latest as mysql
    dep = dep_file.dependencies[15]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet()

    assert dep.extras['as'] == 'mysql'
    assert dep.extras['digest'] is None
    assert dep.extras['flavor'] == 'alpine'
    assert dep.extras['digest'] is None
    assert dep.extras['latest'] is True

    # FROM postgres@1234567
    dep = dep_file.dependencies[16]
    assert dep.name == "postgres"
    assert dep.specs == SpecifierSet('==@1234567')

    assert dep.extras['as'] is None
    assert dep.extras['digest'] == '1234567'
    assert dep.extras['flavor'] is None
    assert dep.extras['latest'] is False


def test_requirements_with_invalid_requirement():

    content = "in=vali===d{}{}{"
    dep_file = parse(content, file_type=filetypes.requirements_txt)
    assert len(dep_file.dependencies) == 0


def test_tox_ini_with_invalid_requirement():

    content = "[testenv]" \
              "passenv = CI TRAVIS TRAVIS_*" \
              "setenv =" \
              "PYTHONPATH = {toxinidir}" \
              "deps =" \
              "-r{toxinidir}/requirements_dev.txt" \
              "pytest-cov" \
              "codecov"
    dep_file = parse(content, file_type=filetypes.tox_ini)
    assert len(dep_file.dependencies) == 0


def test_conda_file_with_invalid_requirement():

    content = "name: my_env\n" \
              "dependencies:\n" \
              "  - gevent=1.2.1\n" \
              "  - pip:\n" \
              "    - in=vali===d{}{}{"
    dep_file = parse(content, file_type=filetypes.conda_yml)
    assert len(dep_file.dependencies) == 0


def test_conda_file_invalid_yml():

    content = "wawth:dda : awd:\ndlll"
    dep_file = parse(content, file_type=filetypes.conda_yml)
    assert dep_file.dependencies == []


def test_conda_file_marked_line():
    content = "name: my_env\n" \
              "dependencies:\n" \
              "  - gevent=1.2.1\n" \
              "  - pip:\n" \
              "    - beautifulsoup4==1.2.3\n # naaah, marked"
    dep_file = parse(content, file_type=filetypes.conda_yml)
    assert len(dep_file.dependencies) == 1

    dep_file = parse(content, file_type=filetypes.conda_yml, marker=((), "naah, marked"))
    assert len(dep_file.dependencies) == 0


def test_tox_ini_marked_line():
    content = "[testenv:bandit]\n" \
              "commands =\n" \
              "\tbandit --ini setup.cfg -ii -l --recursive project_directory\n" \
              "deps =\n" \
              "\tbandit==1.4.0 # naaah, marked\n" \
              "\n" \
              "[testenv:manifest]\n" \
              "commands =\n" \
              "\tcheck-manifest --verbose\n"

    dep_file = parse(content, "tox.ini")
    assert len(dep_file.dependencies) == 1

    dep_file = parse(content, "tox.ini", marker=((), "naah, marked"))
    assert len(dep_file.dependencies) == 0


def test_resolve_file():
    line = "-r req.txt"
    assert Parser.resolve_file("/", line) == "/req.txt"

    line = "-r req.txt # mysterious comment"
    assert Parser.resolve_file("/", line) == "/req.txt"

    line = "-r req.txt"
    assert Parser.resolve_file("", line) == "req.txt"


def test_index_server():
    line = "--index-url https://some.foo/"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "-i https://some.foo/"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "--extra-index-url https://some.foo/"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "--extra-index-url https://some.foo"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "--extra-index-url https://some.foo # some lousy comment"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "-i\t\t https://some.foo \t\t    # some lousy comment"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "--index-url"
    assert Parser.parse_index_server(line) is None

    line = "--index-url=https://some.foo/"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "-i=https://some.foo/"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "--extra-index-url=https://some.foo/"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "--extra-index-url=https://some.foo"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "--extra-index-url=https://some.foo # some lousy comment"
    assert Parser.parse_index_server(line) == "https://some.foo/"

    line = "-i\t\t =https://some.foo \t\t    # some lousy comment"
    assert Parser.parse_index_server(line) == "https://some.foo/"


def test_requirements_package_with_index_server():
    content = """-i https://some.foo/\ndjango"""

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "django"
    assert dep.index_server == "https://some.foo/"


def test_requirements_parse_empty_line():
    content = """
    """

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    assert dep_file.dependencies == []
    assert dep_file.resolved_files == []


def test_requirements_parse_unsupported_line_start():
    content = "-f foo\n" \
              "--find-links bla\n" \
              "-i bla\n" \
              "--index-url bla\n" \
              "--extra-index-url bla\n" \
              "--no-index bla\n" \
              "--allow-external\n" \
              "--allow-unverified\n" \
              "-Z\n" \
              "--always-unzip\n"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    assert dep_file.dependencies == []
    assert dep_file.resolved_files == []


def test_file_resolver():
    content = "-r production/requirements.txt\n" \
              "--requirement test.txt\n"

    dep_file = parse(content=content, path="/", file_type=filetypes.requirements_txt)

    assert dep_file.resolved_files == [
        "/production/requirements.txt",
        "/test.txt"
    ]

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)

    assert dep_file.resolved_files == []


def test_is_marked_file():

    content = "# DON'T\nfoo"
    dep_file = parse(content, file_type=filetypes.requirements_txt)
    assert not dep_file.parser.is_marked_file

    dep_file = parse(content, file_type=filetypes.requirements_txt, marker=(("DON'T",), ()))
    assert dep_file.parser.is_marked_file


def test_is_marked_line():

    content = "foo # don't"
    dep_file = parse(content, file_type=filetypes.requirements_txt)
    assert not dep_file.parser.is_marked_line(next(dep_file.parser.iter_lines()))

    dep_file = parse(content, file_type=filetypes.requirements_txt, marker=((), ("don't",)))
    assert dep_file.parser.is_marked_line(next(dep_file.parser.iter_lines()))
