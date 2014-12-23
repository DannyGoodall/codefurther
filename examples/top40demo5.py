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
from codefurther.top40 import Top40

top40 = Top40()
format_string = "| {:5} | {:50} | {:50} | {:8} | {:8} | {:22} |"
up_arrow = "^  "
down_arrow = "  v"

# Print the column headings
print(
    format_string.format(
        "  No.",
        "Title",
        "Artist",
        "   Weeks",
        "Previous",
        "Change since last week"
    )
)

# Print the heading underline
print(
    format_string.format(
        "-----",
        "-----",
        "------",
        "--------",
        "--------",
        "----------------------"
    )
)

albums = top40.albums

for album in albums:

    # Create the string that describes that change since last week
    # If the amount of change since last week's chart is 0, or previous position in the chart was 0 (i.e. it is a new
    # entry to the chart), then we should set the change_text to be empty.
    if album.change.amount == 0:
        change_text = ''
    elif album.previousPosition == 0:
        change_text = '    **NEW ENTRY**'
    else:
        # We now know that there was a change in position since last week

        # We want to use the word place if there is only 1 place change, but if there is more than one place change
        # then we want to use the word places. To do this we will use a Python conditional assignment
        places_text = "place" if album.change.amount == 1 else "places"

        # We want to use the up arrow text if the album has moved up since last week, and the down arrow text if it
        # has moved down. To do this we will also use a Python conditional assignment
        arrow_text = up_arrow if album.change.direction == "up" else down_arrow

        # Now let's build the change_text variable from the three components
        # - The arrow text
        # - The amount of change since last week
        # - The place text - using the correct plural term
        change_text = "{} by {} {}".format(
            arrow_text,
            album.change.amount,
            places_text
        )

    # Print the output using the same format string that we used for the heading and underline
    print(
        format_string.format(
            album.position,
            album.title,
            album.artist,
            album.numWeeks,
            album.previousPosition,
            change_text
        )
    )
