import os
from .blender_mesh_gen import BlenderMeshGen
from .scan_path_generator import ScanPathGenerator
from .osm_parser import OSMParser
from .osm_dl import OSMDownloader


class OSMGenerator:

    def __init__(self, file_path):
        self.file_path = file_path

    def generate(self):
        dl = OSMDownloader()
        #dl.download_to_file([13.0306900,52.3933300,13.0478100,52.3988800], 'map.osm')

        print("Parsing OSM File...")
        parser = OSMParser()
        #g, b = parser.parse(os.getcwd() + '/villevite/Assets/map.osm')
        g, b = parser.parse(self.file_path)
        print("Parsed OSM File successfully")

        print("Generating Scan Path...")
        scan_path_gen = ScanPathGenerator(g)
        scan_path_gen.generate_path()
        print("Scan Path generated successfully")

        print("Generating Blender Mesh...")
        bmgen = BlenderMeshGen(g, b)
        city_map = bmgen.generate()
        print("Blender Mesh Generated successfully")
        return city_map
