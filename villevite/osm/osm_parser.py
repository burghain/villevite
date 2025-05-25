from pyrosm import OSM
import igraph as ig
import pandas as pd
from .extractors.node_extractor import NodeExtractor
from .extractors.highway_extractor import HighwayExtractor

class OSMParser():

    def parse(self, filename):
        g = ig.Graph(directed=False)

        osm = OSM('/mnt/SUPERCOOL/osm-pbf/paris.pbf')

        df_nodes, _ = osm.get_network(nodes=True, network_type='all')
        df_ways = osm.get_data_by_custom_criteria({'highway': ['primary', 'secondary', 'tertiary', 'residential', 'living_street', 'motorway', 'trunk']})
        df_way_nodes = pd.DataFrame(osm._way_records).set_index('id')['nodes']

        df_ways = df_ways.merge(df_way_nodes, on='id')

        node_extractor = NodeExtractor(df_nodes, osm.get_boundaries(boundary_type='all').total_bounds)
        node_extractor.write_to_graph(g)

        hw_extractor = HighwayExtractor(df_ways)
        hw_extractor.write_to_graph(g)

        lonely_vertices = g.vs.select(lambda v: v.degree() == 0)
        print(f"delete {len(lonely_vertices)}")
        g.delete_vertices(lonely_vertices)

        print("Built graph")
        print(f"no. verts: {len(g.vs)}, no. edges: {len(g.es)}")

        return g, []
