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

    def generate_road_graph(self):
        if self.source == "OSM-Attributes":
            road_graph = OSMGenerator().generate()

        elif self.source == "Generated":
            road_graph = bpy.data.objects.get("Example Road Graph")
            bpy.context.collection.objects.link(road_graph)
        return road_graph

    def generate(self):

        road_graph = self.generate_road_graph()
        nodes.add_to_object(road_graph, "City Generator",
                            self.parameters)
        return road_graph
