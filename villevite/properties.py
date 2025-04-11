from bpy import props, types


class CityProperties(types.PropertyGroup):
    source: props.EnumProperty(
        name="Source",
        description="Source of the city data",
        items=[
            ("osm", "OSM", "OpenStreetMap"),
            ("template", "Template", "Template"),
        ],
        default="osm",
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
