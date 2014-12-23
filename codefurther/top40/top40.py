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

"""The ``top40`` module contains the high level classes that are used to package the returned data such as
:py:class:`Entry`, :py:class:`Chart` and :py:class:`Change`.

In addition the :py:class:`Top40` class provides the main external interface into the module. Once an instance of the
:py:class:`Top40` class has been instantiated it can be used to return data from the remote API to the called program::

    from pythontop40 import Top40

    top40 = Top40()

    album_list = top40.albums
    singles_list = top40.singles

    albums_chart = top40.albums_chart
    singles_chart = top40.singles_chart

From there, the returned objects can be interrogated and interacted with::

    first_album = album_list[0]
    print( first_album.position )
    print( first_album.artist )

    print("The date of the singles chart is", singles_chart.date)
    print(The album_chart was retrieved from the server on", albums_chart.retrieved

And this, don't forget this::

    class Repo(Model):
         name = fields.String()
         owner = fields.Embedded(User)

    booby = Repo(
        name='Booby',
        owner={
            'login': 'jaimegildesagredo',
            'name': 'Jaime Gil de Sagredo'
        })

    print booby.to_json()
    '{"owner": {"login": "jaimegildesagredo", "name": "Jaime Gil de Sagredo"}, "name": "Booby"}'
"""

from __future__ import print_function
__author__ = 'Danny Goodall'
import requests
import requests.exceptions
from nap.url import Url
from booby import Model, fields
from codefurther.errors import CodeFurtherConnectionError, CodeFurtherError, CodeFurtherHTTPError, CodeFurtherReadTimeoutError
from codefurther.utils import recurse_structure


class Change(Model):
    """The Change model that describes the change of this entry since last week's chart.

    This class isn't made publicly visible, so it should never really need to be initialised manually. That said,
    it is initialised by passing a series of keyword arguments, like so::

        change = Change(
            direction = "down",
            amount = 2,
            actual = -2
        )

    The model does not feature any validation.

    Args:
        \*\*kwargs: Keyword arguments with the fields values to initialize the model.
    Attributes:
        direction (str): The direction of the change "up" or "down".
        amount (int): The amount of change in chart position expressed as a positive integer.
        actual (int): The amount of the change in chart position expressed as positive or negative (or 0).
    Returns:
        :py:class:`Change`: The Change model instance created from the passed arguments.
    """
    direction = fields.String()
    amount = fields.Integer()
    actual = fields.Integer()


class Entry(Model):
    """The Entry model that contains the details about the chart entry, a Change Model is embedded in each Entry model.

    Args:
        position (:py:class:`int`): The position of this entry in the chart.
        previousPosition (:py:class:`int`): The position of this entry in the previous week's chart.
        numWeeks (:py:class:`int`): The number of weeks this entry has been in the chart.
        artist (:py:class:`str`): The name of the artist for this entry.
        title (:py:class:`str`): The title of this entry.
        change (:py:class:`Change`): The embedded change model that describes the change in position.
        status (:py:class:`str`): **NEW in dev6** The text status from the BBC chart - takes the format of
            "new" ¦ "up 3" ¦ "down 4" ¦ "non-mover". Not used in Ben Major's V1 API - optional
    Attributes:
        position (:py:class:`int`): The position of this entry in the chart.
        previousPosition (:py:class:`int`): The position of this entry in the previous week's chart.
        numWeeks (:py:class:`int`): The number of weeks this entry has been in the chart.
        artist (:py:class:`str`): The name of the artist for this entry.
        title (:py:class:`str`): The title of this entry.
        change (:py:class:`Change`): The embedded change model that describes the change in position.
        status (:py:class:`str`): **NEW in dev6** The text status from the BBC chart - takes the format of
            "new" ¦ "up 3" ¦ "down 4" ¦ "non-mover". Not used in Ben Major's V1 API - optional
    Returns:
        :class:`Entry`: The Entry model instance created from the arguments.
    """

    position = fields.Integer()
    previousPosition = fields.Integer()
    numWeeks = fields.Integer()
    artist = fields.String()
    title = fields.String()
    change = fields.Embedded(Change)

    # Status is optional
    status = fields.String(required=False)


