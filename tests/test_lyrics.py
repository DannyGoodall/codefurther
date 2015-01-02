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

import os
import unittest
from codefurther.utils import request_send_file

__author__ = 'User'

from expects import *
import httpretty
from codefurther import lyrics, errors, utils
import json


class FileSpoofer:
    def __init__(self, api_base="http://cflyricsserver.herokuapp.com/lyricsapi", base_folder="tests/resources"):
        self.api_base = api_base
        self.base_folder = base_folder

    def isolate_path_filename(self, uri, api_base=None):
        """Accept a url and return the part that is unique to this request

        Accept a uri in the following format - http://site/folder/filename.ext and return the component part that is
        unique to the request when the base api of http://site/folder has been removed

        Args:
            uri (:py:class:`str`): The uri from which the filename should be returned
            api_base (:py:class:`str`): The new base to use, defaults to self.api_base
        Returns:
            file_component (:py:class:`str`): The isolated path
        """
        # Did we get an api_base
        api_base = api_base if api_base else self.api_base

        # Look for the part after the api_base
        url_parse = uri.lower().rpartition(api_base)

        # Take everything to the right of the api_base
        file_component = url_parse[2]

        return file_component

    def get_file_contents_as_text(self, url_tail):
        path = url_tail.replace("/", "")

        resource_file = os.path.normpath(
            self.base_folder.format(
                path
            )
        )

        # Read the contents of the JSON file as string
        file_text = open(resource_file, mode='rb').read()
        # json_dict = json.loads(file_text.decode())
        # return json_dict
        return file_text.decode()

    def request_send_file(self, request, uri, headers):
        if uri.endswith('-404-'):
            return (400, headers, "")
        filename = self.isolate_path_filename(uri)
        file_contents = self.get_file_contents_as_text(filename)
        return 200 if 'status' not in headers else headers['status'], headers, file_contents


class TestPatchedTop40GetData(unittest.TestCase):
    def setUp(self):
        self.file_spoofer = FileSpoofer()
        self.lyrics_machine = lyrics.Lyrics()

    def tearDown(self):
        pass

    @httpretty.activate
    def test_should_fail_if_api_response_format_incorrect_for_song_lyrics(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/lyrics/billy bragg/days like these",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        def callback():
            data = self.lyrics_machine._get_json_response("lyrics/billy bragg/days like these")
            return data

        expect(callback()).to(be_a(dict))
        expect(callback()['lyrics']).to(be_a(list))

    def test_should_fail_if_api_response_format_incorrect_for_artist_songs(self):
        def callback():
            data = self.lyrics_machine._get_json_response("songs/billy bragg")
            return data

        expect(callback()).to(be_a(dict))
        expect(callback()['songs']).to(be_a(list))


    def test_should_fail_if_api_response_format_incorrect_for_artist_search(self):
        def callback():
            data = self.lyrics_machine._get_json_response("search/billy bragg")
            return data

        expect(callback()).to(be_a(dict))
        expect(callback()['artist']).to(be_a(dict))
        expect(callback()['artist']['artist']).to(equal("Billy Bragg"))
        expect(callback()['artist']['url']).to(equal("http://lyrics.wikia.com/Billy_Bragg"))

    def test_should_fail_if_list_type_not_returned_for_song_lyrics(self):
        def callback():
            data = self.lyrics_machine.song_lyrics("billy bragg", "days like these")
            return data

        expect(callback()).to(be_a(list))

    def test_should_fail_if_list_type_not_returned_for_songs(self):
        def callback():
            data = self.lyrics_machine.artist_songs("billy bragg")
            return [x for x in data]

        expect(callback()).to(be_a(list))



