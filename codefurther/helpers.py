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
"""Helper functions and classes for the codefurther package.

.. moduleauthor:: Danny Goodall <danny@onebloke.com>

"""
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
from future.standard_library import hooks
with hooks():
    from urllib.parse import unquote
import os
import re
import codecs

# This code from here: http://stackoverflow.com/a/24519338/1300916
ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)

def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


class FileSpoofer:
    def __init__(self, api_base="http://cflyricsserver.herokuapp.com/lyricsapi", base_folder="tests/resources/lyricsapi", extension=".json"):
        self.api_base = api_base
        self.base_folder = base_folder
        self.extension = extension
        self.base_folder_fmt = base_folder+"{}"+extension if base_folder.endswith("/") else base_folder+"/{}"+extension

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

        # Remove any URL ? parameters
        if '?' in file_component:
            file_component = file_component.rpartition('?')[0]

        #: Remove URL encoding
        file_component = unquote(file_component)

        #: Remove any spaces in the filename
        file_component = file_component.replace(' ','')

        return file_component

    def get_file_contents_as_text(self, url_tail):
        #path = url_tail.replace("/", "")

        resource_file = os.path.normpath(
            self.base_folder_fmt.format(
                url_tail
            )
        )

        # Read the contents of the JSON file as string
        try:
            file_text = open(resource_file, encoding="utf-8").read()
            #file_text = open(resource_file, 'rb').read()
        except Exception as e:
            print("An error occurred",e)

        # json_dict = json.loads(file_text.decode())
        # return json_dict

        # Let's check for unicode escape characters
        #file_text = file_text.decode('unicode-escape').encode('utf-8')
        #file_text = decode_escapes(file_text)

        return file_text

    def request_send_file(self, request, uri, headers):
        if '-404-' in uri:
            return (404, headers, "")
        filename = self.isolate_path_filename(uri)
        file_contents = self.get_file_contents_as_text(filename)
        return 200 if 'status' not in headers else headers['status'], headers, file_contents

