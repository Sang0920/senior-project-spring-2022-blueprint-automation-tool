"""
File:           game_automation.py
Description:    handles basic automation of Minecraft functions
"""

import re
from time import sleep

import constants
import keyboard
import win32api
import win32con
import window


class AutomationException(Exception):
    """Exception for when game automation fails"""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class GameAutomator:
    """Handles individual parts of automating Minecraft"""

    def __init__(self):
        # Automation elements
        self.keyboard = keyboard.KeyboardHandler()
        self.window = window.WindowHandler()

        # Minecraft information
        self.max_height = 319
        self.min_height = -64

        # Window Objects
        self.is_switched_to_game = False
        self.program_window = self.window.get_current_window()

    def _check_emergency_stop(self):
        """Kills the script if the user holds down the "END" Key

        Raises:
            AutomationException: if the user holds down the "END" key
        """

        if win32api.GetAsyncKeyState(win32con.VK_END):
            raise AutomationException('The "END" key was held down for an emergency stop.')

    def find_minecraft_version(self):
        """Attempts to find the current running version of Minecraft

        Raises:
            AutomationException: if no version of the game can be found

        Returns:
            The version of the game
        """

        game = self.window.find_window(r"Minecraft.*[0-9]+\.[0-9]+.*", limit=1)
        if game:
            game = game[0]
            version = re.findall(r"[0-9]+\.[0-9]+", game.title)[0]
            if version in constants.SUPPORTED_MINECRAFT_VERSIONS:
                if version != "1.18":
                    self.max_height = 256
                    self.min_height = 0
                return version

        # Raise exception if game was not found or version is not supported
        raise AutomationException("No supported version of the game was found!")

    def switch_to_game(self):
        """Switches to the game window"""

        self._check_emergency_stop()
        game = self.window.find_window(
            r"Minecraft.*[0-9]+\.[0-9]+.*(Singleplayer|Multiplayer)", limit=1
        )
        if game:
            self.window.maximize_window(game[0])
            self.window.set_current_window(game[0])
            sleep(3)
            self.keyboard.press_and_release("esc")
            self.is_switched_to_game = True
        else:
            raise AutomationException(
                """No game was found that was loaded into a world. Please make sure you are loaded \
                    into a world!"""
            )

    def send_to_chat(self, message):
        """Sends a message to the game chat, including commands

        Args:
            message: The text to send to chat

        Raises:
            AutomationException: if the script did not switch to the game
        """

        self._check_emergency_stop()
        if self.is_switched_to_game:
            self.keyboard.press_and_release("t")
            sleep(0.05)
            self.keyboard.paste(message)

            max_attempts = 10
            for i in range(max_attempts):
                self.keyboard.select_all()
                if self.keyboard.copy() == message:
                    break
                elif i == max_attempts - 1:
                    raise AutomationException(f"Unable to send message to chat.\n{message}")
                self.keyboard.press_and_release("backspace")
                self.keyboard.paste(message)
                sleep(0.05)
            self.keyboard.press_and_release("enter")
            sleep(0.1)
        else:
            raise AutomationException(
                "Cannot send messages to chat. The script hasn't switched to the game yet."
            )

    def teleport(self, x, y, z):
        """Teleports the player to the given coordinates

        Args:
            x: X-coordinate in-game
            y: Y-coordinate in-game
            z: Z-coordinate in-game

        Raises:
            AutomationException: if the script did not switch to the game
        """

        self._check_emergency_stop()
        if self.is_switched_to_game:
            self.send_to_chat(f"/tp @p {x} {y} {z} 180 90")
            sleep(2)
        else:
            raise AutomationException(
                "Cannot teleport. The script hasn't switched to the game yet."
            )

    def pos(self, x, y, z, pos=1):
        """Selects the given coordinate with WorldEdit with the given position

        Args:
            x: X-coordinate in-game
            y: Y-coordinate in-game
            z: Z-coordinate in-game

        Raises:
            AutomationException: if the script did not switch to the game
        """

        self._check_emergency_stop()
        if self.is_switched_to_game:
            self.send_to_chat(f"//pos{pos} {x},{y},{z}")
        else:
            raise AutomationException(
                "Cannot select first position. The script hasn't switched to the game yet."
            )

    def line(self, block):
        """Creates a line between two points with World Edit

        Args:
            block: the block to draw the line with

        Raises:
            AutomationException: if the script did not switch to the game
        """

        self._check_emergency_stop()
        if self.is_switched_to_game:
            self.send_to_chat(f"//line {block}")
            sleep(0.1)
        else:
            raise AutomationException(
                "Cannot place the line. The script hasn't switched to the game yet."
            )
