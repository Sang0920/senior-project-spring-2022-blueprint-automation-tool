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

last_block_x = None
last_block_z = None
for coordinate in found_places[0].coordinate_list:
    block_x, _, block_z = p.convert_to_minecraft(ref_place.latitude, coordinate.latitude, ref_place.longitude, coordinate.longitude)
    print(floor(block_x), floor(block_z))
    if last_block_x is not None:
        g.teleport(last_block_x, -59, last_block_z)
        g.pos1(last_block_x, -60, last_block_z)
        g.teleport(block_x, -59, block_z)
        g.pos2(block_x, -60, block_z)
        g.line("minecraft:red_wool")
    last_block_x = block_x
    last_block_z = block_z
