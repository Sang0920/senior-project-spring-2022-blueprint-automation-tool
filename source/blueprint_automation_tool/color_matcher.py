"""
File:           color_matcher.py
Description:    Takes an hex value and matches it to the closest minecraft dye color
"""

import math

import constants


def color_to_minecraft_dye(hex_color):
    """Takes an hex value and matches it to the closest minecraft dye color

    Args:
        hex_color: A hex color value in RGB formatting

    Returns:
        A string of the closest minecraft dye color
    """

    r, g, b = _hex_to_rgb(hex_color)

    # Calculate the differences between the RGB values and the minecraft dye colors, and choose the
    # closest one
    color_diffs = []
    for color in constants.DYES:
        cr, cg, cb = color
        color_diff = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        color_diffs.append((color_diff, color))
    min_diff = min(color_diffs)[1]

    return constants.DYES[min_diff]


def _hex_to_rgb(h):
    """Takes a hex color value and converts it to RGB

    Args:
        h: A hex color value

    Returns:
        The RGB values of the hex color
    """

    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
