.. The convention used for headings here is
   #####
   Parts
   #####
   ========
   Chapters
   ========
   Section
   =======
   Subsection
   ----------
   Subsubsection
   ^^^^^^^^^^^^^
   Paragraph
   """""""""

#######################
Top40 - UK Top40 Charts
#######################

============
Introduction
============

The **Top40** module is part of the **codefurther** Python package, and is designed to be used in UK schools to provide
students with access to data that describes the UK Top 40 singles and albums.

Top40 is part of a wider initiative that I'm referring to as **CodeFurther**. The hope is that by providing simple
interfaces to information that is relevant to students, they will be able to relate to the data and imagine more
ways in which they could consume and use it in their code - and hopefully **CodeFurther**.

The data that **Top40** accesses is provided by the excellent work by
`@Ben Major <https://twitter.com/benmajor88>`_ and his
`UK Top 40 Charts API <http://ben-major.co.uk/2013/12/uk-top-40-charts-api/>`_.

The **Top40** module is under active development as part of the **CodeFurther** package and licensed under the
`Apache2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_,
so feel free to `contribute <https://bitbucket.org/dannygoodall/codefurther/pull-requests>`_ and
`report errors and suggestions <https://bitbucket.org/dannygoodall/codefurther/issues>`_.

.. note::
    The **Top40** library is designed to be used in UK schools to provide programmatic access to data that
    describes the UK Top 40 singles and albums. The hope is that by providing simple interfaces to access
    information that students may have an interest in, they may be inspired to **CodeFurther**.
    This documentation will therefore most likely be aimed at teachers and education professionals, who may not have a
    deep knowledge of Python.

.. warning::
    **Top40** is currently designed to work with Python version 3. I have recently carried out a small amount of work
    to make it run on Python 2, but this does need to be more thoroughly tested that my current Nose tests allow. If you
    `encounter any issues <https://bitbucket.org/dannygoodall/codefurther/issues>`_, or you'd like to `submit a pull
    request <https://bitbucket.org/dannygoodall/codefurther/pull-requests>`_, please contact me on BitBucket.

.....

========
Features
========

**Top40** provides:

* a list of the current Top 40 UK singles using the :py:attr:`singles <top40.Top40.singles>` property of the
  :py:class:`~top40.Top40` class.
* a list of the current Top 40 UK albums using the :py:attr:`albums <top40.Top40.singles>` property of the
  :py:class:`~top40.Top40` class.
* a :py:class:`chart <top40.Chart>` object relating to either singles or albums. The
  :py:class:`chart <top40.Chart>` object contains the:

  *  :py:attr:`~top40.Chart.date` that the chart was published
  *  the date that the chart was :py:attr:`~top40.Chart.retrieved` from the server
  *  a :py:class:`list` containing an :py:class:`~top40.Entry` for each Top 40 single or album

* **Top40** will also cache the results, so that once a result type (singles or albums) has been retrieved from
  the remote server, it will be returned on subsequent requests from the cache without refreshing from the remote
  server.
* The cache can be reset using the :py:func:`~top40.Top40.reset_cache` method, so that the next request for
  albums or singles information will be forced to obtain it by connecting to the remote server.

.....

=====
Usage
=====

**Top40** exposes a very simple API to developers. It is accessed by importing the :class:`~top40.Top40`
class into your module and creating an instance of this class, like so::

   from codefurther.top40 import Top40
   top40 = Top40()

The ``top40`` instance exposes a number of properties to the programmer. These include:

* :py:attr:`top40.albums <top40.Top40.albums>`
* :py:attr:`top40.singles <top40.Top40.singles>`
* :py:attr:`top40.albums_chart <top40.Top40.albums_chart>`
* :py:attr:`top40.singles_chart <top40.Top40.singles_chart>`

The example code below shows how you can use one of these properties to get a list of the current Top 40 albums.::

   from codefurther.top40 import Top40

   top40 = Top40()

   albums = top40.albums

   for album in albums:
       print(
           album.position,
           album.title,
           "BY",
           album.artist
       )

This short program uses the :py:attr:`~top40.Top40.albums` property of the :class:`~top40.Top40`
class to obtain the Python :class:`list` of the current Top 40 UK albums. It then loops through this list, and at each
iteration of the loop the variable `album` is set to the next album entry in the list.

A :func:`print` function then prints the :py:attr:`~top40.Entry.position`,
:py:attr:`~top40.Entry.title` and :py:attr:`~top40.Entry.artist` attributes of the album
:py:class:`entry <top40.Entry>` resulting in something like this:::

    1 Never Been Better BY Olly Murs
    2 X BY Ed Sheeran
    3 FOUR BY One Direction
    4 In The Lonely Hour BY Sam Smith
    5 The Endless River BY Pink Floyd
    .
    .
    .
    40 The London Sessions BY Mary J. Blige


I hope it's pretty clear what is going on, but a more detailed discussion of what the program does on can be found in
the ExploringTheTop40DemoCode_.

.. _ExploringTheTop40DemoCode:

.....

=============================
Exploring the Top40 Demo Code
=============================

Our example program
===================

Let's look at an example program, and examine in detail what it is doing and how it works.

.. literalinclude:: ../examples/top40demo.py
    :language: python
    :lines: 18-

Importing the PythonTop40 module
================================

The first line in our program

.. literalinclude:: ../examples/top40demo.py
    :emphasize-lines: 1
    :language: python
    :lines: 18-

uses the Python :keyword:`import` command to bring the :class:`~top40.Top40` class from the :mod:`top40`
module into our code.

This :keyword:`import` command means that our program can now use the :class:`~top40.Top40` class, to get the list
of Top 40 singles and albums. The :keyword:`import` command is how we tell Python that we want to use a feature that
isn't included in the Python standard library.

Creating a Top40 instance
=========================

The next line in our program creates a variable called ``top40`` which becomes the way we will talk to the remote server
where the lists of Top 40 singles and albums information is held.

.. literalinclude:: ../examples/top40demo.py
    :emphasize-lines: 3
    :language: python
    :lines: 18-

.. sidebar:: Behind the Scenes

    Technically speaking this code creates an *instance* of the :class:`~top40.Top40` *class*, and behind the
    scenes it is this that manages the communication with the remote server that contains the list of singles and
    albums.

    We don't really need to worry about that, as all of this complexity is hidden from us. Instead we simply
    interact with the data and capabilities that the ``top40`` variable provides us.


We can think of the ``top40`` variable as providing us with a number of ways to access the Top 40 charts for
albums and singles.

``top40`` does this through a number of *properties* that each returns different results to our
program.

If we were to use the :py:attr:`top40.singles <top40.Top40.singles>` *property* instead of the
:py:attr:`top40.albums <top40.Top40.albums>` *property*, then as you might expect our
program would receive a python :class:`list` of singles instead of a :py:class:`list` of albums.

Other properties that we could use are :py:attr:`top40.singles_chart <top40.Top40.singles_chart>` and
:py:attr:`top40.albums_chart <top40.Top40.albums_chart>` which both return a little bit more information about the
chart itself - such as the :py:attr:`~top40.Chart.date` it was published and the date it was
:py:attr:`~top40.Chart.retrieved` from the server.

Retrieving the Top40 albums
===========================

The following line of code creates a variable called ``albums`` and assigns to it the value returned from the
:py:attr:`top40.albums <top40.Top40.albums>` *property*.

.. literalinclude:: ../examples/top40demo.py
    :emphasize-lines: 5
    :language: python
    :lines: 18-


When this piece of code is executed, behind the scenes our ``top40`` variable *magically* makes contact with a server
over the Internet, asks it for the list of the Top 40 albums, and returns this list :py:class:`list` of information to
our ``albums`` variable.

The format of the returned data
===============================

If we could see the value returned to the ``albums`` variable in the above code, it would look *something* like this.

.. code-block:: python

    albums = [
        Entry(
            position = 1,
            artist = "One Direction"
            ...
        ),
        Entry(
            position = 2,
            artist = "Ed Sheeran"
            ...
        ),
        Entry(
            position = 3,
            artist = "Sam Smith"
            ...
        )
    ]

.. note:: The ``...`` in the above example shows that there are more pieces of information in the :class:`Entry`, but
    these are not shown to make the example easier to understand.

The data is enclosed in ``[]`` square brackets, which tells us that we have a Python :class:`list` of '*things*'. But
what are the things in the list? Well, because we have a :py:class:`list` of things, we can access the first
(or 0 :superscript:`th item)  in the list by placing ``[0]`` after the name of a :class:`list`.

.. code-block:: python

    print(albums[0])
    Entry(postition = 1, artist = "One Direction"...)

.. sidebar:: Behind the Scenes

    Whilst you will never have to do this yourself, an :class:`~top40.Entry` instance is created by passing
    *named arguments* to the :py:class:`~top40.Entry` class. If we were to manually create the
    :py:class:`~top40.Entry` instance, it might look something like this.

    .. code-block:: python

        entry = Entry(
            position = 3,
            previousPosition = 4,
            numWeeks = 26,
            artist = "Sam Smith",
            title = "In The Lonely Hour",
            Change(
                direction = "up",
                amount = 1,
                actual = 1
            )
        )

    If we then asked Python to print the position attribute of the ``entry`` variable, we would get the following result

    .. code-block:: python

        print(entry.position)
        3

    Likewise if we wanted to see how many weeks this entry had been in the chart we could access it like this.

    .. code-block:: python

        print(entry.numWeeks)
        26

    .. _EmbeddedChangeObject:

    So you should be able to see that inside our :py:class:`~top40.Entry` *object*, we have another object called
    :py:class:`~top40.Change`. This means that to access the :py:class:`~top40.Change` object that is inside
    the :py:class:`~top40.Entry` object, we would do the following.

    .. code-block:: python

        print(entry.change)
        <Change(
            amount=1,
            actual=1,
            direction='up'
        )>

    And finally, to access the direction of the change since last week's chart, we can see that we would have to access
    the :py:attr:`~top40.Change.direction` attribute of the :py:class:`~top40.Change` object that is
    embedded in the :py:class:`~top40.Entry` object. And to do that, we could type the following.

    .. code-block:: python

        print(entry.change.direction)
        up

Accessing the information within each chart entry
=================================================

This tells us that we have a list of things of type :py:class:`~top40.Entry`. There is one
:py:class:`~top40.Entry` for every album in our Top 40 chart. The example data above only shows the first 3
entries, but given that this is the Top 40 we are dealing with, we would expect to see 40 entries in our list.

Each entry is represented by a Python *object* called :class:`~top40.Entry`. The :class:`~top40.Entry`
*class* has been created as part of the **PythonTop40** project to hold the details of albums or singles in the chart.

As you'd expect from looking at the example code, the :class:`~top40.Entry` class can hold information about the
:py:attr:`position <top40.Entry.position>` of this entry, the name of the
:py:attr:`artist <top40.Entry.artist>`, the :py:attr:`title <top40.Entry.title>` of the album or single.

In addition, the number of weeks the album or single has been in the chart is accessed via the
:py:attr:`numWeeks <top40.Entry.numWeeks>` attribute and the position that the entry occupied last week can be
found by using the :py:attr:`previousPosition <top40.Entry.previousPosition>` attribute.

So in our original example, the next part the code loops through each of the album entries in the chart using the
:py:keyword:`for` statement, and then inside the loop, the value of ``album`` is set to each of the ``albums`` in our
list.

This means that we can use the :func:`print` function to print the position, title and artist of each of the
albums in our chart.

.. literalinclude:: ../examples/top40demo.py
    :emphasize-lines: 7-13
    :language: python
    :lines: 18-


Printing extra information about the chart entry
================================================

If we wanted to extend our demo program to print the number of weeks that the album had been in the chart, as well as
the chart position it occupied in the previous week's chart, we could do this by accessing the
:py:attr:`numWeeks <top40.Entry.numWeeks>` and :py:attr:`previousPosition <top40.Entry.previousPosition>`
attributes respectively.

The following code would achieve that.

.. literalinclude:: ../examples/top40demo2.py
    :emphasize-lines: 13-14
    :language: python
    :lines: 18-

If this code is run, it would result in something similar to this.

.. code-block:: text

    1 Never Been Better BY Olly Murs 1 0
    2 X BY Ed Sheeran 23 2
    3 FOUR BY One Direction 2 1
    4 In The Lonely Hour BY Sam Smith 27 3
    5 The Endless River BY Pink Floyd 3 4
    6 Wanted On Voyage BY George Ezra 22 8
    .
    .
    .
    40 The London Sessions BY Mary J. Blige 1 0

Formatting the output columns
=============================

It's not easy to see the information, but you can now see that there are two numbers at the end of each line that
represent the :py:attr:`numWeeks <top40.Entry.numWeeks>` and
:py:attr:`previousPosition <top40.Entry.previousPosition>` attributes respectively.

So if we now wanted to make the formatting a little easier to read, we can make use of the :py:func:`format` function
that allows us to carry out formatting on a string. The description of the :py:func:`format` function is outside the
scope of this tutorial, but hopefully the following code will be relatively simple to follow.

.. literalinclude:: ../examples/top40demo3.py
    :emphasize-lines: 9
    :language: python
    :lines: 18-

When this code is run, it produces a column-based list of album entries that is much easier to understand.

.. code-block:: text

        1 Never Been Better                                  by Olly Murs                                              1     0
        2 X                                                  by Ed Sheeran                                            23     2
        3 FOUR                                               by One Direction                                          2     1
        4 In The Lonely Hour                                 by Sam Smith                                             27     3
        5 The Endless River                                  by Pink Floyd                                             3     4
        6 Wanted On Voyage                                   by George Ezra                                           22     8
        .
        .
        .
       40 The London Sessions                                by Mary J. Blige                                          1     0

Hopefully you can see that the format string features a series of place markers - represented by the ``{}``
braces, and that each place marker brace corresponds with a data value in the list ``format()`` variables that follow.

.. literalinclude:: ../examples/top40demo3.py
    :emphasize-lines: 9-16
    :language: python
    :lines: 18-


Again, it will probably be clear that the text inside each of the braces such as ``{:5}`` tells the :py:func:`format`
function how many columns that specific entry will take up.

So ``{:5}`` at the beginning of the format string, tells the :py:func:`format` function to use 5 columns for the first
variable, and as :py:attr:`album.position <top40.Entry.position>` is the first in the list of variables inside the
:py:func:`format` function, the position of the album in the chart will take up the first 5 columns.

The second ``{}`` brace contains ``{:50}`` which means it will occupy 50 columns, and
the second variable is :py:attr:`album.title <top40.Entry.title>`, so the album title will occupy the next 50 columns,
and so on...

Notice that in amongst all those ``{}`` braces, the format string actually contains the word ``by``, because it's fine
to put other things in the format string alongside the ``{}`` braces - even spaces! If it isn't a ``{}`` brace then it just gets
produced as is.

Accessing the change information
================================

As mentioned above the album :py:class:`~top40.Entry` object has a
:py:class:`~top40.Change` object embedded within it.

.. code-block:: python

    entry = Entry(
        position = 3,
        previousPosition = 4,
        numWeeks = 26,
        artist = "Sam Smith",
        title = "In The Lonely Hour",
        Change(
            direction = "up",
            amount = 1,
            actual = 1
        )
    )

The :py:class:`~top40.Change` object actually describes the change since last week's chart in a little bit more
detail. It provides access to the following pieces of information about the chart :py:class:`~top40.Entry`.

* The :py:attr:`~top40.Change.amount` of change in position since last week's chart. The is an
  :py:func:`absolute <abs>` value - i.e. it describes the amount of change, but not the direction. So unless it is zero,
  it is always positive.
* The :py:attr:`~top40.Change.actual` amount of change in positions since last week's chart. This can be
  negative, positive or zero.
* The :py:attr:`~top40.Change.direction` of the change since last week. This is a :py:func`str` and is either
  ``up`` or ``down``.

Printing the change information
===============================

So if we wanted to alter our program so that we started printed a summary of whether the album had gone up or down since
last week, we could do so as follows.

.. literalinclude:: ../examples/top40demo4.py
    :emphasize-lines: 9,15-16
    :language: python
    :lines: 18-

You'll see that we've added the following ``{}`` braces to the format string

.. code-block:: python

    "{:4}({:4})"

and we've also added two more variables to the :py:func:`format` function.

.. code-block:: python

    album.change.direction,
    album.change.amount

These changes result in the following text output when the code is run.

.. code-block:: text

    1 Never Been Better                                  by Olly Murs                                              1     0 - down(   1)
    2 X                                                  by Ed Sheeran                                            23     2 - none(   0)
    3 FOUR                                               by One Direction                                          2     1 - down(   2)
    4 In The Lonely Hour                                 by Sam Smith                                             27     3 - down(   1)
    5 The Endless River                                  by Pink Floyd                                             3     4 - down(   1)
    6 Wanted On Voyage                                   by George Ezra                                           22     8 - up  (   2)
    .
    .
    .
   40 The London Sessions                                by Mary J. Blige                                          1     0 - down(  40)

Some finishing touches
======================

Finally, we'll make some significant changes to the program to add column headings, column formatting, and to alter the
text that describes the change since last week.

The output of the new program looks like this.

.. code-block:: text

    |   No. | Title                                              | Artist                                             |    Weeks | Previous | Change since last week |
    | ----- | -----                                              | ------                                             | -------- | -------- | ---------------------- |
    |     1 | Never Been Better                                  | Olly Murs                                          |        1 |        0 |     **NEW ENTRY**      |
    |     2 | X                                                  | Ed Sheeran                                         |       23 |        2 |                        |
    |     3 | FOUR                                               | One Direction                                      |        2 |        1 |   v by 2 places        |
    |     4 | In The Lonely Hour                                 | Sam Smith                                          |       27 |        3 |   v by 1 place         |
    |     5 | The Endless River                                  | Pink Floyd                                         |        3 |        4 |   v by 1 place         |
    |     6 | Wanted On Voyage                                   | George Ezra                                        |       22 |        8 | ^   by 2 places        |
    |     7 | 1989                                               | Taylor Swift                                       |        5 |        7 |                        |
    |     8 | Listen                                             | David Guetta                                       |        1 |        0 |     **NEW ENTRY**      |
    |     9 | Sonic Highways                                     | Foo Fighters                                       |        3 |        5 |   v by 4 places        |
    |    10 | It's The Girls                                     | Bette Midler                                       |        2 |        6 |   v by 4 places        |
    |    11 | Partners                                           | Barbra Streisand                                   |       11 |       16 | ^   by 5 places        |
    |    12 | Love In Venice                                     | André Rieu                                         |        4 |       11 |   v by 1 place         |
    |    13 | Hope                                               | Susan Boyle                                        |        1 |        0 |     **NEW ENTRY**      |
    |    14 | Dublin To Detroit                                  | Boyzone                                            |        1 |        0 |     **NEW ENTRY**      |
    |    15 | No Sound Without Silence                           | The Script                                         |       11 |       17 | ^   by 2 places        |
    |    16 | Forever                                            | Queen                                              |        3 |       13 |   v by 3 places        |
    |    17 | Christmas                                          | Michael Bublé                                      |       34 |       27 | ^   by 10 places       |
    |    18 | Motion                                             | Calvin Harris                                      |        4 |       18 |                        |
    |    19 | Blue Smoke - The Best Of                           | Dolly Parton                                       |       25 |       26 | ^   by 7 places        |
    |    20 | Home Sweet Home                                    | Katherine Jenkins                                  |        2 |       10 |   v by 10 places       |
    |    21 | The Greatest Hits                                  | Luther Vandross                                    |        2 |       22 | ^   by 1 place         |
    |    22 | Strictly Come Dancing                              | Dave Arch & The Strictly Come Dancing Band         |        1 |        0 |     **NEW ENTRY**      |
    |    23 | Melody Road                                        | Neil Diamond                                       |        6 |       15 |   v by 8 places        |
    |    24 | A Perfect Contradiction                            | Paloma Faith                                       |       38 |       23 |   v by 1 place         |
    |    25 | Sirens Of Song                                     | Jools Holland & His Rhythm & Blues Orchestra       |        1 |        0 |     **NEW ENTRY**      |
    |    26 | Chapter One                                        | Ella Henderson                                     |        7 |       25 |   v by 1 place         |
    |    27 | Serenata                                           | Alfie Boe                                          |        2 |       14 |   v by 13 places       |
    |    28 | My Dream Duets                                     | Barry Manilow                                      |        1 |        0 |     **NEW ENTRY**      |
    |    29 | Aquostic (Stripped Bare)                           | Status Quo                                         |        6 |       29 |                        |
    |    30 | Nothing Has Changed (The Best of David Bowie)      | David Bowie                                        |        2 |        9 |   v by 21 places       |
    |    31 | Love In The Future                                 | John Legend                                        |       52 |       32 | ^   by 1 place         |
    |    32 | Stand Beside Me: Live In Concert                   | Daniel O'Donnell                                   |        2 |       20 |   v by 12 places       |
    |    33 | Royal Blood                                        | Royal Blood                                        |       14 |       35 | ^   by 2 places        |
    |    34 | 5 Seconds Of Summer                                | 5 Seconds of Summer                                |       22 |       39 | ^   by 5 places        |
    |    35 | Caustic Love                                       | Paolo Nutini                                       |       33 |       38 | ^   by 3 places        |
    |    36 | Nostalgia                                          | Annie Lennox                                       |        5 |       30 |   v by 6 places        |
    |    37 | No Fixed Address                                   | Nickelback                                         |        2 |       12 |   v by 25 places       |
    |    38 | If Everyone Was Listening                          | Michael Ball                                       |        2 |       21 |   v by 17 places       |
    |    39 | +                                                  | Ed Sheeran                                         |      168 |       42 | ^   by 3 places        |
    |    40 | The London Sessions                                | Mary J. Blige                                      |        1 |        0 |     **NEW ENTRY**      |

And below is the complete program that produced the output above.

.. literalinclude:: ../examples/top40demo5.py
    :language: python
    :lines: 18-

It might be worth spending a little time looking at the program and the output that it produces, to see if you can see
which changes in the code produce which changes in the output.

.....

=========
Top40 API
=========

.. automodule:: top40
	:members:
	:member-order: bysource