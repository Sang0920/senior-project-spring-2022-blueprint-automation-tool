"""
File:           rotunda.py
Description:    test file to check parsing/converting of .kml files

Author(s):      Kevin Green
"""
import os
from math import floor

from game_automation import GameAutomator
from place_parser import PlaceParser

p = PlaceParser()
g = GameAutomator()

_here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(_here, "Rotunda.kml")
found_places = p.parse_place(filename)

ref_place = found_places[0].coordinate_list[0]

g.switch_to_game()

for coordinate in found_places[0].coordinate_list:
    block_x, block_y = p.get_line_length_bearing(
        ref_place.latitude,
        coordinate.latitude,
        ref_place.longitude,
        coordinate.longitude,
    )
    print(floor(block_x), floor(block_y))
    g.send_to_chat(f"/setblock {block_x} 0 {block_y} magenta_wool")
