import os

from source.blueprint_automation_tool import place_parser


def test_place_color():
    parser = place_parser.PlaceParser()
    _here = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(_here, "Rotunda.kml")
    loc = parser.parse_place(file)[0]
    assert loc.color == "ffaa00"


def test_get_line_length_bearing():
    parser = place_parser.PlaceParser()
    _here = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(_here, "Rotunda.kml")
    loc = parser.parse_place(file)[0]
    block_loc = parser.get_line_length_bearing(
        loc.coordinate_list[0].latitude,
        loc.coordinate_list[4].latitude,
        loc.coordinate_list[0].longitude,
        loc.coordinate_list[4].longitude,
    )
    assert block_loc == (1, -7)
