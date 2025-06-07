from .graph_extractor import GraphExtractor
from ..utils import CoordToMeterConverter

class NodeExtractor(GraphExtractor):

    def __init__(self, df, map_bounds):
        super().__init__(df)
        self.ctm_conv = CoordToMeterConverter(map_bounds)

    def write_to_graph(self, g):
        for _, row in self.df.iterrows():
            v = g.add_vertex()

            v['osm_id'] = row['id']
            v['coord'] = self.ctm_conv.geo_coords_to_meter( (float(row['lon']), float(row['lat'])) )