"""
File:           rotunda.py
Description:    test file to check parsing/converting of .kml files

Author(s):      Kevin Green
"""
import tkinter
from time import time
from tkinter import filedialog

import helpers.color_converter as cc
from game_automation import GameAutomator
from place_parser import PlaceParser

base_height = -60
block_choice = "concrete"

root = tkinter.Tk()
root.withdraw()

reference_file_path = filedialog.askopenfilename()
places_file_paths = filedialog.askopenfilenames()
print(reference_file_path)
print(places_file_paths)

p = PlaceParser()
g = GameAutomator()

ref_place = p.parse_place(reference_file_path)[0].coordinate_list[0]

g.switch_to_game()

print("Placing a gold block at the reference point.")
g.teleport(0, base_height + 20, 0)
g.send_to_chat(f"/setblock 0 {base_height} 0 minecraft:gold_block")

for file in places_file_paths:
    found_places = p.parse_place(file)
    color = cc.color_to_minecraft_dye(found_places[0].color)
    last_block_x = last_block_z = last_alt = None

    print(f"Now building {found_places[0].name}")

    start = time()

    for coordinate in found_places[0].coordinate_list:
        block_x, altitude, block_z = p.convert_to_minecraft(
            ref_place.latitude, coordinate.latitude, ref_place.longitude, coordinate.longitude
        )
        if last_block_x is not None:
            mid_x = (last_block_x + block_x) / 2
            mid_y = ((last_alt + altitude) / 2) + base_height
            mid_z = (last_block_z + block_z) / 2

            g.teleport(mid_x, mid_y + 20, mid_z)
            g.pos1(last_block_x, last_alt + base_height, last_block_z)
            g.pos2(block_x, altitude + base_height, block_z)
            g.line(f"minecraft:{color}_{block_choice}")
        else:
            g.teleport(block_x, altitude + base_height + 20, block_z)
            g.send_to_chat(f"/setblock {block_x} {altitude + base_height} {block_z} minecraft:{color}_{block_choice}")
        last_block_x = block_x
        last_block_z = block_z
        last_alt = altitude

    stop = time()

    print(f"Time Elapsed: {stop - start} seconds")
    print(f"Finished building {found_places[0].name}")

print("Done!")
