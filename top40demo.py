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

__author__ = 'Danny Goodall'
from codefurther import top40

import arrow

top40 = top40.Top40()
sep = "-"*132
print(sep)
albums_chart = top40.albums_chart
print("Date of chart: {}. Date of chart download: {}".format(
    arrow.get(albums_chart.date),
    arrow.get(albums_chart.retrieved))
)
albums = top40.albums
for album in albums:
    print("{:4} - {:30}  {:50}  {:6}({:4}) - {:4} weeks in the chart.".format(
        album.position,
        album.artist,
        album.title,
        album.change.direction,
        album.change.actual,
        album.numWeeks
    ))

print(sep)
print(sep)

singles_chart = top40.singles_chart
print("Date of chart: {}. Date of chart download: {}".format(
    arrow.get(singles_chart.date),
    arrow.get(singles_chart.retrieved))
)
singles = top40.singles
for single in singles:
    print("{:4} - {:30}  {:50}  {:6}({:4}) - {:4} weeks in the chart.".format(
        single.position,
        single.artist,
        single.title,
        single.change.direction,
        single.change.actual,
        single.numWeeks
    ))
