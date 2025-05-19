import os
from .blender_mesh_gen import BlenderMeshGen
from .scan_path_generator import ScanPathGenerator
from .osm_parser import OSMParser
from .osm_dl import OSMDownloader


class OSMGenerator:

    '''
    Initialize the OSMGenerator with the coordinates of the map excerpt to generate

    Use coords or stringcoords as keyword argument, depending of the format of the coordinates

    coords.. 4-tuple of floats
    stringcoords.. string with 4 floats separated by ','
    '''
    def __init__(self, **kwargs):
        if 'coords' in kwargs:
            self.coords = kwargs['coords']
        else:
            self.coords = [float(x) for x in kwargs['stringcoords'].split(',')]

    def generate(self):
        dl = OSMDownloader(self.coords, 'map.osm')
        dl.download_to_file()

        print("Parsing OSM File...")
        parser = OSMParser()
        g, b = parser.parse(os.getcwd() + '/villevite/Assets/map.osm')
        print("Parsed OSM File successfully")

        dl.clear()

        print("Generating Scan Path...")
        scan_path_gen = ScanPathGenerator(g)
        scan_path_gen.generate_path()
        print("Scan Path generated successfully")

        print("Generating Blender Mesh...")
        bmgen = BlenderMeshGen(g, b)
        city_map = bmgen.generate()
        print("Blender Mesh Generated successfully")
        return city_map
