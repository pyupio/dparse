#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
"""Tests for `dparse.dependencies`"""

import pytest

from dparse.dependencies import Dependency, DependencyFile
from dparse import filetypes, parse, parser, errors


def test_dependency_serialize():
    dep = Dependency(
        name="foo",
        specs=(),
        line="foo==1.2.3"
    )

    serialized = dep.serialize()
    assert dep.name == serialized["name"]
    assert dep.specs == serialized["specs"]
    assert dep.line == serialized["line"]

    dep.extras = "some-extras"
    dep.line_numbers = (0, 4)
    dep.index_server = "some-foo-server"
    dep.hashes = {
        "method": "sha256",
        "hash": "the hash"
    }
    dep.dependency_type = filetypes.requirements_txt

    serialized = dep.serialize()
    assert dep.extras == serialized["extras"]
    assert dep.line_numbers == serialized["line_numbers"]
    assert dep.hashes == serialized["hashes"]
    assert dep.dependency_type == serialized["dependency_type"]


def test_dependency_deserialize():
    d = {
        "name": "foo",
        "specs": [],
        "line": "foo==1.2.3"
    }

    dep = Dependency.deserialize(d)

    assert d["name"] == dep.name
    assert d["specs"] == dep.specs
    assert d["line"] == dep.line

    d["extras"] = "some-extras"
    d["line_numbers"] = (0, 4)
    d["index_server"] = "some-foo-server"
    d["hashes"] = {
        "method": "sha256",
        "hash": "the hash"
    }
    d["dependency_type"] = filetypes.requirements_txt

    dep = Dependency.deserialize(d)

    assert d["extras"] == dep.extras
    assert d["line_numbers"] == dep.line_numbers
    assert d["index_server"] == dep.index_server
    assert d["hashes"] == dep.hashes
    assert d["dependency_type"] == dep.dependency_type


def test_dependency_file_serialize():
    content = "django==1.2\nrequests==1.2.3"
    dep_file = parse(
        content=content,
        file_type=filetypes.requirements_txt,
        path="req.txt",
        sha="sha"
    )

    serialized = dep_file.serialize()

    assert serialized["file_type"] == dep_file.file_type
    assert serialized["content"] == dep_file.content
    assert serialized["path"] == dep_file.path
    assert serialized["sha"] == dep_file.sha
    assert serialized["dependencies"][0]["name"] == "django"
    assert serialized["dependencies"][1]["name"] == "requests"


def test_dependency_file_deserialize():
    d = {
        'file_type': 'requirements.txt',
        'content': 'django==1.2\nrequests==1.2.3',
        'sha': 'sha',
        'dependencies': [
            {
                'hashes': [],
                'line_numbers': None,
                'extras': (),
                'name': 'django',
                'index_server': None,
                'dependency_type': 'requirements.txt',
                'line': 'django==1.2',
                'specs': [('==', '1.2')]
             },
            {
                'hashes': [],
                'line_numbers': None,
                'extras': (), 'name':
                'requests',
                'index_server': None,
                'dependency_type': 'requirements.txt',
                'line': 'requests==1.2.3',
                'specs': [('==', '1.2.3')]}],
        'path': 'req.txt'
    }

    dep_file = DependencyFile.deserialize(d)

    assert d['file_type'] == dep_file.file_type
    assert d['content'] == dep_file.content
    assert d['sha'] == dep_file.sha
    assert d['path'] == dep_file.path
    assert "django" == dep_file.dependencies[0].name
    assert "requests" == dep_file.dependencies[1].name


def test_parser_class():

    dep_file = parse("", file_type=filetypes.requirements_txt)
    assert isinstance(dep_file.parser, parser.RequirementsTXTParser)

    dep_file = parse("", path="req.txt")
    assert isinstance(dep_file.parser, parser.RequirementsTXTParser)

    dep_file = parse("", file_type=filetypes.tox_ini)
    assert isinstance(dep_file.parser, parser.ToxINIParser)

    dep_file = parse("", path="tox.ini")
    assert isinstance(dep_file.parser, parser.ToxINIParser)

    dep_file = parse("", file_type=filetypes.conda_yml)
    assert isinstance(dep_file.parser, parser.CondaYMLParser)

    dep_file = parse("", path="conda.yml")
    assert isinstance(dep_file.parser, parser.CondaYMLParser)

    dep_file = parse("", parser=parser.CondaYMLParser)
    assert isinstance(dep_file.parser, parser.CondaYMLParser)

    with pytest.raises(errors.UnknownDependencyFileError) as e:
        parse("")
