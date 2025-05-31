from .basic_extractor import BasicExtractor

class GraphExtractor(BasicExtractor):

    def write_to_graph(self, g):
        raise NotImplementedError