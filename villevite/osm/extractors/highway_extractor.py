from .graph_extractor import GraphExtractor
import itertools

class HighwayExtractor(GraphExtractor):

    def write_to_graph(self, g, prop_register):
        for _, row in self.df.iterrows():
            nodes = row['nodes']

            prop_register.process_all_props(row)

            for i, j in itertools.pairwise(nodes):
                i_vertex = g.vs.find(osm_id=i)
                j_vertex = g.vs.find(osm_id=j)

                e = g.add_edge(i_vertex, j_vertex)

                prop_register.write_all_props(e)