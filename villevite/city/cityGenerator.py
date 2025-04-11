import bpy
import os
from .. import nodes, assets
from ..osm.osm_parser import OSMParser
from ..osm.blender_mesh_gen import BlenderMeshGen


class CityGenerator:
    def __init__(self, source="osm"):
        self.source = source
        assets.import_assets()

    def generate_road_graph(self):
        if self.source == "osm":
            library_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "Assets")
            parser = OSMParser()
            graph, v = parser.parse(os.path.join(
                library_path, 'potsdam-mini.osm'))
            gen = BlenderMeshGen(graph)
            road_graph = gen.generate()
        elif self.source == "template":
            road_graph = bpy.data.objects.get("Example Road Graph")
            bpy.context.collection.objects.link(road_graph)
        return road_graph

    def generate(self):

        road_graph = self.generate_road_graph()
        nodes.add_to_object(road_graph, "City Generator")
        return road_graph
