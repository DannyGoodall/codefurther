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
from codefurther.errors import CodeFurtherHTTPError, CodeFurtherConnectionError
from six import string_types, PY2, PY3
import unittest
from codefurther.helpers import FileSpoofer

__author__ = 'User'

from expects import *
import httpretty
from codefurther import lyrics


class TestPatchedLyrics(unittest.TestCase):
    def setUp(self):
        self.file_spoofer = FileSpoofer(
            "http://cflyricsserver.herokuapp.com/lyricsapi",
            "tests/resources/lyricsapi",
            extension=".json"
        )
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

        data = self.lyrics_machine.song_lyrics("billy bragg","days like these")

        expect(data).to(be_a(list))

    @httpretty.activate
    def test_should_fail_if_malformed_json_response_not_trapped_for_song_lyrics(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/lyrics/billy bragg/malformed",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        def callback():
            return self.lyrics_machine.song_lyrics("billy bragg","malformed")

        expect(callback).to(raise_error(ValueError))

    @httpretty.activate
    def test_should_fail_if_api_response_format_incorrect_for_artist_songs(self):

        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/songs/billy bragg",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        data = self.lyrics_machine.artist_songs("billy bragg")

        expect(data).to(be_a(list))

    @httpretty.activate
    def test_should_fail_if_malformed_json_response_not_trapped_for_artist_songs(self):

        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/songs/malformed",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        def callback():
            return self.lyrics_machine.artist_songs("malformed")

        expect(callback).to(raise_error(ValueError))

    @httpretty.activate
    def test_should_fail_if_api_response_format_incorrect_for__artist_search(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/search/billy bragg",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        data = self.lyrics_machine._artist_search("billy bragg")

        expect(data).to(be_a(dict))
        expect(data['artist']).to(equal("Billy Bragg"))
        expect(data['url']).to(equal("http://lyrics.wikia.com/Billy_Bragg"))


    @httpretty.activate
    def test_should_fail_if_api_response_format_incorrect_for_artist_search(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/search/billy bragg",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        data = self.lyrics_machine.artist_search("billy bragg")

        expect(data).to(be_a(string_types))
        expect(data).to(equal("Billy Bragg"))


    @httpretty.activate
    def test_should_fail_if_malformed_json_response_not_trapped_for_artist_search(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/search/malformed",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        def callback():
            return self.lyrics_machine.artist_search("malformed")

        expect(callback).to(raise_error(ValueError))

    @httpretty.activate
    def test_should_fail_if_list_type_not_returned_for_song_lyrics(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/lyrics/billy bragg/days like these",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        def callback():
            data = self.lyrics_machine.song_lyrics("billy bragg", "days like these")
            return data

        expect(callback()).to(be_a(list))

    @httpretty.activate
    def test_should_fail_if_list_type_not_returned_for_songs(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/songs/billy bragg",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        def callback():
            data = self.lyrics_machine.artist_songs("billy bragg")
            return list(data)

        expect(callback()).to(be_a(list))

    def test_should_fail_if_null_artist_passed_to_artist_songs(self):

        def callback_none():
            return self.lyrics_machine.artist_songs(None)

        def callback_null():
            return self.lyrics_machine.artist_songs("")


        expect(callback_none).to(raise_error(ValueError))
        expect(callback_null).to(raise_error(ValueError))


    def test_should_fail_if_null_artist_and_title_passed_to_song_lyrics(self):

        def callback_none():
            return self.lyrics_machine.song_lyrics(None,None)


        def callback_null():
            return self.lyrics_machine.song_lyrics("","")


        expect(callback_none).to(raise_error(ValueError))
        expect(callback_null).to(raise_error(ValueError))


    def test_should_fail_if_null_artist_passed_to_artist_search(self):

        def callback_none():
            return self.lyrics_machine.artist_search(None)


        def callback_null():
            return self.lyrics_machine.artist_search("")


        expect(callback_none).to(raise_error(ValueError))
        expect(callback_null).to(raise_error(ValueError))

    @httpretty.activate
    def test_should_fail_if_http_error_not_handled(self):

        def callback():
            return self.lyrics_machine.artist_songs('-404-')

        httpretty.register_uri(
            httpretty.GET,
            "http://cflyricsserver.herokuapp.com/lyricsapi/songs/-404-",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        expect(callback).to(raise_error(CodeFurtherHTTPError))


    def test_should_fail_if_connection_error_not_received(self):

        def callback():
            return self.lyrics_machine._get_json_response('asdasdasdasd')

        # It appears that there is a difference between PY3 and PY2 in the way connection error is handled.
        # TODO Looking into difference in connection error between PY2 and PY3
        if PY3:
            expect(callback).to(raise_error(CodeFurtherConnectionError))
        else:
            expect(callback).to(raise_error(CodeFurtherHTTPError))

