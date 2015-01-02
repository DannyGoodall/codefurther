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
from codefurther.errors import CodeFurtherHTTPError
from codefurther.utils import request_send_file

__author__ = 'User'

from expects import *
import requests
import requests_cache
import httpretty
from codefurther import top40


class TestPatchedRequestsCached(unittest.TestCase):

    def setUp(self):
        self.top40 = top40.Top40(cache_duration=3600)

        #: Clear the cache, otherwise if a Python 2 test is run after a Python 3 test, then
        #: incorrect pickle format errors can occur
        requests_cache.clear()

    def tearDown(self):
        requests_cache.clear()

    @httpretty.activate
    def test_should_fail_if_second_get_is_not_cached(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://ben-major.co.uk/labs/top40/api/albums",
            body=request_send_file,
            content_type='text/json',
            status=200
        )

        response = requests.get("http://ben-major.co.uk/labs/top40/api/albums")
        response = requests.get("http://ben-major.co.uk/labs/top40/api/albums")

        expect(response).to(have_property("from_cache"))
        expect(response.from_cache).to(be(True))

    @httpretty.activate
    def test_should_fail_if_cache_is_not_turned_off_and_on_properly(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://ben-major.co.uk/labs/top40/api/albums",
            body=request_send_file,
            content_type='text/json',
            status=200
        )

        #: Clear the cache, so that no cached reads are present
        requests_cache.clear()

        #: Turn the cache off
        self.top40.reset_cache(None)

        #: Make a request, but this should not find its way into the cache
        response = requests.get("http://ben-major.co.uk/labs/top40/api/albums")

        expect(response).to(not_(have_property("from_cache")))

        #: Turn cache on
        self.top40.reset_cache(3600)

        #: Prime the cache
        response = requests.get("http://ben-major.co.uk/labs/top40/api/albums")

        #: The first read should not have come from the cache
        expect(response.from_cache).to(be(False))

        #: This time it should be from the cache
        response = requests.get("http://ben-major.co.uk/labs/top40/api/albums")

        expect(response).to(have_property("from_cache"))
        expect(response.from_cache).to(be(True))


class TestPatchedRequestsNoCache(unittest.TestCase):

    def setUp(self):
        self.top40 = top40.Top40(cache_duration=None)

    def tearDown(self):
        pass

    @httpretty.activate
    def test_should_fail_if_500_status_error_not_returned(self):
        def callback():
            data = self.top40._get_data('/albums')
            return data

        httpretty.register_uri(
            httpretty.GET,
            "http://ben-major.co.uk/labs/top40/api/albums",
            body=request_send_file,
            content_type='text/json',
            status=500
        )

        expect(callback).to(raise_error(CodeFurtherHTTPError))

    @httpretty.activate
    def test_should_fail_if_response_type_is_not_a_dict_albums(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://ben-major.co.uk/labs/top40/api/albums",
            body=request_send_file,
            content_type='text/json'
        )

        data = self.top40._get_data('/albums')
        expect(data).to(be_a(dict))

    @httpretty.activate
    def test_should_fail_if_response_type_is_not_a_dict_singles(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://ben-major.co.uk/labs/top40/api/singles",
            body=request_send_file,
            content_type='text/json'
        )

        data = self.top40._get_data('/singles')
        expect(data).to(be_a(dict))


    @httpretty.activate
    def test_should_fail_if_url_is_not_valid(self):
        def callback():
            data = self.top40._get_data("-404-")

        httpretty.register_uri(
            httpretty.GET,
            "http://ben-major.co.uk/labs/top40/api/-404-",
            body=request_send_file,
            content_type='text/json'
        )

        expect(callback).to(raise_error(CodeFurtherHTTPError))


    @httpretty.activate
    def test_should_fail_if_models_are_not_populated_correctly_albums(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://ben-major.co.uk/labs/top40/api/albums",
            body=request_send_file,
            content_type = 'text/json'
        )

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

    @httpretty.activate
    def test_should_fail_if_models_are_not_populated_correctly_singles(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://ben-major.co.uk/labs/top40/api/singles",
            body=request_send_file,
            content_type = 'text/json'
        )

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


class TestUnpatchedTop40GetData(unittest.TestCase):

    def setUp(self):
        self.top40 = top40.Top40()

    def tearDown(self):
        pass

    def test_should_fail_if_get_data_if_url_not_passed(self):
        def callback():
            data = self.top40._get_data()

        expect(callback).to(raise_error(TypeError))



