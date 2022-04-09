"""
File:           builder.py
Description:    main building automation for the project
"""

from color_matcher import color_to_minecraft_dye
from game_automation import AutomationException, GameAutomator
from kivy.logger import Logger
from place_parser import PlaceParser


class PlaceBuilder:
    """Build places into the Minecraft Environment"""

    def build_place(self, reference_point, places_file_paths, base_height, block_choice, scale):
        """Build a list of places into the Minecraft Environment

        Args:
            reference_point: The parsed reference point
            places_file_paths: List of file paths of places to build
            base_height: The default y-value to build from
            block_choice: The block to build with
            scale: The scale to build the places at in relation to the reference point
        """

        p = PlaceParser()
        g = GameAutomator()

        # Check to make sure there are places to build in relation to a reference
        if reference_point is None:
            raise AutomationException("No reference point is currently loaded!")
        elif places_file_paths is None:
            raise AutomationException("No places have been loaded to build!")

        # Get the coordinates for the reference place
        ref_place = reference_point.coordinate_list[0]

        g.switch_to_game()

        Logger.info("PlaceBuilder: Placing a gold block at the reference point.")
        g.teleport(0, base_height + 30, 0)
        g.send_to_chat(f"/setblock 0 {base_height} 0 minecraft:gold_block")

        # Build each place file sequentially
        for file in places_file_paths:
            found_places = p.parse_place(file)
            color = color_to_minecraft_dye(found_places[0].color)
            last_block_x = last_block_z = last_alt = None

            Logger.info(f"PlaceBuilder: Now building {found_places[0].name}")

            for coordinate in found_places[0].coordinate_list:

                # Convert geo-coordinate to Minecraft coordinate
                block_x, altitude, block_z = p.convert_to_minecraft(
                    ref_place.latitude,
                    coordinate.latitude,
                    ref_place.longitude,
                    coordinate.longitude,
                    coordinate.altitude,
                    scale,
                )

                # Just place a single block if there has been no previous block
                if last_block_x is not None:
                    mid_x = (last_block_x + block_x) / 2
                    mid_y = ((last_alt + altitude) / 2) + base_height
                    mid_z = (last_block_z + block_z) / 2

                    g.teleport(mid_x, mid_y + 30, mid_z)
                    g.pos(last_block_x, last_alt + base_height, last_block_z, 1)
                    g.pos(block_x, altitude + base_height, block_z, 2)
                    g.line(f"minecraft:{color}_{block_choice}")

                # Otherwise, draw a line
                else:
                    g.teleport(block_x, altitude + base_height + 30, block_z)
                    g.send_to_chat(
                        f"""/setblock {block_x} {altitude + base_height} {block_z} \
                        minecraft:{color}_{block_choice}"""
                    )

                # Build pillars if height is greater than 0 to create a box
                if altitude > 0:
                    g.pos(block_x, altitude + base_height, block_z, 1)
                    g.pos(block_x, base_height, block_z, 2)
                    g.line(f"minecraft:{color}_{block_choice}")

                # Set current block as the last block
                last_block_x = block_x
                last_block_z = block_z
                last_alt = altitude

            Logger.info(f"PlaceBuilder: Finished building {found_places[0].name}.")

        Logger.info("PlaceBuilder: Teleporting back to the reference point.")
        g.teleport(0, base_height + 100, 0)

        Logger.info("PlaceBuilder: Done building!")
