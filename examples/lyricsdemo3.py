# -*- coding: utf-8 -*-
#
# Copyright 2014 Danny Goodall
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the Lice  nse.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function, unicode_literals
__author__ = 'Danny Goodall'
from codefurther.lyrics import Lyrics

lyrics_machine = Lyrics()

song_list = lyrics_machine.artist_songs("billy bragg", all_details=True)

for count, song_details in enumerate(song_list):
    print(
        "{:4}. {:40} {:50} {:50} ".format(
            count+1,
            song_details['song'],
            song_details['url'],
            song_details['title']
        )
    )

