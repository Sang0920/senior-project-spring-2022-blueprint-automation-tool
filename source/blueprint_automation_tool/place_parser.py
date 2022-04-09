"""
File:           place_parser.py
Description:    parses .kml and .kmz files to find the following information:
                name
                geo-coordinates
                style
                color
"""

import xml.etree.ElementTree as et
import zipfile
from io import StringIO
from math import atan2, cos, floor, radians, sin, sqrt


class Coordinate:
    """Representation of  a geographic coordinate"""

    def __init__(self, longitude, latitude, altitude):
        self.longitude = radians(float(longitude))
        self.latitude = radians(float(latitude))
        self.altitude = float(altitude)

    def __repr__(self):
        return f"Longitude: {self.longitude} Latitude: {self.latitude} Altitude: {self.altitude}"


class Place:
    """Representation of a parsed place"""

    def __init__(self, name, coordinate_list, shape, color="ff0000"):
        self.name = name
        self.coordinate_list = coordinate_list
        self.shape = shape
        self.color = color


class PlaceParser:
    """Handles the parsing of files to find the places contained in them"""

    def parse_place(self, file):
        """Parses a .kml/.kmz file and returns a list of found places

        Args:
            file: Path to the file to parse

        Returns:
            A list of found places
        """

        # Extracts the .kml file from .kmz files if necessary
        if file.endswith("kmz"):
            print("Handling a .kmz file")
            with zipfile.ZipFile(file) as zip_file:
                with zip_file.open("doc.kml", "r") as f:
                    string_content = f.read().decode("utf-8")
        else:
            with open(file, "r") as f:
                string_content = f.read()

        # Get namespaces from file so we can search it
        namespaces = dict(
            [n for _, n in et.iterparse(StringIO(string_content), events=["start-ns"])]
        )

        tree = et.parse(StringIO(string_content))
        root = tree.getroot()

        # Create a new place for each placemark in the file
        places = []
        for placemark in root.findall(".//Placemark", namespaces):
            # Grab name for the placemark
            place_name = placemark.find("name", namespaces).text

            # Attempt to find each kind of Placemark that Google Earth Pro creates
            place_types = ["Point", "LineString", "Polygon"]
            for shape_type in place_types:
                # Match the shape to what is stored in the file
                place = placemark.find(shape_type, namespaces)
                if place:
                    shape = shape_type

                    # Grab the coordinates from the file
                    if place.find("outerBoundaryIs", namespaces):
                        outerBoundaryIs = place.find("outerBoundaryIs", namespaces)
                        ring = outerBoundaryIs = outerBoundaryIs.find("LinearRing", namespaces)
                        coordinate_strings = (
                            ring.find("coordinates", namespaces).text.strip().split(" ")
                        )
                    else:
                        coordinate_strings = (
                            place.find("coordinates", namespaces).text.strip().split(" ")
                        )
                    coordinate_list = []

                    for coordinate in coordinate_strings:
                        coordinate_split = coordinate.split(",")
                        coordinate_list.append(
                            Coordinate(
                                coordinate_split[0],
                                coordinate_split[1],
                                coordinate_split[2],
                            )
                        )

            # Attempt to get the color of the place, otherwise default to red
            color = "ff0000"
            style = root.find(".//Style", namespaces)
            if style:
                linestyle = style.find("LineStyle", namespaces)
                iconstyle = style.find("IconStyle", namespaces)
                if linestyle:
                    reversed_color = linestyle.find("color", namespaces).text[2:]
                    color = reversed_color[::-1]
                elif iconstyle:
                    color_elem = iconstyle.find("color", namespaces)
                    if color_elem is not None:
                        reversed_color = iconstyle.find("color", namespaces).text[2:]
                        color = reversed_color[::-1]

            places.append(Place(place_name, coordinate_list, shape, color))
            return places

    def convert_to_minecraft(self, lat1, lat2, long1, long2, altitude=0, scale=1):
        """Converts a place to a block location given a reference point
            Calculations from:
            https://www.movable-type.co.uk/scripts/latlong.html

        Args:
            lat1: The reference latitude
            lat2: The place latitude
            long1: The reference longitude
            long2: The place longitude
            altitude: The height of the place. Defaults to 0.
            scale: How much to scale the conversion. Defaults to 1.

        Returns:
            X, Y, Z coordinates of the place in-game
        """

        earth_radius = 6_371_000  # Earth's Approximate Radius in meters

        delta_lat = lat2 - lat1
        delta_long = long2 - long1

        # Calculate the initial bearing between the two points
        y = sin(long2 - long1) * cos(lat2)
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_long)

        bearing = atan2(y, x)

        # Calculate the haversine distance between the two points
        a = sin(delta_lat / 2) * sin(delta_lat / 2) + cos(lat1) * cos(lat2) * sin(
            delta_long / 2
        ) * sin(delta_long / 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = scale * earth_radius * c

        # Using the distance and bearing as polar coordinates, convert them to cartesian coordinates
        # Values for x and z are swapped and z is multiplied by -1 to rotate the coordinates to
        # Minecraft's coordinates for North
        block_x = floor(distance * sin(bearing))
        block_z = -1 * floor(distance * cos(bearing))

        return (block_x, floor(altitude), block_z)
