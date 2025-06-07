from pyrosm import OSM
import os
import igraph as ig
import pandas as pd
from .extractors.node_extractor import NodeExtractor
from .extractors.highway_extractor import HighwayExtractor
from .extractors.building_extractor import BuildingExtractor

class OSMParser():

    def parse(self, filename, with_edge_props, with_b_props):
        g = ig.Graph(directed=False)
        b = []

        osm = OSM(f'{os.getcwd()}/villevite/Assets/{filename}.pbf')

        map_bounds = osm.get_boundaries(boundary_type='all').total_bounds

        df_nodes, _ = osm.get_network(nodes=True, network_type='all')
        df_highways = osm.get_data_by_custom_criteria({'highway': ['primary', 'secondary', 'tertiary', 'residential', 'living_street', 'motorway', 'trunk']})
        df_buildings = osm.get_buildings()

        df_way_nodes = pd.DataFrame(osm._way_records).set_index('id')['nodes']

        df_highways = df_highways.merge(df_way_nodes, on='id')

        node_extractor = NodeExtractor(df_nodes, map_bounds)
        node_extractor.write_to_graph(g)

        hw_extractor = HighwayExtractor(df_highways)
        hw_extractor.write_to_graph(g, with_edge_props)

        building_extractor = BuildingExtractor(df_buildings, map_bounds)
        building_extractor.write_to_array(b, with_b_props)

        lonely_vertices = g.vs.select(lambda v: v.degree() == 0)
        print(f"delete {len(lonely_vertices)}")
        g.delete_vertices(lonely_vertices)

        print("Built graph")
        print(f"no. verts: {len(g.vs)}, no. edges: {len(g.es)}")

        return g, b
