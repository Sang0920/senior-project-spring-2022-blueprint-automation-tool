import re
from time import sleep

from automation_helpers.window import WindowHandler
from automation_helpers.keyboard import KeyboardHandler


class AutomationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MinecraftHandler:
    def __init__(self):
        self.current_version = None
        self.window_handler = WindowHandler()
        self.keyboard_handler = KeyboardHandler()
        self.supported_mc_versions = ['1.12', '1.13', '1.14', '1.15', '1.16', '1.17', '1.18']
        self.supported_blocks = [
            'minecraft:red_wool',
            'minecraft:orange_wool',
            'minecraft:pink_wool',
            'minecraft:yellow_wool',
            'minecraft:lime_wool',
            'minecraft:green_wool',
            'minecraft:light_blue_wool',
            'minecraft:cyan_wool',
            'minecraft:blue_wool',
            'minecraft:magenta_wool',
            'minecraft:purple_wool',
            'minecraft:brown_wool',
            'minecraft:gray_wool',
            'minecraft:light_gray_wool',
            'minecraft:black_wool',
        ]
        self.lowest_height = -64
        self.tallest_height = 328
        self.game_window = None

    def find_minecraft_version(self):
        game_window = self.window_handler.find_window("Minecraft.*[0-9]+\.[0-9]+.*(Singleplayer|Multiplayer)", limit=1)
        if game_window:
            version = re.findall("[0-9]+\.[0-9]+", game_window[0].title)
            if version and version[0] in self.supported_mc_versions:
                self.game_window = game_window[0]
                self.current_version == version[0]
                return version[0]
            else:
                raise AutomationException(f"A Minecraft Window was found, but its version is not supported")
        else:
            raise AutomationException("Minecraft Window not found! Is there an active world open yet?")

    def switch_to_game(self):
        self.window_handler.set_current_window(self.game_window)
        self.window_handler.maximize_window(self.game_window)
        sleep(5)
        self.keyboard_handler.press_and_release('esc', hold_time=1)

    def execute_command(self):
        self.keyboard_handler.press_and_release('t', hold_time=0.1)
        # TODO make this an actual command thing
        # self.keyboard_handler.write("Andy is a person", hold_time=0.1, pause_between=0.1)
        self.keyboard_handler.paste("Andy is a great person")


if __name__ == "__main__":
    sleep(10)
    print(MinecraftHandler().find_minecraft_version())
    handler = MinecraftHandler()
    handler.find_minecraft_version()
    handler.switch_to_game()
    handler.execute_command()
