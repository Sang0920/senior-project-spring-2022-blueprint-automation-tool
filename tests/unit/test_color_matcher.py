import blueprint_automation_tool.color_matcher as cm


def test_color_to_minecraft_dye():
    assert cm.color_to_minecraft_dye("1D1D21") == "black"
    assert cm.color_to_minecraft_dye("B02E26") == "red"
    assert cm.color_to_minecraft_dye("5E7C16") == "green"
    assert cm.color_to_minecraft_dye("835432") == "brown"
    assert cm.color_to_minecraft_dye("3C44AA") == "blue"
    assert cm.color_to_minecraft_dye("8932B8") == "purple"
    assert cm.color_to_minecraft_dye("169C9C") == "cyan"
    assert cm.color_to_minecraft_dye("9D9D97") == "light_gray"
    assert cm.color_to_minecraft_dye("474F52") == "gray"
    assert cm.color_to_minecraft_dye("F38BAA") == "pink"
    assert cm.color_to_minecraft_dye("80C71F") == "lime"
    assert cm.color_to_minecraft_dye("FED83D") == "yellow"
    assert cm.color_to_minecraft_dye("3AB3DA") == "light_blue"
    assert cm.color_to_minecraft_dye("C74EBD") == "magenta"
    assert cm.color_to_minecraft_dye("F9801D") == "orange"
    assert cm.color_to_minecraft_dye("F9FFFE") == "white"


def test_hex_to_rgb():
    assert cm._hex_to_rgb("ff0000") == (255, 0, 0)
    assert cm._hex_to_rgb("ffa500") == (255, 165, 0)
    assert cm._hex_to_rgb("ffff00") == (255, 255, 0)
    assert cm._hex_to_rgb("008000") == (0, 128, 0)
    assert cm._hex_to_rgb("0000ff") == (0, 0, 255)
    assert cm._hex_to_rgb("4b0082") == (75, 0, 130)
    assert cm._hex_to_rgb("ee82ee") == (238, 130, 238)
    assert cm._hex_to_rgb("000000") == (0, 0, 0)
    assert cm._hex_to_rgb("ffffff") == (255, 255, 255)
