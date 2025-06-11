from ..fixtures import create_osm_highway_dataframe, create_igraph_node_graph
from villevite.osm.property_register import EdgePropertyRegister
from villevite.osm.extractors.highway_extractor import HighwayExtractor

def test_simple(create_osm_highway_dataframe, create_igraph_node_graph):
    prop_reg = EdgePropertyRegister()

    highway_extractor = HighwayExtractor(create_osm_highway_dataframe)

    highway_extractor.write_to_graph(create_igraph_node_graph, prop_reg)

    assert len(create_igraph_node_graph.es) == 1
    assert [create_igraph_node_graph.vs[v_id]['osm_id'] for v_id in create_igraph_node_graph.es[0].tuple] == ['1', '2']
