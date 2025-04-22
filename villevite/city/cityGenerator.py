import bpy
import os
from .. import nodes, assets
from ..osm.osm_generator import OSMGenerator


class CityGenerator:
    def __init__(self, properties):
        self.set_parameters(properties)
        self.source = properties.source
        assets.import_assets()

    def set_parameters(self, parameters):
        self.parameters = {
            "Roadway Vehicle Density": parameters.roadway_vehicle_density,
            "Parking Lot Vehicle Density": parameters.parking_lot_vehicle_density,
            "Preview": False,
            "Data Source": ["OSM-Attributes", "Generated"].index(parameters.source),
            "Seed": 0,
        }

    def retrieve_map(self):
        if self.source == "OSM-Attributes":
            city_map = OSMGenerator().generate()

        elif self.source == "Generated":
            city_map = bpy.data.objects.get("Example Road Graph")
            bpy.context.collection.objects.link(city_map)
        return city_map

    def generate(self):

        city_map = self.retrieve_map()
        nodes.add_to_object(city_map, "City Generator",
                            self.parameters)

        return city_map
