=================
Dependency Parser
=================


.. image:: https://img.shields.io/pypi/v/dparse.svg
        :target: https://pypi.python.org/pypi/dparse

.. image:: https://img.shields.io/travis/pyupio/dparse.svg
        :target: https://travis-ci.org/pyupio/dparse

.. image:: https://codecov.io/gh/pyupio/dparse/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/pyupio/dparse


A parser for Python dependency files


Supported Files
---------------

+------------------+------------+-----------+
| File             | parse      | update    |
+==================+============+===========+
| requirements.txt | yes        | yes       |
+------------------+------------+-----------+
| conda.yml        | yes        | yes       |
+------------------+------------+-----------+
| tox.ini          | yes        | yes       |
+------------------+------------+-----------+
| Pipfile          | yes        | yes       |
+------------------+------------+-----------+
| Pipfile.lock     | yes        | yes       |
+------------------+------------+-----------+
| poetry.lock      | yes        | no        |
+------------------+------------+-----------+
| setup.py         | no (# 2_)  | no (# 2_) |
+------------------+------------+-----------+
| zc.buildout      | no (# 3_)  | no (# 3_) |
+------------------+------------+-----------+
| setup.cfg        | no (# 4_)  | no (# 4_) |
+------------------+------------+-----------+
| pyproject.toml   | yes        | no        |
+------------------+------------+-----------+

.. _2: https://github.com/pyupio/dparse/issues/2
.. _3: https://github.com/pyupio/dparse/issues/3
.. _4: https://github.com/pyupio/dparse/issues/8

************
Installation
************

To install dparse, run:

.. code-block:: console

    $ pip install dparse

If you want to update Pipfiles, install the pipenv extra:

.. code-block:: console

    $ pip install dparse[pipenv]

If you want to parse conda YML files, install the conda extra:

.. code-block:: console

    $ pip install dparse[conda]

*****
Usage
*****

To use dparse in a Python project::

    from dparse import parse, filetypes

    content = """
    South==1.0.1 --hash=sha256:abcdefghijklmno
    pycrypto>=2.6
    """

    df = parse(content, file_type=filetypes.requirements_txt)

    print(df.json())




    {
      "file_type": "requirements.txt",
      "content": "\nSouth==1.0.1 --hash=sha256:abcdefghijklmno\npycrypto>=2.6\n",
      "path": null,
      "sha": null,
      "dependencies": [
        {
          "name": "South",
          "specs": [
            [
              "==",
              "1.0.1"
            ]
          ],
          "line": "South==1.0.1 --hash=sha256:abcdefghijklmno",
          "source": "pypi",
          "meta": {},
          "line_numbers": null,
          "index_server": null,
          "hashes": [
            "--hash=sha256:abcdefghijklmno"
          ],
          "dependency_type": "requirements.txt",
          "extras": []
        },
        {
          "name": "pycrypto",
          "specs": [
            [
              ">=",
              "2.6"
            ]
          ],
          "line": "pycrypto>=2.6",
          "source": "pypi",
          "meta": {},
          "line_numbers": null,
          "index_server": null,
          "hashes": [],
          "dependency_type": "requirements.txt",
          "extras": []
        }
      ]
    }

**********
Python 2.7
**********

This tool requires latest Python patch versions starting with version 3.5. We
did support Python 2.7 in the past but, as for other Python 3.x minor versions,
it reached its End-Of-Life and as such we are not able to support it anymore.

We understand you might still have Python 2.7 projects running. At the same
time, Safety itself has a commitment to encourage developers to keep their
software up-to-date, and it would not make sense for us to work with officially
unsupported Python versions, or even those that reached their end of life.

If you still need to use Safety with Python 2.7, please use version 0.4.1 of
Dparse available at PyPi. Alternatively, you can run Safety from a Python 3
environment to check the requirements file for your Python 2.7 project.
