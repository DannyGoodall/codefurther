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

__author__ = 'User'

from expects import *
import mock
from codefurther import lyrics, errors, utils
import json

def fake_get_data(instance, url, params=None, convert=None):
    """
    A stub for get_data that returns a json responses from the filesystem.
    """
    # Remove any spaces in the URL
    path = url.replace(" ", "")
    resource_file = os.path.normpath(
        '../tests/resources/{}.json'.format(
            path
        )
    )
    # Read the contents of the JSON file as string
    file_text = open(resource_file, mode='rb').read()
    json_dict = json.loads(file_text.decode())
    json_munch = utils.recurse_structure(json_dict, convert=convert)
    return json_munch


class TestPatchedTop40GetData:

    def setUp(self):
        self.patcher = mock.patch('codefurther.lyrics.Lyrics._get_data', fake_get_data)
        self.patcher.start()
        self.lyrics_machine = lyrics.Lyrics()

    def tearDown(self):
        self.patcher.stop()

    def test_should_fail_if_api_response_format_incorrect_for_song_lyrics(self):
        def callback():
            data = self.lyrics_machine._get_data("/lyricsapi/lyrics/billy bragg/days like these")
            return data

        expect(callback()).to(be_a(dict))
        expect(callback()['lyrics']).to(be_a(list))

    def test_should_fail_if_api_response_format_incorrect_for_artist_songs(self):
        def callback():
            data = self.lyrics_machine._get_data("/lyricsapi/songs/billy bragg")
            return data

        expect(callback()).to(be_a(dict))
        expect(callback()['songs']).to(be_a(list))


    def test_should_fail_if_api_response_format_incorrect_for_artist_search(self):
        def callback():
            data = self.lyrics_machine._get_data("/lyricsapi/search/billy bragg")
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



