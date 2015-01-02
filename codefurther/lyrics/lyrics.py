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
from future.standard_library import hooks

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

# Import urljoin for V2 and V3 - http://python-future.org/compatible_idioms.html
with hooks():
    from urllib.parse import urljoin

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
        self.base_url = base_url

    def _get_json_response(self, service_url):

        full_url = urljoin(
            self.base_url,
            service_url
        )

        try:
            response = requests.get(full_url).json()
        except requests.exceptions.HTTPError as e:
            message = Lyrics.error_format.format(
                service_url,
                e.response.status_code
            )
            print(message)
            raise CodeFurtherHTTPError(message, e.response.status_code)
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout):
            raise CodeFurtherConnectionError("Could not connect to remote server.")
        except requests.exceptions.ReadTimeout:
            raise CodeFurtherReadTimeoutError("The remote server took longer than expected to reply.")
        except Exception as e:
            raise

        return response

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

        service_url = 'lyrics/{}/{}'.format(
            artist,
            title
        )

        json_response = self._get_json_response(service_url)

        if "lyrics" not in json_response:
            raise ValueError(self.bad_response)

        # Return the :py:class:`list` of lyric strings
        return json_response['lyrics']


    def _artist_songs(self, artist):
        if artist is None or not artist:
            raise ValueError("The get_artist_songs method was expecting an artist to be supplied, but none was found.")

        service_url = "songs/{}".format(
            artist
        )

        json_response = self._get_json_response(service_url)

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

        service_url = 'search/{}'.format(
            artist
        )

        json_response = self._get_json_response(service_url)

        if 'artist' not in json_response:
            raise ValueError(self.bad_response)

        return json_response['artist']

    def artist_search(self, artist):
        """Returns the first result of a search for the given artist on Lyrics Wikia.

        **Proceed with a little caution as I'm not completely sure that these results are accurate**.

        Returns a string containing the search result. The actual string returned depends on what the search
        functionality at Lyrics Wikia returns.

        Args:
            artist: (:py:class:`str`) The name of the artist being searched for.
        Returns:
            result: (:py:class:`str`): The result of the search If the string contains a colon ``:``, then it typically
                means that an artist and song has been returned, separated by the colon. If a string is returned without
                a colon, then it likely means that an exact match for the search artist was found.
        """
        artist_details = self._artist_search(artist)
        return artist_details['artist']

