=================
Dependency Parser
=================


.. image:: https://img.shields.io/pypi/v/dparse.svg
        :target: https://pypi.python.org/pypi/dparse

.. image:: https://img.shields.io/travis/pyupio/dparse.svg
        :target: https://travis-ci.org/pyupio/dparse

.. image:: https://codecov.io/gh/pyupio/dparse/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/pyupio/dparse

.. image:: https://readthedocs.org/projects/dparse/badge/?version=latest
        :target: https://dparse.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jayfk/dparse/shield.svg
     :target: https://pyup.io/repos/github/pyupio/dparse/
     :alt: Updates


A parser for Python dependency files


* Free software: MIT license
* Documentation: https://dparse.readthedocs.io.


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
| Pipfile          | no (# 1_)  | no (# 1_) |
+------------------+------------+-----------+
| Pifile.lock      | no (# 1_)  | no (# 1_) |
+------------------+------------+-----------+
| setup.py         | no (# 2_)  | no (# 2_) |
+------------------+------------+-----------+
| zc.buildout       | no (# 3_)  | no (# 3_) |
+------------------+------------+-----------+
| setup.cfg        | no (# 4_)  | no (# 4_) |
+------------------+------------+-----------+

.. _1: https://github.com/pyupio/dparse/issues/1
.. _2: https://github.com/pyupio/dparse/issues/2
.. _3: https://github.com/pyupio/dparse/issues/3
.. _4: https://github.com/pyupio/dparse/issues/8

************
Installation
************

To install dparse, run:

.. code-block:: console

    $ pip install dparse

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
