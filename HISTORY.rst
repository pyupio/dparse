=======
History
=======

0.5.2a (master)
---------------

* Current unstable version

0.5.1 (2020-04-26)
------------------

* Fixed package metadata removing 2.7 support
* Install pipenv only when asked for with extras

0.5.0 (2020-03-14)
------------------

A bug with this package allows it to be installed on Python 2.7 environments,
even though it should not work on such version. You should stick with version
0.4.1 version instead for Python 2.7 support.

* Dropped Python 2.7, 3.3, 3.4 support
* Removed six package
* Removed pinned dependencies of tests
* Dropped setup.py tests support in favor of tox

0.4.1 (2018-04-06)
------------------

* Fixed a packaging error.

0.4.0 (2018-04-06)
------------------

* pipenv is now an optional dependency that's only used when updating a Pipfile. Install it with dparse[pipenv]
* Added support for invalid toml Pipfiles (thanks @pombredanne)


0.3.0 (2018-03-01)
------------------

* Added support for setup.cfg files (thanks @kexepal)
* Dependencies from Pipfiles now include the section (thanks @paulortman)
* Multiline requirements are now ignored if they are marked
* Added experimental support for Pipfiles

0.2.1 (2017-07-19)
------------------

* Internal refactoring

0.2.0 (2017-07-19)
------------------

* Removed setuptools dependency


0.1.1 (2017-07-14)
------------------

* Fixed a bug that was causing the parser to throw errors on invalid requirements.

0.1.0 (2017-07-11)
------------------

* Initial, not much to see here.
