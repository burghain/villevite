from .graph_extractor import GraphExtractor
import itertools

class HighwayExtractor(GraphExtractor):

    def write_to_graph(self, g):
        for _, row in self.df.iterrows():
            nodes = row['nodes']

            for i, j in itertools.pairwise(nodes):
                i_vertex = g.vs.find(osm_id=i)
                j_vertex = g.vs.find(osm_id=j)

                g.add_edge(i_vertex, j_vertex)
