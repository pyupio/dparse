#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""Tests for `dparse.parser`"""

from dparse.parser import parse, Parser
from dparse import filetypes
from packaging.specifiers import SpecifierSet


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


def test_pipfile():
    content = """[[source]]

url = "http://some.pypi.mirror.server.org/simple"
verify_ssl = false
name = "pypi"


[packages]

django = "==2.0"
djangorestframework = "*"
django-allauth = "*"


[dev-packages]

toml = "*"
"""
    dep_file = parse(content, file_type=filetypes.pipfile)
    assert len(dep_file.dependencies) == 4
    assert dep_file.dependencies[0].name == 'django'
    assert dep_file.dependencies[0].specs == SpecifierSet('==2.0')
    assert dep_file.dependencies[1].name == 'djangorestframework'
    assert dep_file.dependencies[1].specs == SpecifierSet()


def test_pipfile_lock():
    content = """{
    "_meta": {
        "hash": {
            "sha256": "8b5635a4f7b069ae6661115b9eaa15466f7cd96794af5d131735a3638be101fb"
        },
        "host-environment-markers": {
            "implementation_name": "cpython",
            "implementation_version": "3.6.3",
            "os_name": "posix",
            "platform_machine": "x86_64",
            "platform_python_implementation": "CPython",
            "platform_release": "17.3.0",
            "platform_system": "Darwin",
            "platform_version": "Darwin Kernel Version 17.3.0: Thu Nov  9 18:09:22 PST 2017; root:xnu-4570.31.3~1/RELEASE_X86_64",
            "python_full_version": "3.6.3",
            "python_version": "3.6",
            "sys_platform": "darwin"
        },
        "pipfile-spec": 6,
        "requires": {},
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.python.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {
        "django": {
            "hashes": [
                "sha256:52475f607c92035d4ac8fee284f56213065a4a6b25ed43f7e39df0e576e69e9f",
                "sha256:d96b804be412a5125a594023ec524a2010a6ffa4d408e5482ab6ff3cb97ec12f"
            ],
            "version": "==2.0.1"
        },
        "pytz": {
            "hashes": [
                "sha256:80af0f3008046b9975242012a985f04c5df1f01eed4ec1633d56cc47a75a6a48",
                "sha256:feb2365914948b8620347784b6b6da356f31c9d03560259070b2f30cff3d469d",
                "sha256:59707844a9825589878236ff2f4e0dc9958511b7ffaae94dc615da07d4a68d33",
                "sha256:d0ef5ef55ed3d37854320d4926b04a4cb42a2e88f71da9ddfdacfde8e364f027",
                "sha256:c41c62827ce9cafacd6f2f7018e4f83a6f1986e87bfd000b8cfbd4ab5da95f1a",
                "sha256:8cc90340159b5d7ced6f2ba77694d946fc975b09f1a51d93f3ce3bb399396f94",
                "sha256:dd2e4ca6ce3785c8dd342d1853dd9052b19290d5bf66060846e5dc6b8d6667f7",
                "sha256:699d18a2a56f19ee5698ab1123bbcc1d269d061996aeb1eda6d89248d3542b82",
                "sha256:fae4cffc040921b8a2d60c6cf0b5d662c1190fe54d718271db4eb17d44a185b7"
            ],
            "version": "==2017.3"
        }
    },
    "develop": {}
}"""
    dep_file = parse(content, file_type=filetypes.pipfile_lock)
    assert dep_file.dependencies[0].name == 'django'
    assert dep_file.dependencies[0].specs == SpecifierSet('==2.0.1')
    assert dep_file.dependencies[0].hashes == [
        "sha256:52475f607c92035d4ac8fee284f56213065a4a6b25ed43f7e39df0e576e69e9f",
        "sha256:d96b804be412a5125a594023ec524a2010a6ffa4d408e5482ab6ff3cb97ec12f"
    ]
