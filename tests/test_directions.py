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
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

from codefurther.errors import CodeFurtherHTTPError, CodeFurtherConnectionError
from six import string_types, PY2, PY3
from future.standard_library import hooks
with hooks():
    from urllib.parse import unquote

import unittest
from codefurther.helpers import FileSpoofer
from codefurther.directions import GetDirections

from expects import *
import types
import httpretty
from codefurther import lyrics, errors, utils

class TestPatchedDirections(unittest.TestCase):
    def setUp(self):
        self.file_spoofer = FileSpoofer(
            "https://maps.googleapis.com/maps/api/directions",
            "tests/resources/directions",
            extension=".json"
        )


    def tearDown(self):
        pass

    @httpretty.activate
    def test_should_fail_if_api_response_format_incorrect_for_get_directions(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://maps.googleapis.com/maps/api/directions/json",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        directions = GetDirections("Eastleigh", "Winchester", "Walking")

        expect(directions.found).to(be(True))
        expect(directions.heading).to(be_a(string_types))
        expect(directions.footer).to(be_a(string_types))

    @httpretty.activate
    def test_should_fail_if_steps_not_returned_correctly(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://maps.googleapis.com/maps/api/directions/json",
            body=self.file_spoofer.request_send_file,
            content_type='text/json',
            status=200
        )

        directions = GetDirections("Eastleigh", "Winchester", "Walking")
        expect(directions.steps).to(be_a(types.GeneratorType))
        expect(directions.heading).to(contain("These are the steps for the (Walking) journey from Southampton, Southampton, UK to Winchester, Winchester, Hampshire, UK."))
        expect(directions.footer).to(contain("Map data ©2015 Google"))

        for count, step in enumerate(directions.steps):
            print(step)
            expect(step).to(be_a(string_types))

        # We should see at least 1 step
        expect(count).to(be_above(0))
