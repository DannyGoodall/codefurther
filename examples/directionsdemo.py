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

from codefurther.directions import GetDirections

# Ask for starting point, destination and the mode of travel
starting_point = input("What is the starting point of your journey? (Southampton) : ")
end_point = input("What is the destination of your journey? (Winchester) :     ")
travel_mode = input("What is mode of travel ? (walking) :                        ")

# Set the defaults for the starting and end points
starting_point = starting_point if starting_point else "southampton, uk"
end_point = end_point if end_point else "winchester, uk"

# Set the travel mode to walking unless it is valid
travel_mode = travel_mode if travel_mode and travel_mode.lower() in GetDirections.valid_modes else "walking"

# Let's create a directions object that we can then interact with
directions = GetDirections(starting_point, end_point, travel_mode)

# Was this route found?
if directions.found:
    # Yes, so let's print out a heading...
    print(directions.heading)

    # Followed by each of the steps...
    for step in directions.steps:
        print(step)

    # Followed by a footer
    print(directions.footer)
else:
    # If the route wasn't found, then explain to the user.
    print("We couldn't find a ({}) route from {}, to {}.".format(travel_mode, starting_point, end_point))

from codefurther.directions import GetDirections

directions = GetDirections("123l123", "345345l34")

print(directions.heading)
for step in directions.steps:
    print(step)
print(directions.footer)
