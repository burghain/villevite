import os
from .blender_mesh_gen import BlenderMeshGen
from .osm_parser import OSMParser

class OSMGenerator:

    def __init__(self):
        pass

    def generate(self):
        library_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "Assets")

        parser = OSMParser()
        g, v = parser.parse(os.path.join(library_path, 'potsdam-mini.osm'))
        gen = BlenderMeshGen(g)
        return gen.generate()