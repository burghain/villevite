import os
from .blender_mesh_gen import BlenderMeshGen
from .scan_path_generator import ScanPathGenerator
from .osm_parser import OSMParser


class OSMGenerator:

    def __init__(self, file_path):
        self.file_path = file_path

    def generate(self):
        parser = OSMParser()
        g, b = parser.parse(self.file_path)

        scan_path_gen = ScanPathGenerator(g)
        scan_path_gen.generate_path()

        bmgen = BlenderMeshGen(g, b)
        city_map = bmgen.generate()
        return city_map
