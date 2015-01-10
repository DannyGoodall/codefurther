
Change Log for **CodeFurther**
==============================

v0.1.3 10th January 2015
------------------------
* Minor fix to requirements files

v0.1.2 10th January 2015
------------------------
* Merged PythonTop40 v0.1.6 (not 0.1.5 as the branch suggests)
* Added support for requests cache for top40
* Moved requests cache temp file to temp directory
* Made the test FileSpoofer class generic across multiple tests
* Added tests to check for malformed JSON in lyrics
* Removed some redundant tests
* Added code to test directions
* Added artist_exists() method for the lyrics module
* Changed the way lyrics handles HTTP errors
* Created helpers module for functions/classes across different modules
* Added PY2 / PY3 compatible code to several modules

v0.1.1 14th December 2014
-------------------------
* Fix for TypeError 'encoding' is an invalid keyword argument for this function - trying to install PythonTop40 on Python 2.7

v0.1.0 13th December 2014
-------------------------
* Minor changes to the documentation relating to Python 2 status
* First official release

v0.1.0.dev9 - 12th December 2014
--------------------------------
* Updated docs from previous change
* First cut at a Python 2 version. Need to create more tests so that I have greater coverage, but passing so far
* Changes to demo code so that it will run in V2 or V3
* Removed python3_compat.py
* Created extra dependencies - six and future
* Increased version number to v0.1.0.dev9

v0.1.0.dev8 - 12th December 2014
--------------------------------
* Added optional field "current" to the Chart model - used in V2 of the API, but not in V1
* Increased version number to v0.1.0.dev8

v0.1.0.dev7 - 11th December 2014
--------------------------------
* Refactoring of Doc generation and setup.py - both now get config information from package_info.json
* Increased version number to v0.1.0.dev7

v0.1.0.dev6 - 11th December 2014
--------------------------------
* Added an optional field "status" to the Entry model - This will be filled in using V2 of the API, but will be not present for V1.
* Added Test changes to ensure "status" field can be present or non-present.
* Increased version number to v0.1.0.dev6

v0.1.0.dev5 - 8th December 2014
-------------------------------
* Removed requirement for development version of Booby from setup.py
* Removed the trailing slash from the URL for /singles and /albums

v0.1.0.dev4 - 6th December 2014
-------------------------------
* Changed the way the setuptools ``long_description`` is accessed
* Documentation changes
* Removed ``demo.py``

  * Changed installation instructions to refer to **PythonTop40** on PyPI
  * Moved changes text into project route directory's ``CHANGES.RST`` and included them into ``docs/changes.rst``
  * Moved code examples out of the ``moredetail.rst`` file, and used ``literalinclude`` instead.
  * Added a link to the ReadTheDocs documentation into the README.rst file

v0.1.0.dev3 - 6th December 2014
-------------------------------
* Minor change to documentation

**ToDo** Modify links to PyPI and ReadTheDocs in the rest of the documentation.


v0.1.0.dev2 - 6th December 2014
-------------------------------
* Test coverage increased
* Initial documentation complete
* Documentation uploaded to `ReadTheDocs <http://pythontop40.readthedocs.org/en/latest/changes.html>`_
* **PythonTop40** now installable using pip - ``pip install pythontop40``
* **PythonTop40** now uploaded to `PyPi <https://pypi.python.org/pypi/pythontop40>`_

**ToDo** Modify links to PyPI and ReadTheDocs in the rest of the documentation.

V0.1.0.dev1 - 4th December 2014
-------------------------------

Initial version with working code and some tests.

**ToDo**:

* Complete tests coverage
* Complete documentation
* Upload documentation to ``readthedocs``.
* Make code installable using ``setup.py`` / ``pip``.
* Make code installable from ``PyPI`` using ``pip``.
