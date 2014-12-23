from __future__ import print_function
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

"""The ``CFLyrics`` module contains the high level classes that are used to package the returned data such as
:py:class:`Entry`, :py:class:`Chart` and :py:class:`Change`.

In addition the :py:class:`CFLyrics` class provides the main external interface into the module. Once an instance of the
:py:class:`CFLyrics` class has been instantiated it can be used to return data from the remote API to the called program::

    from codefurther.lyrics import Lyrics

    lyrics_machine = Lyrics()
    for lyric_line in lyrics_machine.song_lyrics("billy bragg", "days like these"):
        print( lyric_line )
"""

__author__ = 'Danny Goodall'

import requests
import requests.exceptions
from nap.url import Url
from codefurther.errors import CodeFurtherConnectionError, CodeFurtherConversionError, CodeFurtherHTTPError, \
    CodeFurtherReadTimeoutError


class LyricsAPI(Url):
    """Provides the physical connection to the API for the Lyrics object.

    This is the route into API and is a subclass of nap.Url. It provides the get method that carries out the request.get
    method for the chart API.

    This class overrides the :func:`LyricsAPI.get` and :func:`LyricsAPI.after_request` methods in the base class. The
    response returned from the :class:`nap.Url` class is recursively parsed to convert any embedded
    :class:`dict` objects, to :class:`~munch.Munch` types. This is to allow `dot access` to the members of the response,
    as well as using the traditional dict['key'] access.

    Attributes:
        convert (dict): contains none or more key, value pairs.
    """

    def after_request(self, response):
        if response.status_code != 200:
            response.raise_for_status()

        # Now turn the dicts in the Json response into Munch types so that
        # they can be accessed using .notation

        return response.json()


class Lyrics(object):
    """ Provides the programmer with properties that return lyrics from the Wikia site.

    The programmer creates an instance of this object, and then uses the exposed properties to access the data about
    the lyrics.

    Attributes:
        error_format (:py:class:`str`): The format string to be used when creating error messages.
        bad_response (:py:class:`str`): The text to be used in the raised error if the server response is unexpected.
    """
    error_format = "Received an error whist reading from {}: Returned code: {}"
    bad_response = "The server returned a badly assembled response."

    def __init__(self, base_url="http://cflyricsserver.herokuapp.com/lyricsapi/"):
        """Creates and returns the object instance.

        Args:
            base_url (str): The base url of the remote API before the specific service details are appended.
                For example, the base url might be "a.site.com/api/", and the service "/songs/", when appended to the
                base url, creates the total url required to access the album data.
        Returns:
            Lyrics (:py:class:`Lyrics`): The Lyrics model instance.
        """
        self.api = LyricsAPI(base_url)


    def song_lyrics(self, artist, title):
        """Return a list of string lyrics for the given artist and song title.

        Args:
            artist: (:py:class:`str`) The name of the artist for the song being looked up.
            title: (:py:class:`str`) The name of the song being looked up.
        Returns:
            (:py:class:`list`) of (:py:class:`str`) one for each lyric line in the song. Blank lines can
                be returned to space verses from the chorus, etc.
        """
        if artist is None or not artist or title is None or not title:
            raise ValueError("The get_song_lyrics method needs both the artist and the title of the song you are "
                             "looking for to be specified.")
        json_response = self.api.get(
            'lyrics/{}/{}'.format(
                artist,
                title
            )
        )
        if "lyrics" not in json_response:
            raise ValueError(self.bad_response)

        # Return the :py:class:`list` of lyric strings
        return json_response['lyrics']


    def _artist_songs(self, artist):
        if artist is None or not artist:
            raise ValueError("The get_artist_songs method was expecting an artist to be supplied, but none was found.")

        json_response = self.api.get(
            'songs/{}'.format(
                artist
            )
        )
        if 'songs' not in json_response:
            raise ValueError(self.bad_response)

        return json_response

    def artist_songs(self, artist, all_details=False):
        """Returns a generator that yields song titles for the given artist.

        If the `all_details` flag is set to `True`, then a :py:class:`dict` is returned that contains. Returns an empty generator if no songs were found for the specified artist.

        Args:
            artist: (:py:class:`str`) The name of the artist for the song being looked up.
            all_title: (:py:class:`str`) The name of the song being looked up.
        Yields:
            lyric: (:py:class:`str`): one for each lyric line in the song. Expect blank lines to be returned to returned to space verses from the chorus, etc.
        """

        json_response = self._artist_songs(artist)

        for song_detail in json_response['songs']:
            if all_details:
                yield song_detail
            else:
                yield song_detail['song']

    def _artist_search(self, artist):
        if artist is None or not artist:
            raise ValueError("The search_for_artist method was expecting an artist to be supplied, but none was found.")
        json_response = self.api.get(
            'search/{}'.format(
                artist
            )
        )
        if 'artist' not in json_response:
            raise ValueError(self.bad_response)

        return json_response['artist']

    def artist_search(self, artist):
        artist_details = self._artist_search(artist)
        return artist_details['artist']

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
            message = Lyrics.error_format.format(
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

