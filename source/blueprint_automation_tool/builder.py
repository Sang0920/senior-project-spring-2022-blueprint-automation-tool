"""
File:           builder.py
Description:    main building automation for the project
"""
from color_matcher import color_to_minecraft_dye
from game_automation import AutomationException, GameAutomator
from kivy.logger import Logger
from place_parser import PlaceParser


class PlaceBuilder:
    def build_places(self, reference, places, base_height, block_choice, scale):
        automator = GameAutomator()
        parser = PlaceParser()

        if reference is None:
            raise AutomationException("No reference point is loaded!")
        if places is None:
            raise AutomationException("No places are loaded to build!")

        ref_coords = reference.coordinate_list[0]

        automator.switch_to_game()

        Logger.info("PlaceBuilder: Placing a Gold Block at the Reference Point")
        automator.teleport(0, base_height + 30, 0)
        automator.send_to_chat(f"/setblock 0 {base_height} 0 minecraft:gold_block")

        first_x = first_y = first_z = None
        last_x = last_y = last_z = None
        for i, place in enumerate(places):
            Logger.info(f"PlaceBuilder: Now building {place.name}")
            automator.send_to_chat(f"Now building {place.name}")
            color = color_to_minecraft_dye(place.color)

            if len(place.coordinate_list) == 1:
                block_x, block_y, block_z = parser.convert_to_minecraft(
                    ref_coords.latitude,
                    place.coordinate_list[0].latitude,
                    ref_coords.longitude,
                    place.coordinate_list[0].longitude,
                    place.coordinate_list[0].altitude,
                    scale,
                )
                automator.teleport(block_x, block_y, block_z)
                automator.send_to_chat(
                    f"""/setblock {block_x} {block_y + base_height} {block_z} \
                    minecraft:{color}_{block_choice}"""
                )
            else:
                for j, coordinate in enumerate(place.coordinate_list):
                    block_x, block_y, block_z = parser.convert_to_minecraft(
                        ref_coords.latitude,
                        coordinate.latitude,
                        ref_coords.longitude,
                        coordinate.longitude,
                        coordinate.altitude,
                        scale,
                    )

                    # Draw majority of polygon
                    if j == 0:
                        automator.send_to_chat("//deselect")
                        automator.send_to_chat("//sel convex")
                        automator.teleport(block_x, block_y + base_height + 30, block_z)
                        automator.pos(block_x, block_y + base_height, block_z, 1)
                        first_x = block_x
                        first_y = block_y + base_height
                        first_z = block_z
                    else:
                        automator.pos(block_x, block_y + base_height, block_z, 2)
                        if j == len(place.coordinate_list) - 2:  # Second to last item
                            last_x = block_x
                            last_y = block_y + base_height
                            last_z = block_z
                automator.line(f"minecraft:{color}_{block_choice}")

                # Draw last line if we are building a polygon
                if place.shape == "Polygon":
                    automator.send_to_chat("//deselect")
                    automator.send_to_chat("//sel cuboid")
                    automator.pos(first_x, first_y, first_z, 1)
                    automator.pos(last_x, last_y, last_z, 2)
                    automator.line(f"minecraft:{color}_{block_choice}")

            percent = round((i + 1) / float(len(places)) * 100, 2)

            Logger.info(f"PlaceBuilder: Finished building {place.name}")
            automator.send_to_chat(
                f"Done building {place.name}. Progress: {i + 1}/{len(places)} ({percent}%)"
            )

        Logger.info("PlaceBuilder: Teleporting back to the reference point")
        automator.send_to_chat("//deselect")
        automator.teleport(0, base_height + 100, 0)

        Logger.info("PlaceBuilder: Done!")
