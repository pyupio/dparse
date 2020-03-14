#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dparse.updater`"""

from dparse.parser import parse
from dparse.updater import RequirementsTXTUpdater, CondaYMLUpdater, ToxINIUpdater, PipfileLockUpdater, PipfileUpdater
from dparse import filetypes


def test_update_tox_ini():
    content = "[testenv:bandit]\n" \
              "commands =\n" \
              "\tbandit --ini setup.cfg -ii -l --recursive project_directory\n" \
              "deps =\n" \
              "\tbandit==1.4.0\n" \
              "\n" \
              "[testenv:manifest]\n" \
              "commands =\n" \
              "\tcheck-manifest --verbose\n"

    dep_file = parse(content, "tox.ini")
    dep = dep_file.dependencies[0]

    assert dep.name == "bandit"

    new_content = "[testenv:bandit]\n" \
                  "commands =\n" \
                  "\tbandit --ini setup.cfg -ii -l --recursive project_directory\n" \
                  "deps =\n" \
                  "\tbandit==2.9.5\n" \
                  "\n" \
                  "[testenv:manifest]\n" \
                  "commands =\n" \
                  "\tcheck-manifest --verbose\n"

    assert ToxINIUpdater.update(content=content, dependency=dep, version="2.9.5") == new_content


def test_update_conda_yml():
    content = "name: my_env\n" \
              "dependencies:\n" \
              "  - gevent=1.2.1\n" \
              "  - pip:\n" \
              "    - beautifulsoup4==1.2.3\n"

    dep_file = parse(content, "conda.yml")
    dep = dep_file.dependencies[0]

    assert dep.name == "beautifulsoup4"

    new_content = "name: my_env\n" \
                  "dependencies:\n" \
                  "  - gevent=1.2.1\n" \
                  "  - pip:\n" \
                  "    - beautifulsoup4==4.5.6\n"

    assert CondaYMLUpdater.update(content=content, dependency=dep, version="4.5.6") == new_content


def test_update_requirements_multispace():
    content = "                   pass"
    new_content = "pass==2.9.5"
    version = "2.9.5"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "pass"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_compatible():
    content = "Jinja2~=2.9.4         # via flask"
    new_content = "Jinja2==2.9.5         # via flask"
    version = "2.9.5"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "Jinja2"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_compatible_matching_latest():
    content = "Jinja2~=2.9.5         # via flask"
    new_content = "Jinja2==2.9.5         # via flask"
    version = "2.9.5"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "Jinja2"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_contains_correct_sep_char():
    content = "Jinja2==2.9.4         # via flask"
    new_content = "Jinja2==2.9.5         # via flask"
    version = "2.9.5"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "Jinja2"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_with_hashes():
    content = "alembic==0.8.9 \\\n" \
              "        --hash=sha256:abcde # yay"
    new_content = "alembic==1.4.2 \\\n" \
                  "    --hash=sha256:123 \\\n" \
                  "    --hash=sha256:456 # yay"
    version = "1.4.2"
    hashes = [{"method": "sha256", "hash": "123"}, {"method": "sha256", "hash": "456"}]

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "alembic"
    assert RequirementsTXTUpdater.update(content=content, version=version, dependency=dep,
                                         hashes=hashes) == new_content


def test_update_requirements_with_hashes_and_comment_and_env_markers():
    content = "alembic==0.8.9; sys_platform != 'win32' \\\n" \
              "        --hash=sha256:abcde # yay"
    new_content = "alembic==1.4.2; sys_platform != 'win32' \\\n" \
                  "    --hash=sha256:123 \\\n" \
                  "    --hash=sha256:456 # yay"
    version = "1.4.2"
    hashes = [{"method": "sha256", "hash": "123"}, {"method": "sha256", "hash": "456"}]

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "alembic"
    assert RequirementsTXTUpdater.update(content=content, version=version, dependency=dep,
                                         hashes=hashes) == new_content


def test_update_requirements_with_hashes_and_comment_inline():
    content = "alembic==0.8.9 --hash=sha256:abcde # yay"
    new_content = "alembic==1.4.2 \\\n" \
                  "    --hash=sha256:123 \\\n" \
                  "    --hash=sha256:456 # yay"
    version = "1.4.2"
    hashes = [{"method": "sha256", "hash": "123"}, {"method": "sha256", "hash": "456"}]

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "alembic"
    assert RequirementsTXTUpdater.update(content=content, version=version, dependency=dep,
                                         hashes=hashes) == new_content


def test_update_requirements_with_hash_and_space_separator():
    content = "taskcluster==0.3.4 --hash sha256:d4fe5e2a44fe" \
              "27e195b92830ece0a6eb9eb7ad9dc556a0cb16f6f2a6429f1b65"
    new_content = "taskcluster==1.4.2 \\\n" \
                  "    --hash=sha256:123 \\\n" \
                  "    --hash=sha256:456"
    version = "1.4.2"
    hashes = [{"method": "sha256", "hash": "123"}, {"method": "sha256", "hash": "456"}]

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "taskcluster"
    assert RequirementsTXTUpdater.update(content=content, version=version, dependency=dep,
                                         hashes=hashes) == new_content


def test_update_requirements_with_hash_and_comment_and_env_markers_inline():
    content = "alembic==0.8.9; sys_platform != 'win32' --hash=sha256:abcde # yay"
    new_content = "alembic==1.4.2; sys_platform != 'win32' \\\n" \
                  "    --hash=sha256:123 \\\n" \
                  "    --hash=sha256:456 # yay"
    version = "1.4.2"
    hashes = [{"method": "sha256", "hash": "123"}, {"method": "sha256", "hash": "456"}]

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "alembic"
    assert RequirementsTXTUpdater.update(content=content, version=version, dependency=dep,
                                         hashes=hashes) == new_content


