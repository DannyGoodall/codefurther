# -*- coding: utf-8 -*-
#
# Copyright 2014 Danny Goodall
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The errors module containing the exceptions that PythonTop40 uses """

__author__ = 'dan'

class CodeFurtherError(Exception):
    """Base class for all exceptions"""
    pass

class CodeFurtherConversionError(TypeError):
    """This is raised when a conversion is specified, but causes an error"""
    pass


class CodeFurtherConnectionError(CodeFurtherError):
    """This is raised when a connection cannot be established to the remote
    server"""
    pass

class CodeFurtherReadTimeoutError(CodeFurtherError):
    """This is raised when an ongoing action takes longer than expected"""
    pass

class CodeFurtherHTTPError(CodeFurtherError):
    """This exception is raised if an HTTP level error was experienced. i.e.
    no physical or connection error, but a web server error was returned."""
    def __init__(self, message, return_code):
        """Create a new instance of the Top40HTTPError exception

        Args:
            message (:py:class:`str`):  The error message text.
            return_code: (:py:class:`int`): The error code for this exception.
        Returns:
            Top40HTTPError (:py:func:`Top40HTTPError`) -- The Exception instance.
        """
        self.message = message
        self.error_code = return_code
        super(CodeFurtherHTTPError, self).__init__(message)

    pass
