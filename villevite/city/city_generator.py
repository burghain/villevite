"""Main class that orchestrates the city generation"""
import bpy


from .. import nodes, assets
from ..osm.osm_generator import OSMGenerator


class CityGenerator:
    """
    A class to generate a city using Blender and OpenStreetMap (OSM) data.

    Attributes:
        source (str): The data source for the city generation.
        source_file (str): The file path to the source data if using OSM-Attributes.
        parameters (Dict[str, Any]): A dictionary of parameters for city generation.
    """

    def __init__(self, properties: bpy.types.PropertyGroup) -> None:
        """
        Initialize the CityGenerator with the given properties.
        """
        self.set_parameters(properties)
        self.source = properties.source
        self.coordinates = properties.coordinates
        assets.import_assets_and_nodes()

    def set_parameters(self, parameters: bpy.types.PropertyGroup) -> None:
        """
        Set the city generation parameters from the cityProperties Group.
        """
        self.parameters = {
            "Roadway Vehicle Density": parameters.roadway_vehicle_density,
            "Parking Lot Vehicle Density": parameters.parking_lot_vehicle_density,
            "Preview": False,
            "Data Source": ["OSM-Attributes", "Generated"].index(parameters.source),
            "Seed": 0,
        }

    def retrieve_map(self) -> bpy.types.Object:
        """
        Retrieve the city map based on the data source.
        """
        if self.source == "OSM-Attributes":
            city_map = OSMGenerator(stringcoords=self.coordinates).generate()
        elif self.source == "Generated":
            city_map = bpy.data.objects.get("Example Road Graph")
            if city_map:
                bpy.context.collection.objects.link(city_map)
        return city_map

    def generate(self) -> bpy.types.Object:
        """
        Generate the city using the specified parameters and data source.
        """
        city_map = self.retrieve_map()
        if city_map:
            nodes.add_to_object(city_map, "City Generator", self.parameters)
        return city_map