class Chart(Model):
    """The Chart model that contains the embedded list of entries.

    Args:
        entries (:py:class:`list` of :py:class:`dict`): A list of Python dictionaries. Each dictionary describes each
            :class:`Entry` type in the chart, so the keys in the dictionary should match the properties of the
            :class:`Entry` class.
        date (:py:class:`int`): The date of this chart as an integer timestamp containing the total number of seconds.
        retrieved (:py:class:`int`): The date that this chart was retrieved from the API server as an integer timestamp
            containing the total number of seconds.
        current (:py:class:`bool`): **Optional**. A flag used in V2 of the API to signify if the last scheduled read from the BBC's
            server worked on not. A value ``True`` means that the returned chart is the latest version that we have
            tried to read. A value of ``False`` means that the chart that is being returned is old. In all liekliehood
            the chart is probably still in accurate as it is only updated once per week, so this flag only means that
            the last scheduled read from the BBC's server did not work.
    Attributes:
        entries (:py:class:`list` of :py:class:`Entry`): A list of :py:class:`Entry` types for each entry in the
            specific :py:class:`Chart`. The entries are returned in the :py:class:`list` with the highest chart position
            (i.e. the lowest number - #1 in the chart) first.
        date (:py:class:`int`): The date of this chart as an integer timestamp containing the total number of seconds.
            This value can then be converted to a Python :py:class:`datetime.datetime` type by
            ``datetime_type = datetime.datetime.fromtimestamp(chart.date)``
            (assuming that the ``chart`` variable was of type :py:class:`Chart`).
        retrieved (:py:class:`int`): The date that this chart was retrieved from the API server as an integer timestamp
            containing the total number of seconds. This can be converted to a datetime type in the same as described
            for ``date`` above.
        current (:py:class:`bool`): **Optional**. A flag used in V2 of the API to signify if the last scheduled read from the BBC's
            server worked on not. A value ``True`` means that the returned chart is the latest version that we have
            tried to read. A value of ``False`` means that the chart that is being returned is old. In all liekliehood
            the chart is probably still in accurate as it is only updated once per week, so this flag only means that
            the last scheduled read from the BBC's server did not work.
    Returns:
        Chart (:py:class:`Chart`): The Chart model instance created from the arguments.

    """
    date = fields.Integer()
    retrieved = fields.Integer()
    entries = fields.Collection(Entry)
    current = fields.Boolean(required=False)


