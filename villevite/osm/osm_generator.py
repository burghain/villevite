import os
from .blender_mesh_gen import BlenderMeshGen
from .scan_path_generator import ScanPathGenerator
from .osm_parser import OSMParser
from .osm_dl import OSMDownloader
from .property_register import *
from .property_writer import *


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
        edge_prop_reg = EdgePropertyRegister()
        edge_prop_reg.register_writers([
            NumberOfLanesWriter('Number Of Lanes', 1, 'INT8'),
            HasParkingLotsWriter('Has Parking Lots', False, 'BOOLEAN'),
            HasBikeLaneWriter('Has Bike Lane', False, 'BOOLEAN'),
            HasSidewalkWriter('Has Sidewalk', False, 'BOOLEAN'),
            StreetIDWriter('Street ID', -1, 'INT')
        ])

        b_prop_reg = BasicPropertyRegister()
        b_prop_reg.register_writers([LevelWriter(1)])

        print("Parsing OSM File...")
        parser = OSMParser()
        g, b = parser.parse(edge_prop_reg, b_prop_reg)
        print("Parsed OSM File successfully")

        # print("Generating Scan Path...")
        # scan_path_gen = ScanPathGenerator(g)
        # scan_path_gen.generate_path()
        # print("Scan Path generated successfully")

        print("Generating Blender Mesh...")
        bmgen = BlenderMeshGen(g, b, edge_prop_reg)
        city_map = bmgen.generate()
        print("Blender Mesh Generated successfully")
        return city_map
