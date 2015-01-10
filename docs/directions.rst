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

###############################
directions - Google maps routes
###############################

The **Directions** module is part of the **codefurther** Python package, and is designed to be used in UK schools to provide
students with access to data that describes journeys from one point to another.

**Directions** is part of a wider initiative that I'm referring to as **CodeFurther**. The hope is that by providing simple
interfaces to information that is relevant to students, they will be able to relate to the data and imagine more
ways in which they could consume and use it in their code - and hopefully **CodeFurther**.

The data that **Directions** accesses is provided by Google as part of its
`Google Maps API <https://developers.google.com/maps/>`_.

.....

========
Features
========

**Directions** provides:

* Simplified access to directions from `a` to `b` using Google Maps
* Place names can be vague, Google will do it's best to decipher them
* Walking, cycling, driving and transit routes

.....

=====
Usage
=====

Importing the module
====================

**Directions** exposes a very simple API to developers. It is accessed by importing the
:class:`~directions.GetDirections` class into your module and creating an instance of this class, like so::

   from codefurther.directions import GetDirections
   directions = GetDirections("southampton", "winchester")

GetDirections parameters
========================

The :py:class:`GetDirections` object is initialised with a starting location and an end location. It can also be
initialised with an optional ``mode`` parameter that describes the mode of transport to use.::

   from codefurther.directions import GetDirections

   driving_directions = GetDirections("southampton","winchester", "driving")
   walking_directions = GetDirections("southampton","winchester", "walking)
   bike_directions = GetDirections("southampton","winchester", "bicycling")
   transit_directions = GetDirections("southampton","winchester", "transit")

GetDirections properties
========================

The :py:class:`~directions.GetDirections` instance exposes a number of properties to the programmer. These include:

* :py:attr:`GetDirections.found <directions.GetDirections.found>`
* :py:attr:`GetDirections.heading <directions.GetDirections.heading>`
* :py:attr:`GetDirections.footer <directions.GetDirections.footer>`
* :py:attr:`GetDirections.steps <directions.GetDirections.steps>`

Example program
===============

The example code below shows how you can use these properties to get directions from one place to another.::

    from codefurther.directions import GetDirections

    directions = GetDirections("Southampton, UK", "Winchester, UK")

    if directions.found:
        print( directions.heading )
        for step in directions.steps:
            print( step )
        print( directions.footer )

When run, this code results in the following extract being printed to the display.::

    These are the steps for the (walking) journey from Southampton, Southampton, UK to Winchester, Winchester, Hampshire, UK.
    1. Head east (8 m / 1 min)
    2. Turn left toward Brunswick Pl/A3024 (7 m / 1 min)
    3. Turn right toward Brunswick Pl/A3024 (0.2 km / 3 mins)
    .
    .
    .
    39. Turn right onto Colebrook St (85 m / 1 min)
    Map data ©2014 Google

It is possible to run the same code without first checking if the result was found. In that case, **CodeFurther** will
simply replace the header text with a message stating that the route could not be found, no direction steps will
be returned, and the footer will be blank too.::

    from codefurther.directions import GetDirections

    directions = GetDirections("123l123", "345345l34")

    print(directions.heading)
    for step in directions.steps:
        print(step)
    print(directions.footer)

When run, this code would produce the following output (returned by the :py:attr:`GetDirections.heading <directions.GetDirections.heading>` property). ::

    We couldn't find (walking) directions from: 123l123, to 345345l34.

The idea here is that when used in the classroom, the students will not be put off experimenting by having to remember
to check for the :py:attr:`GetDirections.found <directions.GetDirections.found>` property.

.....

==============
Directions API
==============

.. automodule:: directions
	:members:
	:member-order: bysource