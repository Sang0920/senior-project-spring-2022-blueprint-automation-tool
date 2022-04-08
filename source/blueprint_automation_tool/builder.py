"""
File:           rotunda.py
Description:    test file to check parsing/converting of .kml files

Author(s):      Kevin Green
"""
from time import time

from color_matcher import color_to_minecraft_dye
from game_automation import AutomationException, GameAutomator
from place_parser import PlaceParser


class PlaceBuilder:
    def __init__(self):
        pass

    def build_place(self, reference_point, places_file_paths, base_height, block_choice, scale):
        p = PlaceParser()
        g = GameAutomator()

        if reference_point is None:
            raise AutomationException("No reference point is currently loaded!")
        elif places_file_paths is None:
            raise AutomationException("No places have been loaded to build!")

        ref_place = reference_point.coordinate_list[0]

        g.switch_to_game()

        total_start = time()

        print("Placing a gold block at the reference point.")
        g.teleport(0, base_height + 30, 0)
        g.send_to_chat(f"/setblock 0 {base_height} 0 minecraft:gold_block")

        for file in places_file_paths:
            found_places = p.parse_place(file)
            color = color_to_minecraft_dye(found_places[0].color)
            last_block_x = last_block_z = last_alt = None

            print(f"Now building {found_places[0].name}")

            start = time()

            for coordinate in found_places[0].coordinate_list:
                block_x, altitude, block_z = p.convert_to_minecraft(
                    ref_place.latitude,
                    coordinate.latitude,
                    ref_place.longitude,
                    coordinate.longitude,
                    coordinate.altitude,
                    scale,
                )
                if last_block_x is not None:
                    mid_x = (last_block_x + block_x) / 2
                    mid_y = ((last_alt + altitude) / 2) + base_height
                    mid_z = (last_block_z + block_z) / 2

                    g.teleport(mid_x, mid_y + 30, mid_z)
                    g.pos1(last_block_x, last_alt + base_height, last_block_z)
                    g.pos2(block_x, altitude + base_height, block_z)
                    g.line(f"minecraft:{color}_{block_choice}")
                else:
                    g.teleport(block_x, altitude + base_height + 30, block_z)
                    g.send_to_chat(
                        f"""/setblock {block_x} {altitude + base_height} {block_z} \
                        minecraft:{color}_{block_choice}"""
                    )
                last_block_x = block_x
                last_block_z = block_z
                last_alt = altitude

            stop = time()

            print(f"Time Elapsed: {stop - start} seconds")
            print(f"Finished building {found_places[0].name}")

        total_stop = time()

        print("Teleporting back to reference point")
        g.teleport(0, base_height + 100, 0)

        print("Done!")
        print(f"Total Elapsed Time: {total_stop - total_start} seconds")
