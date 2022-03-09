"""
File:           place_parser.py
Description:    parses .kml and .kmz files to find the following information:
                name
                geo-coordinates
                style
                color

Author(s):      Kevin Green
"""

# Built-In Modules
import xml.etree.ElementTree as et
from dataclasses import dataclass


@dataclass
class Coordinate:
    """_summary_
    """
    def __init__(self, longitude, latitude, altitude):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.altitude = float(altitude)

    def __repr__(self):
        return f'Longitude: {self.longitude} Latitude: {self.latitude} Altitude: {self.altitude}'


@dataclass
class Place:
    """_summary_
    """
    def __init__(self, name, coordinate_list, shape, color='ff0000'):
        self.name = name
        self.coordinate_list = coordinate_list
        self.shape = shape
        self.color = color


def parse_place(file):
    # Get namespaces from file so we can search it
    namespaces = dict([
        n for _, n in et.iterparse(file, events=['start-ns'])
    ])

    tree = et.parse(file)
    root = tree.getroot()

    # Create a new place for each placemark in the file
    places = []
    for placemark in root.findall(".//Placemark", namespaces):
        # Grab name for the placemark
        place_name = placemark.find("name", namespaces).text

        # Attempt to find each kind of Placemark that Google Earth Pro creates
        place_types = ["Point", "LineString"]
        for shape_type in place_types:
            # Match the shape to what is stored in the file
            place = placemark.find(shape_type, namespaces)
            if place:
                shape = shape_type

                # Grab the coordinates from the file
                coordinate_strings = place.find("coordinates", namespaces).text.strip().split(' ')
                coordinate_list = []

                for coordinate in coordinate_strings:
                    coordinate_split = coordinate.split(',')
                    coordinate_list.append(Coordinate(
                        coordinate_split[0],
                        coordinate_split[1],
                        coordinate_split[2]
                    ))

        # Attempt to get the color of the place, otherwise default to red
        color = "ff0000"
        style = root.find(".//Style", namespaces)
        if style:
            linestyle = style.find("LineStyle", namespaces)
            iconstyle = style.find("IconStyle", namespaces)
            if linestyle:
                reversed_color = linestyle.find("color", namespaces).text[2:]
                color = reversed_color[::-1]
                print(color)
            elif iconstyle:
                color_elem = iconstyle.find("color", namespaces)
                if color_elem is not None:
                    reversed_color = iconstyle.find("color", namespaces).text[2:]
                    color = reversed_color[::-1]
            else:
                print("No color found")

        places.append(Place(place_name, coordinate_list, shape, color))
        return places


places_list = parse_place("__examples__/Center Mark.kml")
print(places_list[0].coordinate_list[0].longitude)
print(places_list[0].color)
