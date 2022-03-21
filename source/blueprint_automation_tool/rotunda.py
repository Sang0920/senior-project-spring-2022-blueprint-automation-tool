"""
File:           rotunda.py
Description:    test file to check parsing/converting of .kml files

Author(s):      Kevin Green
"""
import os
from math import floor

import helpers.color_converter as cc
from game_automation import GameAutomator
from place_parser import PlaceParser

p = PlaceParser()
g = GameAutomator()

_here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(_here, "Rotunda.kml")
found_places = p.parse_place(filename)

ref_place = found_places[0].coordinate_list[0]

color = cc.color_to_minecraft_dye(found_places[0].color)
last_block_x = last_block_z = None

g.switch_to_game()
for coordinate in found_places[0].coordinate_list:
    block_x, _, block_z = p.convert_to_minecraft(ref_place.latitude, coordinate.latitude, ref_place.longitude, coordinate.longitude)
    print(floor(block_x), floor(block_z))
    if last_block_x is not None:
        g.teleport(last_block_x, -59, last_block_z)
        g.pos1(last_block_x, -60, last_block_z)
    else:
        g.teleport(last_block_x, -59, last_block_z)
        g.pos1(block_x, -60, block_z)
    g.teleport(block_x, -59, block_z)
    g.pos2(block_z, -60, block_z)
    g.line(f"minecraft:{color}_wool")
    last_block_x = block_x
    last_block_z = block_z
