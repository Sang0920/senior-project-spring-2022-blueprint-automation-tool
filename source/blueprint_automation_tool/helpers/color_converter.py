import math


def color_to_minecraft_dye(hex_color):
    # Hex color for minecraft dyes from
    # https://minecraft.fandom.com/wiki/Dye
    dyes = {
        "white": "F9FFFE",
        "light_gray": "9D9D97",
        "gray": "474F52",
        "black": "1D1D21",
        "brown": "835432",
        "red": "B02E26",
        "orange": "F9801D",
        "yellow": "FED83D",
        "lime": "80C71F",
        "green": "5E7C16",
        "cyan": "169C9C",
        "light_blue": "3AB3DA",
        "blue": "3C44AA",
        "purple": "8932B8",
        "magenta": "C74EBD",
        "pink": "F38BAA",
    }

    rgb_color = _hex_to_rgb(hex_color)

    lowest_distance = math.inf
    block_color = ""
    for color in dyes:
        distance = _color_distance(_hex_to_rgb(dyes[color]), rgb_color)
        if distance < lowest_distance:
            lowest_distance = distance
            block_color = color

    return block_color


def _hex_to_rgb(hex_color):
    return (int(hex_color[:2], 16), (hex_color[2:4], 16), int(hex_color[4:], 16))


def _color_distance(rgb1, rgb2):
    # Approximation for distance between two colors
    # Derived from https://www.compuphase.com/cmetric.htm
    r_mean = (rgb1[0] + rgb2[0]) / 2
    delta_r = rgb1[0] - rgb2[0]
    delta_g = rgb1[1] - rgb2[1]
    delta_b = rgb1[2] - rgb2[2]

    color_difference = math.sqrt(
        ((2 + (r_mean / 256)) * delta_r * delta_r)
        + (4 * delta_g * delta_g)
        + ((2 + ((255 - r_mean) / 256)) * delta_b * delta_b)
    )

    return color_difference


if __name__ == "__main__":
    print(color_to_minecraft_dye("ffaa00"))
