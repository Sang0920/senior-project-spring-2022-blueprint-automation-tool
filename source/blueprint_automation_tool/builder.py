"""
File:           builder.py
Description:    main building automation for the project
"""
import time

import constants
from color_matcher import color_to_minecraft_dye
from game_automation import AutomationException, GameAutomator
from kivy.logger import Logger
from place_parser import PlaceParser


class PlaceBuilder:
    def build_places(self, reference, places, base_height, block_choice, scale):
        """Builds the given places in the minecraft world

        Args:
            reference: The central reference point of the world
            places: The places to be built
            base_height: The height that building will start at
            block_choice: The block to be used for building
            scale: The scale of the build
        """
        automator = GameAutomator()
        parser = PlaceParser()

        if reference is None:
            raise AutomationException("No reference point is loaded!")
        if places is None:
            raise AutomationException("No places are loaded to build!")

        ref = reference.coordinate_list[0]

        automator.switch_to_game()
        Logger.info("PlaceBuilder: Forcing character into creative mode")
        automator.send_to_chat("/gamemode spectator")
        automator.send_to_chat("/gamemode creative")

        sum_corners = 0
        total_corners_processed = 0
        for place in places:
            sum_corners += len(place.coordinate_list)

        for i, place in enumerate(places):
            color = color_to_minecraft_dye(place.color)
            start_time = time.time()

            Logger.info(f"PlaceBuilder: ({i+1}/{len(places)}) Now Building: {place.name}")
            place_text = (
                '/tellraw @p ["",{"text":"('
                + str(i + 1)
                + "/"
                + str(len(places))
                + ') Now Building: ","color":"white"},{"text":"'
                + place.name
                + '","bold":true,"color":"'
                + constants.DYE_TO_CHAT[color]
                + '"}]'
            )

            # Teleport to the first coorindate in the place
            automator.send_to_chat(place_text)
            block_x, block_y, block_z = parser.convert_to_minecraft(
                ref.latitude,
                place.coordinate_list[0].latitude,
                ref.longitude,
                place.coordinate_list[0].longitude,
                place.coordinate_list[0].altitude,
                scale,
            )
            automator.teleport(block_x, block_y + 50, block_z)

            # If length is 1, then just place a single block
            if len(place.coordinate_list) <= 0:
                raise AutomationException(f"{place.name} has no coordinates within it!")
            if len(place.coordinate_list) == 1:
                automator.send_to_chat(
                    f"""/setblock {block_x} {block_y + base_height} {block_z} \
                    minecraft:{color}_{block_choice}"""
                )
            else:
                # Draw polygon or path
                raised_points = []
                if len(place.coordinate_list) > 2:
                    automator.send_to_chat("//deselect")
                    automator.send_to_chat("//sel convex")
                    automator.pos(block_x, block_y + base_height, block_z, 1)

                    for c in place.coordinate_list[1:]:
                        x, y, z = parser.convert_to_minecraft(
                            ref.latitude,
                            c.latitude,
                            ref.longitude,
                            c.longitude,
                            c.altitude,
                            scale,
                        )

                        # Add raised points to draw columns later
                        if y > 0:
                            raised_points.append((x, y, z))

                        automator.pos(x, y + base_height, z, 2)
                    automator.line(f"minecraft:{color}_{block_choice}")

                # Draw a line between the last two points
                first_x, first_y, first_z = parser.convert_to_minecraft(
                    ref.latitude,
                    place.coordinate_list[-1].latitude,
                    ref.longitude,
                    place.coordinate_list[-1].longitude,
                    place.coordinate_list[-1].altitude,
                    scale,
                )
                last_x, last_y, last_z = parser.convert_to_minecraft(
                    ref.latitude,
                    place.coordinate_list[-2].latitude,
                    ref.longitude,
                    place.coordinate_list[-2].longitude,
                    place.coordinate_list[-2].altitude,
                    scale,
                )
                automator.send_to_chat("//deselect")
                automator.send_to_chat("//sel cuboid")
                automator.pos(first_x, first_y + base_height, first_z, 1)
                automator.pos(last_x, last_y + base_height, last_z, 2)
                automator.line(f"minecraft:{color}_{block_choice}")

                # Draw columns, if necessary
                if raised_points:
                    for point in raised_points:
                        automator.send_to_chat("//deselect")
                        automator.send_to_chat("//sel cuboid")
                        automator.pos(point[0], point[1] + base_height, point[2], 1)
                        automator.pos(point[0], base_height, point[2], 2)
                        automator.line(f"minecraft:{color}_{block_choice}")

            end_time = time.time()
            Logger.info(f"PlaceBuilder: {place.name} Time (s): {end_time - start_time}")
            Logger.info(f"PlaceBuilder: {place.name} Corners: {len(place.coordinate_list)}")

            total_corners_processed += len(place.coordinate_list)
            percent = round((total_corners_processed) / float(sum_corners) * 100, 3)
            chat_color = self._get_chat_color(percent)

            Logger.info(f"PlaceBuilder: Progress: {percent}%")
            automator.send_to_chat(
                '/title @p title ["",{"text":" Progress: '
                + str(percent)
                + '%","color":"'
                + chat_color
                + '"},{"text":" "}]'
            )

        Logger.info("PlaceBuilder: Teleporting back to the reference point")
        automator.send_to_chat("//deselect")
        automator.teleport(0, base_height + 100, 0)
        automator.send_to_chat("/gamemode spectator")

        Logger.info("PlaceBuilder: Done!")

    def _get_chat_color(self, percent):
        """Coverts a percentage value to a color to use in the game chat

        Args:
            percent: Percentage from 0% to 100%

        Returns:
            the color to use in chat for progress
        """
        if percent < 20.0:
            return "dark_red"
        elif percent < 40.0:
            return "red"
        elif percent < 60.0:
            return "gold"
        elif percent < 80.0:
            return "yellow"
        elif percent < 100.0:
            return "green"
        else:
            return "dark_green"
