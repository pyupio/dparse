=======
History
=======

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
