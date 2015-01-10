# -*- coding: utf-8 -*-
#
# Copyright 2014 Danny Goodall
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Return the directions from a given start point to a given end point.

.. moduleauthor:: Danny Goodall <danny@onebloke.com>

"""
__author__ = 'Danny Goodall'

from gmaps import Directions
from gmaps.errors import NoResults, InvalidRequest, RateLimitExceeded, RequestDenied, GmapException
from markupsafe import Markup

class GetDirections:
    """A wrapper for the gmaps Direction class to make it simpler to deal with in the classroom

    The :py:class:`GetDirections` class is inititialised with a starting point, an end_point and
    and optional transport mode.

    >>> directions = GetDirections("southampton, UK","winchester, UK", mode="walking")

    This returns an object that can then be interrogated for information about the route.

    >>> if directions.found:
    >>>     print("Directions found!")
    >>> else:
    >>>     print("Couldn't find a route.")

    If a valid route was found, simplified and prettified text can be accessed through:

    >>> directions.heading
    >>> "These are the steps for the (walking) journey from Southampton, Southampton, UK to Winchester, Winchester, Hampshire, UK."

    and:

    >>> directions.footer
    >>> "Map data ©2014 Google"

    and the steps of the route can be accessed through the :py:attr:`GetDirections.steps` property, which returns
    a :py:class:`list` of :py:class:`str`.

    >>> directions.steps
    >>> [
    >>>     "1. Head east (8 m / 1 min)",
    >>>     "2. Turn left toward Brunswick Pl/A3024 (7 m / 1 min)",
    >>>     "3. Turn right toward Brunswick Pl/A3024 (0.2 km / 3 mins)",
    >>>     "4. Turn right onto Brunswick Pl/A3024 (13 m / 1 min)",
    >>>     .
    >>>     .
    >>>     .
    >>>     "39. Turn right onto Colebrook St (85 m / 1 min)"
    >>> ]

    The raw :py:class:`gmaps.Directions` object can be accessed using:

    >>> directions.raw

    Once the object has been created, subsequent calls to the :py:meth:`GetDirections.journey` method will create
    new routes without the need to create a brand new :py:meth:`GetDirections` object.

    >>> new_directions = directions.new_journey("winchester, uk", "southampton, uk", "driving")
    """

    valid_modes = ['walking', 'driving', 'bicycling', 'transit']

    def __init__(self, starting_point, end_point, mode="walking"):
        """Create a new :py:class:`GetDirections` instance that can be interrogated for route details
        between `starting_point` and `end_point`.

        Args:
            starting_point (:py:class:`str`) : The text string that describes the starting point for the route
            end_point (:py:class:`str`) : The text string that describes the end point for the route
            mode (:py:class:`str`) : Text string either "walking", "driving", "bicycling" or "transit"
                Note that transit doesn't seem to be widely supported outside of the US.

        Attributes:
            starting_point (:py:class:`str`) : The text string that describes the starting point for the route
            end_point (:py:class:`str`) : The text string that describes the end point for the route
            mode (:py:class:`str`) : Text string either "walking", "driving", "bicycling" or "transit"
                Note that transit doesn't seem to be widely supported outside of the US.
            default_mode (:py:class:`str`, optional) : The mode that was specified the first time the object instance
                was created.
        """
        self.starting_point = None
        self.end_point = None
        self.mode = None
        self.default_mode = mode
        self._found = None
        self._heading = None
        self._footer = None
        self._steps = None
        self._directions = None
        self.new_journey(starting_point, end_point, mode)

    def new_journey(self, starting_point, end_point, mode=None):
        """Create a new journey, specifying start and end points and the mode of travel.

        This method pretty much mirrors the :py:meth:`GetDirections.__init__` method.

        If the journey appears valid to Google Maps, then this method sets appropriate values for the
        :py:attr:`GetDirections.heading` method, the :py:attr:`GetDirections.footer` and the
        :py:attr:`GetDirections.steps` methods.

        Args:
            starting_point (:py:class:`str`) : The text string that describes the starting point for the route
            end_point (:py:class:`str`) : The text string that describes the end point for the route
            mode (:py:class:`str`, optional) : Text string either "walking", "driving", "bicycling" or "transit", defaults to "walking".
            Note that transit doesn't seem to be widely supported outside of the US. Defaults to "walking".

        Attributes:
            starting_point (:py:class:`str`) : The text string that describes the starting point for the route
            end_point (:py:class:`str`) : The text string that describes the end point for the route
            mode (:py:class:`str`) : Text string either "walking", "driving", "bicycling" or "transit". Note that transit doesn't seem to be widely supported outside of the US.
            default_mode (:py:class:`str`) : The mode that was specified the first time the object instance was
                created.

        Returns:
            self (:py:class:`GetDirections`) : Returns an instance of the GetDirections object to allow for object
            chaining.
        """
        self.starting_point = starting_point
        self.end_point = end_point
        self.mode = mode if mode else self.default_mode
        self._heading = ""
        self._footer = ""
        self._steps = []
        self._found = False

        # Let's make sure that mode is valid
        if self.mode.lower() not in self.valid_modes:
            self._heading = "The mode of travel must be either {}.".format(
                ", ".join(x for x in self.valid_modes[:-1]) + " or " + self.valid_modes[-1]
            )
            return self

        # Grab the directions, check for an error
        try:
            self._directions = Directions().directions(self.starting_point, self.end_point, self.mode)
        except (NoResults, InvalidRequest, GmapException) as e:
            self._heading = "We couldn't find ({}) directions from: {}, to {}.".format(
                self.mode,
                self.starting_point,
                self.end_point
            )
        except (RateLimitExceeded, RequestDenied) as e:
            self._heading = "Google is a little busy at the moment, or for some reason our request has been " \
                            "denied. Wait a while, and then try again."
        else:
            if self._directions:
                self._found = True
                self._heading = "These are the steps for the ({}) journey from {} to {}.".format(
                    self.mode,
                    self._directions[0]['legs'][0]['start_address'],
                    self._directions[0]['legs'][0]['end_address'],
                )
                self._steps = [
                    "{:3}. {} ({} / {})".format(
                        counter + 1,
                        Markup(step['html_instructions']).striptags(),
                        step['distance']['text'],
                        step['duration']['text']
                    ) for counter, step in enumerate(self._directions[0]['legs'][0]['steps'])
                ]
                self._footer = self._directions[0]['copyrights']

        return self

    @property
    def heading(self):
        """Returns the text heading for this route.

        Returns the text heading for this route - if valid. Or if not valid then an appropriate message is returned
            instead.

        Returns:
            _heading (:py:class:`str`) : A text description of the route if it is valid, or an appropriate message
            if the route is not valid.

        """
        return self._heading

    @property
    def footer(self):
        """Returns the text footer for this route.

        Returns the text footer for this route which is usually a copyright notice - if valid. Or if not valid then a
            null string is returned instead.

        Returns:
            _footer (:py:class:`str`) : A text copyright notice if it is valid, or a null string if the route is
            not valid.
        """
        return self._footer

    @property
    def steps(self):
        """Returns a list of strings that describe the steps for this route.

        Returns a list of strings or an empty list if the route is not valid.

        Yields:
            (:py:class:`str`) : A generator of list of strings that describe the steps for this route, or an empty list if the route is not valid.
        """
        for step in self._steps:
            yield step

    @property
    def found(self):
        """Reveals if the route specified was found.

        Returns a boolean True if the route specified was found by Google, or False if the route could not be found.

        Returns:
            _found (:py:class:`bool`) : True if the route was valid or False if the route was invalid.
        """
        return self._found

    @property
    def raw(self):
        """Provides access to the raw :py:class:`gmaps.directions.Directions` class object.

        Returns:
            _directions (:py:class:`gmaps.Directions`) : The raw Directions object.
        """
        return self._directions
