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

from setuptools import find_packages, setup
import json
from os import path
from io import open

PACKAGE_DIR = "codefurther"
LONG_DESCRIPTION_FILE = "NULL.rst"
PROJECT_DIR = path.abspath(path.dirname(__file__))
# Get the long description from the relevant file
with open(path.join(PROJECT_DIR, LONG_DESCRIPTION_FILE), encoding='utf-8') as f:
    long_description = f.read()

with open(
        '{}/package_info.json'.format(PACKAGE_DIR)
) as fp:
    _info = json.load(fp)

setup(
    name=_info['name'],
    version=_info['version_full'],
    packages=find_packages(exclude=['tests']),
    url=_info['url'],
    license=_info['license'],
    author=_info['author'],
    author_email=_info['author_email'],
    description=_info['description'],
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'munch==2.0.2',
        'nap==2.0.0',
        'arrow==0.4.4',
        'booby>=0.7.0',
        'six==1.8.0',
        'future==0.14.2'
    ],
    dependency_links=[
    ]
)
