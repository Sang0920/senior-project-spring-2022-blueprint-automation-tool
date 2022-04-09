"""
File:           constants.py
Description:    defines constants that are used in the project
"""

import os

# Application Information

APPLICATION_NAME = "Blueprint Automation Tool"

DEFAULT_SETTINGS = {
    "base_building_height": 0,
    "building_block_choice": "concrete",
    "scaling_factor": 1.0,
    "theme_style": "Dark",
    "last_used_reference": None,
    "last_used_game_version": "1.18",
}

# Minecraft Information

# Translation of RGB values to their respective minecraft dye color
# Translated from hex values from https://minecraft.fandom.com/wiki/Dye#Color_values

SUPPORTED_MINECRAFT_VERSIONS = [
    "1.12",
    "1.13",
    "1.14",
    "1.15",
    "1.16",
    "1.17",
    "1.18",
]

BLOCKS = [
    "concrete",
    "concrete_powder",
    "terracotta",
    "glazed_terracotta",
    "stained_glass",
    "stained_glass_pane",
    "wool",
]

DYES = {
    (249, 255, 254): "white",
    (157, 157, 151): "light_gray",
    (71, 79, 82): "gray",
    (29, 29, 33): "black",
    (131, 84, 50): "brown",
    (176, 46, 38): "red",
    (249, 128, 29): "orange",
    (254, 216, 61): "yellow",
    (128, 199, 31): "lime",
    (94, 124, 22): "green",
    (22, 156, 156): "cyan",
    (58, 179, 218): "light_blue",
    (60, 68, 170): "blue",
    (137, 50, 184): "purple",
    (243, 139, 170): "pink",
    (199, 78, 189): "magenta",
}

# Directories

PROJECT_PATH = os.path.join(os.path.expanduser("~/Documents"), "Project BAT")
LOGS_PATH = os.path.join(PROJECT_PATH, "logs")