def test_update_requirements_with_hash_inline():
    content = "alembic==0.8.9 --hash=sha256:abcde"
    new_content = "alembic==1.4.2 \\\n" \
                  "    --hash=sha256:123 \\\n" \
                  "    --hash=sha256:456"
    version = "1.4.2"
    hashes = [{"method": "sha256", "hash": "123"}, {"method": "sha256", "hash": "456"}]

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "alembic"
    assert RequirementsTXTUpdater.update(content=content, version=version, dependency=dep,
                                         hashes=hashes) == new_content


def test_update_requirements_with_env_markers():
    content = "uvloop==0.6.5; sys_platform != 'win32'"
    new_content = "uvloop==1.4.2; sys_platform != 'win32'"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "uvloop"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_with_env_markers_and_comment():
    content = "uvloop==0.6.5; sys_platform != 'win32' # and here's some comment"
    new_content = "uvloop==1.4.2; sys_platform != 'win32' # and here's some comment"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "uvloop"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_with_extras():
    content = "requests[security]==1.4.1"
    new_content = "requests[security]==1.4.2"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "requests"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_with_tabs():
    content = "bla==1.4.1\t\t# pyup: <1.4.2"
    new_content = "bla==1.4.2\t\t# pyup: <1.4.2"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "bla"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_with_plus():
    content = "some-package==0.12.2+tmf"
    new_content = "some-package==0.13.1"
    version = "0.13.1"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "some-package"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_line_endings():
    content = """\r\n\r\nWerkzeug\r\ndjango-template-repl\nbpython\nsome-fooo    \n"""
    version = "1.2.3"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)

    assert dep_file.dependencies[0].name == "Werkzeug"
    assert dep_file.dependencies[1].name == "django-template-repl"
    assert dep_file.dependencies[2].name == "bpython"
    assert dep_file.dependencies[3].name == "some-fooo"

    assert "Werkzeug==1.2.3\r\n" in RequirementsTXTUpdater.update(
        content=content,
        version=version,
        dependency=dep_file.dependencies[0]
    )
    assert "django-template-repl==1.2.3\n" in RequirementsTXTUpdater.update(
        content=content,
        version=version,
        dependency=dep_file.dependencies[1]
    )
    assert "bpython==1.2.3" in RequirementsTXTUpdater.update(
        content=content,
        version=version,
        dependency=dep_file.dependencies[2]
    )
    assert "some-fooo==1.2.3    \n" in RequirementsTXTUpdater.update(
        content=content,
        version=version,
        dependency=dep_file.dependencies[3]
    )


def test_update_requirements_simple_pinned():
    content = "Django==1.4.1"
    new_content = "Django==1.4.2"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "Django"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_simple_unpinned():
    content = "django"
    new_content = "django==1.4.2"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "django"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_simple_unpinned_with_comment():
    content = "django # newest django release"
    new_content = "django==1.4.2 # newest django release"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "django"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content

    content = "Django #django"
    new_content = "Django==1.4.2 #django"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "Django"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content

    content = "Django #django #yay this has really cool comments ######"
    new_content = "Django==1.4.2 #django #yay this has really cool comments ######"
    version = "1.4.2"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "Django"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_cookiecutter_template():
    content = 'raven==5.8.1\n' \
              '{%- endif %}\n\n' \
              '{% if cookiecutter.use_newrelic == "y" -%}\n' \
              '# Newrelic agent for performance monitoring\n' \
              '# -----------------------------------------\n' \
              'newrelic\n' \
              '{%- endif %}\n\n'
    new_content = 'raven==5.8.1\n' \
                  '{%- endif %}\n\n' \
                  '{% if cookiecutter.use_newrelic == "y" -%}\n' \
                  '# Newrelic agent for performance monitoring\n' \
                  '# -----------------------------------------\n' \
                  'newrelic==2.58.1.44\n' \
                  '{%- endif %}\n\n'
    version = "2.58.1.44"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[1]

    assert dep.name == "newrelic"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_with_double_package_name():
    content = 'raven\n' \
              'ravenclient'
    new_content = 'raven==2.58.1.44\n' \
                  'ravenclient'
    version = "2.58.1.44"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "raven"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_ranged():
    content = 'raven>=0.2\n' \
              'ravenclient'
    new_content = 'raven==1.5.6\n' \
                  'ravenclient'
    version = "1.5.6"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "raven"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_requirements_unfinished_line():
    content = 'raven==0.2\n'
    new_content = 'raven==1.5.6\n'
    version = "1.5.6"

    dep_file = parse(content=content, file_type=filetypes.requirements_txt)
    dep = dep_file.dependencies[0]

    assert dep.name == "raven"
    assert RequirementsTXTUpdater.update(content=content, version=version,
                                         dependency=dep) == new_content


def test_update_pipfile(monkeypatch):
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
    import pipenv.project
    monkeypatch.setattr(
        pipenv.project.pipfile.Pipfile,
        'find',
        lambda max_depth: '/tmp/MockPipFile'
    )
    dep_file = parse(content=content, file_type=filetypes.pipfile)
    dep = dep_file.dependencies[0]
    new_content = PipfileUpdater.update(content, version="2.1", dependency=dep)
    assert 'django = "==2.1"' in new_content
