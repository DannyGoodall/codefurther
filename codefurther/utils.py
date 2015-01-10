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

"""The :mod:`utils` module contains utility functions and classes used by the other modules in the suite.

"""
import os

from future.utils import raise_from
from codefurther.errors import CodeFurtherConversionError
from munch import Munch
from six import iteritems


def isolate_path_filename(uri):
    """Accept a url and return the isolated filename component

    Accept a uri in the following format - http://site/folder/filename.ext and return the filename component.

    Args:
        uri (:py:class:`str`): The uri from which the filename should be returned
    Returns:
        file_component (:py:class:`str`): The isolated filename
    """
    # Look for the last slash
    url_parse = uri.rpartition('/')

    # Take everything to the right of the last slash and seperate it on the '.' if it exists, otherwise return the
    # string as is
    if '.' in url_parse[2]:
        file_parse = url_parse[2].rpartition('.')
        file_component = file_parse[0]
    else:
        file_component = url_parse[2]

    return file_component

def get_file_contents_as_text(url_tail, base_folder="tests/resources/{}.json"):
    path = url_tail.replace("/", "")

    resource_file = os.path.normpath(
        base_folder.format(
            path
        )
    )

    # Read the contents of the JSON file as string
    file_text = open(resource_file, mode='rb').read()
    #json_dict = json.loads(file_text.decode())
    #return json_dict
    return file_text.decode()


def request_send_file(request, uri, headers):
    if uri.endswith('-404-'):
        return (400, headers, "")
    filename = isolate_path_filename(uri)
    file_contents = get_file_contents_as_text(filename)
    return (200 if 'status' not in headers else headers['status'], headers, file_contents)


def recurse_structure(thing, use_munch=True, convert=None):
    """Recursively convert any dicts in a thing to Munch types.

    The any iterables in ``thing`` will be walked along, and any :py:class:`dict` types will be converted to ``Munch``
    types.

    As the ``thing`` is being walked, if a :py:class:`dict` key is found in the ``conversion`` :py:class:`dict`, the
    :py:func:`recurse_structure` function will attempt to convert the key to the correspond class in the convert
    :py:class:`dict`. For example, if the convert :py:class:`dict` contains::

        {
            "float_age": int
        }

    Then, if the key "float_age" is found whilst walking the ``thing``, a conversion will be attempted like so::

        key = "float_age"
        new_value = convert[key]( thing[key] )

    If an exception is raised during the conversion, a Top40ConversionError is raised.

    Args:
        thing (Any type): The thing to be recursively parsed and/or converted.
        use_munch (:py:class:`bool`): Should dicts be replaced with Munch types?
        convert (:py:class:`dict` or :py:class:`None`): A dictionary of key and type pairs to be converted.

    Returns:
        The converted thing (Any tupe)

    Raises:
        Top40ConversionError: if a conversion from the ``convert`` :py:class:`dict` fails.
    """

    if convert is None:
        convert = {}

    # What are we dealing with?
    if isinstance(thing, list):
        new_thing = []
        for x in thing:
            new_thing.append(
                recurse_structure(x, use_munch=use_munch, convert=convert)
            )
        return new_thing
    elif isinstance(thing, dict):
        new_thing = {} if not use_munch else Munch()
        for k, v in iteritems(thing):
            # Do we need to convert this thing?
            if k in convert:
                try:
                    v = convert[k](v)
                except TypeError as e:
                    raise_from(
                        CodeFurtherConversionError(
                            "A TypeError occurred trying to convert a dictionary value. "
                            "Key: '{}', Value: {}, Converting to: {}".format(
                                str(k),
                                str(v),
                                str(convert[k])
                            )
                        ),
                        e
                    )

            new_thing[k] = recurse_structure(v, use_munch=use_munch, convert=convert)
        return new_thing
    else:
        return thing