class ChartsAPI(Url):
    """Provides the physical connection to the API for the Top40 object.

    This is the route into API and is a subclass of nap.Url. It provides the get method that carries out the request.get
    method for the chart API.

    This class overrides the :func:`ChartsAPI.get` and :func:`ChartsAPI.after_request` methods in the base class. The
    response returned from the :class:`nap.Url` class is recursively parsed to convert any embedded
    :class:`dict` objects, to :class:`~munch.Munch` types. This is to allow `dot access` to the members of the response,
    as well as using the traditional dict['key'] access.

    Attributes:
        convert (dict): contains none or more key, value pairs.
    """
    def __init__(self, *args, **kwargs):
        self.convert = {}
        super(ChartsAPI, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        # Remove the convert kwarg before calling super class get
        self.convert = kwargs.pop("convert", {})
        return (
            super(ChartsAPI, self).get(*args, **kwargs)
        )

    def after_request(self, response):
        if response.status_code != 200:
            response.raise_for_status()

        # Now turn the dicts in the Json response into Munch types so that
        # they can be accessed using .notation

        response_munch = recurse_structure(response.json(), convert=self.convert)

        return response_munch


class Top40(object):
    """ Provides the programmer with properties that return the Top 40 chart data.

    The programmer creates an instance of this object, and then uses the exposed properties to access the data about
    the singles and albums charts.

    Attributes:
        error_format (str): The format string to be used when creating error messages.
        what_am_i (str): Not implemented yet.
        what_do_i_manage (str): Not implemented yet.
    """
    error_format = "Received an error whist reading from {}: Returned code: {}"
    what_am_i = "Top40"
    what_do_i_manage = "charts information"

    def __init__(self, base_url="http://ben-major.co.uk/labs/top40/api/"):
        """Creates and returns the object instance.

        Args:
            base_url (str): The base url of the remote API before the specific service details are appended.
                For example, the base url might be "a.site.com/api/", and the service "/albums/", when appended to the
                base url, creates the total url required to access the album data.
        Returns:
            Top40 (Top40): The Top40 model instance.
        """
        self.api = ChartsAPI(base_url)
        self.reset_cache()

    def reset_cache(self):
        """Remove any cached singles or albums charts

        Because the UK Top40 charts only change once per week, :py:class:`Top40` will cache the results of singles and
        albums. This means that during the execution of a program, repeated calls to retrieve singles and albums chart
        information will only actually call the remote API once. If, for whatever reason you need to ensure that an
        attempt to access single or album information actually results in a call to the remote API, then calling the
        :py:meth:`Top40.reset_cache` method will do this, by clearing down any existing cached chart information.
        """
        self._albums_chart = None
        self._singles_chart = None

    def _get_data(self, url, params=None, convert=None):
        """Internal routine to retrieve data from the external service.

        The URL component that is passed is added to the base URL that was specified when the object was instantiated.
        Additional params passed will be passed to the API as key=value pairs, and the return data is parsed and
        any :func:`dict` contained within the structure is converted to a :class:`Munch` type. In addition, the convert
        :class:`dict` is used to optionally convert values returned from the API to different types.

        Args:
            url (str): The remote url to connect to.
            params (dict): Additional parameters will be passed as key=value pairs to the URL as query variables
                ?key=value.
            convert (dict): The JSON structure that is returned is parsed for instances of ``key``, and if
                found the, value of convert[key] is used to convert it. For example supplying ``{"position",int}``
                would ensure that if the key ``position`` was found in the JSON structure, it will be converted to type
                int.
        Returns:
            response (JSON): All embedded :class:`dict` will be converted to :class:`Munch`.
        """
        if not params:
            params = {}
        if not convert:
            convert = {}
        try:
            response_json = self.api.get(url, params=params, convert=convert)
        except requests.exceptions.HTTPError as e:
            message = Top40.error_format.format(
                url,
                e.response.status_code
            )
            print(message)
            raise CodeFurtherHTTPError(message, e.response.status_code)
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout):
            raise CodeFurtherConnectionError("Could not connect to remote server.".format(self.what_do_i_manage))
        except requests.exceptions.ReadTimeout:
            raise CodeFurtherReadTimeoutError("The remote server took longer than expected to reply.")
        except Exception as e:
            raise
        return response_json

    def _get_albums_chart(self):
        """Internal routine to pull the albums chart information into the cache
        """
        albums = self._get_data("/albums")
        self._albums_chart = Chart(**albums)


    @property
    def albums_chart(self):
        """A ``property`` that returns the :py:class:`Chart` object for the current Top40 albums

        Returns:
            :py:class:`Chart`: The albums' chart object - an instance of the :class:`Chart` class containing the album
                information and the and the issue and retrieval dates specific to this chart.
        """
        if self._albums_chart is None:
            self._get_albums_chart()
        return self._albums_chart

    @property
    def albums(self):
        """A ``property`` that returns a :py:class:`list` of album :py:class:`Entry` types.

        Returns:
            :py:class:`list` : A :py:class:`list` of :class:`Entry` instances. Each entry describes an album in the chart.
        """
        albums_chart = self.albums_chart
        return albums_chart.entries

    def _get_singles_chart(self):
        """Internal routine to pull the singles chart information into the cache
        """
        singles = self._get_data("/singles")
        self._singles_chart = Chart(**singles)

    @property
    def singles_chart(self):
        """A ``property`` that returns the :py:class:`Chart` object for the current Top40 singles

        Returns:
            :py:class:`Chart`: The singles' chart object - an instance of the :class:`Chart` class containing the
                singles information and the issue and retrieval dates specific to this chart.
        """
        if self._singles_chart is None:
            self._get_singles_chart()
        return self._singles_chart

    @property
    def singles(self):
        """A ``property`` that returns a list of single entries.

        Returns:
            :py:class:`list`: A :py:class:`list` of :class:`Entry` instances. Each entry describes a single in the chart.
        """
        singles_chart = self.singles_chart
        return singles_chart.entries