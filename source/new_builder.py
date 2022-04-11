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

        # Placing a Gold Block at the Reference Point
        g.teleport(0, base_height + 30, 0)
        g.send_to_chat(f"/setblock 0 {base_height} 0 minecraft:gold_block")

        for place in places:
            Logger.info(f"PlaceBuilder: Now building {place.name}")
            color = color_to_minecraft_dye(place.color)
            last_block_x = last_block_z = last_block_y = None

            for coordinate in place.coordinate_list:
                block_x, block_y, block_z = parser.convert_to_minecraft(
                    ref_coords.latitude,
                    coordinate.latitude,
                    ref_coords.longitude,
                    coordinate.longitude,
                    coordinate.altitude,
                    scale,
                )

                if len(place.coordinate_list) == 1:
                    automator.teleport(block_x, block_y, block_z)
                    automator.send_to_chat(
                        f"""/setblock {block_x} {block_y + base_height} {block_z} \
                        minecraft:{color}_{block_choice}"""
                    )
                elif last_block_x is not None and last_block_z is not None:
                    mid_x = (last_block_x + block_x) / 2
                    mid_y = ((last_block_y + block_y) / 2) + base_height
                    mid_z = (last_block_z + block_z) / 2

                    automator.teleport(mid_x, mid_y + 30, mid_z)
                    automator.pos(last_block_x, last_block_y + base_height, last_block_z, 1)
                    automator.pos(block_x, block_y + base_height, block_z, 2)
                    automator.line(f"minecraft:{color}_{block_choice}")

                    if block_y > 0:
                        automator.pos(block_x, base_height, block_z, 1)
                        automator.line(f"minecraft: {color}_{block_choice}")

                last_block_x = block_x
                last_block_y = block_y
                last_block_z = block_z

            Logger.info(f"PlaceBuilder: Finished building {place.name}")

        Logger.info("PlaceBuilder: Teleporting back to the reference point")
        automator.teleport(0, base_height + 100, 0)

        Logger.info("PlaceBuilder: Done!")
