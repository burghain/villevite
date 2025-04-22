import os
from .blender_mesh_gen import BlenderMeshGen
from .scan_path_generator import ScanPathGenerator
from .osm_parser import OSMParser


class OSMGenerator:

    def __init__(self):
        pass

    def generate(self):
        library_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "Assets")

        parser = OSMParser()
        g, b = parser.parse(os.path.join(library_path, 'potsdam-mini.osm'))

        scan_path_gen = ScanPathGenerator(g)
        scan_path_gen.generate_path()

        bmgen = BlenderMeshGen(g, b)
        city_map = bmgen.generate()
        return city_map
