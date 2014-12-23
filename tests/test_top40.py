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
from codefurther import top40, errors, utils
import json

def fake_get_data(instance, url, params=None, convert=None):
    """
    A stub for get_data that returns a json responses from the filesystem.
    """
    # Map path from url to a file
    path = url.replace("/", "")
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
        self.patcher = mock.patch('codefurther.top40.Top40._get_data', fake_get_data)
        self.patcher.start()
        self.top40 = top40.Top40()

    def tearDown(self):
        self.patcher.stop()

    def test_should_fail_if_dict_type_not_returned_for_albums(self):
        def callback():
            data = self.top40._get_data("/albums/")
            return data

        expect(callback()).to(be_a(dict))

    def test_should_fail_if_dict_type_not_returned_for_singles(self):
        def callback():
            data = self.top40._get_data("/singles/")
            return data

        expect(callback()).to(be_a(dict))

    def test_should_fail_if_albums_chart_models_not_initiated_correctly(self):
        """
          "date": 1416700800,
          "retrieved": 1417260657,
          "entries": [
            {
              "position": 1,
              "previousPosition": 0,
              "numWeeks": 1,
              "artist": "One Direction",
              "title": "FOUR",
              "change": {
                "direction": "down",
                "amount": 1,
                "actual": -1
              }
            },
        """

        albums_chart = self.top40.albums_chart
        albums_entries = self.top40.albums

        expect(albums_entries).to(be_a(list))
        expect(albums_entries).to(equal(albums_chart.entries))

        expect(albums_chart).to(be_a(top40.Chart))
        expect(albums_chart.date).to(equal(1416700800))
        expect(albums_chart.retrieved).to(equal(1417260657))

        expect(albums_chart.entries).to(be_a(list))

        expect(albums_chart.entries[0]).to(be_an(top40.Entry))
        expect(albums_chart.entries[0].change).to(be_a(top40.Change))
        expect(albums_chart.entries[0].change.direction).to(equal("down"))
        expect(albums_chart.entries[0].change.amount).to(equal(1))
        expect(albums_chart.entries[0].change.actual).to(equal(-1))
        expect(albums_chart.entries[0].position).to(equal(1))
        expect(albums_chart.entries[0].previousPosition).to(equal(0))
        expect(albums_chart.entries[0].numWeeks).to(equal(1))
        expect(albums_chart.entries[0].artist).to(equal("One Direction"))
        expect(albums_chart.entries[0].title).to(equal("FOUR"))

    def test_should_fail_if_albums_entries_model_not_initiated_correctly(self):
        pass



    def test_should_fail_if_singles_chart_model_not_initiated_correctly(self):
        """
          "date": 1416700800,
          "retrieved": 1417260648,
          "entries": [
            {
              "position": 1,
              "previousPosition": 0,
              "numWeeks": 1,
              "artist": "Band Aid 30",
              "title": "Do They Know It's Christmas? (2014)",
              "change": {
                "direction": "down",
                "amount": 1,
                "actual": -1
              }
            },
        """

        singles_chart = self.top40.singles_chart
        single_entries = self.top40.singles

        expect(single_entries).to(be_a(list))
        expect(single_entries).to(equal(singles_chart.entries))

        expect(singles_chart).to(be_a(top40.Chart))
        expect(singles_chart.date).to(equal(1416700800))
        expect(singles_chart.retrieved).to(equal(1417260648))

        expect(singles_chart.entries).to(be_a(list))

        expect(singles_chart.entries[0]).to(be_an(top40.Entry))

        expect(singles_chart.entries[0].position).to(equal(1))
        expect(singles_chart.entries[0].previousPosition).to(equal(0))
        expect(singles_chart.entries[0].numWeeks).to(equal(1))
        expect(singles_chart.entries[0].artist).to(equal("Band Aid 30"))
        expect(singles_chart.entries[0].title).to(equal("Do They Know It's Christmas? (2014)"))

        expect(singles_chart.entries[0].change).to(be_a(top40.Change))
        expect(singles_chart.entries[0].change.direction).to(equal("down"))
        expect(singles_chart.entries[0].change.amount).to(equal(1))
        expect(singles_chart.entries[0].change.actual).to(equal(-1))




class TestUnpatchedTop40GetData:

    def setUp(self):
        self.top40 = top40.Top40()

    def tearDown(self):
        pass

    def test_should_fail_if_get_data_if_url_not_passed(self):
        def callback():
            data = self.top40._get_data()

        expect(callback).to(raise_error(TypeError))

    def test_should_fail_if_url_is_not_valid(self):
        def callback():
            data = self.top40._get_data("A")

        expect(callback).to(raise_error(errors.CodeFurtherHTTPError))


class TestObjectForMunchTest:
    def __init__(self, value):
        self.inner_value = value


class TestRecurseStructure:

    def __init__(self):
        self.structure = [
            {
                "list": [
                    0, 1, 2, 3, 4,
                    {
                        "int": int(2),
                        "string": str("hello"),
                        "float": float(9.99),
                        "object": TestObjectForMunchTest({1, 1, 2, 3}),
                        "list": [
                            0, 1, 2, 3, 4, {
                                "int": int(9),
                                "string": str("world"),
                                "float": float(2.2),
                                "object": TestObjectForMunchTest({2, 2, 3, 4}),
                                "list": [
                                    0, 1, 2, 3, 4
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        self.converted = utils.recurse_structure(self.structure)

    def test_should_pass_with_munch_dot_access(self):

        expect(self.converted[0].list[5]["object"].inner_value).to(equal({1, 2, 3}))
        expect(self.converted[0].list[5].list[5].object.inner_value).to(equal({2, 3, 4}))

        expect(self.converted[0].list[5]["int"]).to(equal(int(2)))
        expect(self.converted[0].list[5].list[5].int).to(equal(int(9)))

        expect(self.converted[0].list[5]["string"]).to(equal(str("hello")))
        expect(self.converted[0].list[5].list[5].string).to(equal(str("world")))

        expect(self.converted[0].list[5]["float"]).to(equal(float(9.99)))
        expect(self.converted[0].list[5].list[5].float).to(equal(float(2.2)))

        expect(self.converted[0].list[5].list[5].list).to(equal([0, 1, 2, 3, 4]))

    def test_should_fail_with_conversion_error(self):
        def callback():
            converted = utils.recurse_structure(
                self.structure,
                convert={
                    "int": dict
                }
            )

        expect(callback).to(raise_error(errors.CodeFurtherConversionError))

    def test_should_pass_when_converting_int_to_float(self):
        def callback():
            converted = utils.recurse_structure(
                self.structure,
                convert={
                    "int": float
                }
            )
            return converted

        expect(callback()[0].list[5].int).to(equal(float(int(2))))
        expect(callback()[0].list[5].list[5].int).to(equal(float(int(9))))