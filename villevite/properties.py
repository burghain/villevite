"""
This module defines the propertygroup for the parameters of the city generation.
"""

from bpy import props, types


class CityProperties(types.PropertyGroup):
    """
    A class representing properties for city generation in Blender.
    """

    source: props.EnumProperty(
        name="Data Source",
        description="Source of the city data",
        items=[
            ("OSM-Attributes", "Read from OSM", "OpenStreetMap"),
            ("Generated", "Generated", "Generated"),
        ],
    )  # type: ignore

    coordinates: props.StringProperty(
        name="Coordinates",
        description="Coordinates of the map excerpt to use (format: 'minlon,minlat,maxlon,maxlat')",
        default="13.0306900,52.3933300,13.0478100,52.3988800",
    )  # type: ignore

    roadway_vehicle_density: props.FloatProperty(
        name="Roadway Vehicle Density",
        description="Amount of vehicles on the road",
        default=0.3,
        min=0.0,
        max=1.0,
    )  # type: ignore

    parking_lot_vehicle_density: props.FloatProperty(
        name="Parking Lot Vehicle Density",
        description="Amount of parked vehicles",
        default=0.7,
        min=0.0,
        max=1.0,
    )  # type: ignore
