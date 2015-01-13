CodeFurther
===========

The **CodeFurther** library is designed to be used in UK schools to provide students with access to data that hopefully
has some relevance for them. The hope is that by gaining access to meaningful data, they will be inspired to
**CodeFurther**.

**CodeFurther** is under active development
and is licensed under the `Apache2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_,
so feel free to `contribute <https://bitbucket.org/dannygoodall/codefurther/pull-requests>`_ and
`report errors and suggestions <https://bitbucket.org/dannygoodall/codefurther/issues>`_.

.. note::
    The **CodeFurther** package is designed to be used in UK schools to provide programmatic access to data that
    describes the UK Top 40 singles and albums. The hope is that by providing simple interfaces to access
    information that students may have an interest in, they may be inspired to **CodeFurther**.
    This documentation will therefore most likely be aimed at teachers and education professionals, who may not have a
    deep knowledge of Python.

.. warning::
    **CodeFurther** is currently designed to work with Python version 3. I have recently carried out some work to make
    it run on Python 2 too, but this does need to be more thoroughly tested that my current Nose tests allow. If you
    `encounter any issues <https://bitbucket.org/dannygoodall/codefurther/issues>`_, or you'd like to `submit a pull
    request <https://bitbucket.org/dannygoodall/codefurther/pull-requests>`_, please contact me on BitBucket.

Modules in the Package
----------------------
**CodeFurther** contains a number of modules that provide access to *interesting* data. Those modules are shown below:

.. csv-table:: CodeFurther Modules
    :header: "Module", "Description"
    :widths: 30, 50

    ``top40``, "Provides access to the UK Top 40 charts for singles and albums."
    ``lyrics``, "Allows lyrics for a given artist and song title to be accessed within Python."
    ``directions``, "Allows Google Maps route directions to be accessed from within Python."

Features
========
**CodeFurther** provides:

* a list of the current Top 40 UK singles using the `singles <top40.Top40.singles>` property of the
  `~top40.Top40` class.
* a list of the current Top 40 UK albums using the `albums <top40.Top40.singles>` property of the
  `~top40.Top40` class.
* the ability to retrieve the lyrics for a given artist
* the ability to find all of the songs for a given artist
* the ability to search for a specific artist

Installation
============

**CodeFurther** can be found on the Python Package Index `PyPi here. <https://pypi.python.org/pypi/codefurther>`_
It can be installed using ``pip``, like so. ::

    pip install codefurther

Documentation
=============
The documentation for **CodeFurther** can be found on the
`ReadTheDocs site <http://codefurther.readthedocs.org/en/latest/index.html>`_.

Tests
-----
To run the **CodeFurther** test suite, you should install the test and development requirements and then run nosetests.

.. code-block:: bash

    $ pip install -r dev-requirements.txt
    $ nosetests tests

Changes
-------

See `Changes <changes>`.
