"""
File:           game_automation.py
Description:    handles basic automation of Minecraft functions

Author(s):      Kevin Green
"""

# Built-In Modules
import re
from time import sleep

# Custom Modules
from helpers import keyboard, window


class AutomationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class GameAutomator:
    def __init__(self):
        # Automation elements
        self.keyboard = keyboard.KeyboardHandler()
        self.window = window.WindowHandler()

        # Minecraft information
        self.supported_mc_versions = [
            "1.12",
            "1.13",
            "1.14",
            "1.15",
            "1.16",
            "1.17",
            "1.18",
        ]
        self.supported_blocks = [
            "wool",
            "terracotta",
            "glazed_terracotta",
            "concrete",
            "concrete_powder",
        ]
        self.max_height = 319
        self.min_height = -64

        # Window Objects
        self.is_switched_to_game = False
        self.program_window = self.window.get_current_window()

    def find_minecraft_version(self):
        game = self.window.find_window(r"Minecraft.*[0-9]+\.[0-9]+.*", limit=1)
        if game:
            game = game[0]
            version = re.findall(r"[0-9]+\.[0-9]+", game.title)[0]
            if version in self.supported_mc_versions:
                if version != "1.18":
                    self.max_height = 256
                    self.min_height = 0
                return version
        # Raise exception if game was not found or version is not supported
        raise AutomationException("No supported version of the game was found!")

    def switch_to_game(self):
        game = self.window.find_window(r"Minecraft.*[0-9]+\.[0-9]+.*(Singleplayer|Multiplayer)", limit=1)
        if game:
            self.window.set_current_window(game[0])
            self.window.maximize_window(game[0])
            sleep(3)
            self.keyboard.press_and_release("esc")
            self.is_switched_to_game = True

    def send_to_chat(self, message):
        if self.is_switched_to_game:
            self.keyboard.press_and_release("t")
            self.keyboard.paste(message)
            self.keyboard.press_and_release("enter")
        else:
            raise AutomationException("Cannot send messages to chat. The script hasn't switched to the game yet.")
        sleep(1)

    def teleport(self, x, y, z, should_use_tppos=False):
        if self.is_switched_to_game:
            if should_use_tppos:
                self.send_to_chat(f"/tppos {x} {y} {z}")
            else:
                self.send_to_chat(f"/tp @p {x} {y} {z} 180 90")
        else:
            raise AutomationException("Cannot teleport. The script hasn't switched to the game yet.")

    def pos1(self, x, y, z):
        if self.is_switched_to_game:
            self.send_to_chat(f"//pos1 {x},{y},{z}")
        else:
            raise AutomationException("Cannot select first position. The script hasn't switched to the game yet.")

    def pos2(self, x, y, z):
        if self.is_switched_to_game:
            self.send_to_chat(f"//pos2 {x},{y},{z}")
        else:
            raise AutomationException("Cannot select second position. The script hasn't switched to the game yet.")

    def line(self, block):
        if self.is_switched_to_game:
            self.send_to_chat(f"//line {block}")
        else:
            raise AutomationException("Cannot place the line. The script hasn't switched to the game yet.")


if __name__ == "__main__":
    automator = GameAutomator()
    automator.find_minecraft_version()
    automator.switch_to_game()
    automator.send_to_chat("Test")
    automator.teleport(0, 100, 0)
