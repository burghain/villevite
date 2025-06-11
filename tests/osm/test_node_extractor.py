import pytest
from villevite.osm.extractors.node_extractor import NodeExtractor
from ..fixtures import create_igraph_graph, create_osm_node_dataframe, create_big_osm_node_dataframe

def test_simple(create_igraph_graph, create_osm_node_dataframe):
    map_bounds = [6.5, 34.5, 6.5, 34.5]

    node_extractor = NodeExtractor(create_osm_node_dataframe, map_bounds)

    node_extractor.write_to_graph(create_igraph_graph)

    assert len(create_igraph_graph.vs) == 1
    assert create_igraph_graph.vs[0]['osm_id'] == '1'

def test_coords(create_igraph_graph, create_osm_node_dataframe):
    map_bounds = [13.0306900,52.3933300,13.0478100,52.3988800]

    node_extractor = NodeExtractor(create_osm_node_dataframe, map_bounds)

    node_extractor.write_to_graph(create_igraph_graph)

    coord = create_igraph_graph.vs[0]['coord']

    assert coord[0] == pytest.approx(360, abs=10)
    assert coord[1] == pytest.approx(300, abs=10)

def test_multi_nodes(create_igraph_graph, create_big_osm_node_dataframe):
    map_bounds = [0, 0, 0, 0]

    node_extractor = NodeExtractor(create_big_osm_node_dataframe, map_bounds)

    node_extractor.write_to_graph(create_igraph_graph)

    assert len(create_igraph_graph.vs) == len(create_big_osm_node_dataframe)