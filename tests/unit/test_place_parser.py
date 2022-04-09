import os

from blueprint_automation_tool import place_parser


def get_location():
    parser = place_parser.PlaceParser()
    _here = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(_here, "Rotunda.kml")
    loc = parser.parse_place(file)[0]
    return loc


def test_place_color():
    assert get_location().color == "ffaa00"


def test_get_line_length_bearing():
    p = place_parser.PlaceParser()
    loc = get_location()
    block_loc = p.convert_to_minecraft(
        loc.coordinate_list[0].latitude,
        loc.coordinate_list[4].latitude,
        loc.coordinate_list[0].longitude,
        loc.coordinate_list[4].longitude,
    )
    assert block_loc == (-7, 0, -1)
