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
| zc.bildout       | no (# 3_)  | no (# 3_) |
+------------------+------------+-----------+

.. _1: https://github.com/pyupio/dparse/issues/1
.. _2: https://github.com/pyupio/dparse/issues/2
.. _3: https://github.com/pyupio/dparse/issues/3

************
Installation
************

To install dparse, run:

.. code-block:: console

    $ pip install -e git+https://github.com/pyupio/dparse.git

*****
Usage
*****

To use dparse in a Python project::

    from dparse import parse, filetypes

    content = """
    -e common/lib/calc
    South==1.0.1 --hash==abcdefghijklmno
    pycrypto>=2.6
    git+https://github.com/pmitros/pyfs.git@96e1922348bfe6d99201b9512a9ed946c87b7e0b
    distribute>=0.6.28, <0.7
    # bogus comment
    -e .
    pdfminer==20140328
    -r production/requirements.txt
    --requirement test.txt
    """

    df = parse(content, filetype=filetypes.requirements_txt)

    print(df.json())
