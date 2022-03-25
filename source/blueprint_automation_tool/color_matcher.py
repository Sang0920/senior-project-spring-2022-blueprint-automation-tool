"""
File:           color_matcher.py
Description:    Takes an hex value and matches it to the cloest minecraft dye color
"""

import math


def color_to_minecraft_dye(hex_color):
    # Minecraft Colors from https://minecraft.fandom.com/wiki/Dye#Color_values
    dyes = {
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

    r, g, b = _hex_to_rgb(hex_color)
    color_diffs = []
    for color in dyes:
        cr, cg, cb = color
        color_diff = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        color_diffs.append((color_diff, color))
    min_diff = min(color_diffs)[1]

    return dyes[min_diff]


def _hex_to_rgb(h):
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    print(color_to_minecraft_dye("ffffff"))
