import bpy
import pytest
from bl_ext.user_default.villevite import assets
import pandas as pd
import igraph as ig



def clear_all():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
    for group in bpy.data.node_groups:
        bpy.data.node_groups.remove(group)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)


@pytest.fixture
def import_assets():
    assets.import_assets_and_nodes()
    yield
    clear_all()


@pytest.fixture(scope="module")
def import_assets_and_tests():
    assets.import_assets_and_nodes()
    assets.import_tests()
    yield
    clear_all()

@pytest.fixture
def create_osm_node_dataframe():
    d = {'id': ['1', '2'],
         'lat': ['52.3961586', '52.3961589'],
         'lon': ['13.0360831', '13.0360832']}
    
    return pd.DataFrame(data=d)

@pytest.fixture
def create_big_osm_node_dataframe():
    ids = range(1, 101)

    d = {'id': ids,
         'lat': ['52.3961586' for _ in ids],
         'lon': ['13.0360831' for _ in ids]}
    
    return pd.DataFrame(data=d)

@pytest.fixture
def create_igraph_graph():
    return ig.Graph(directed=False)

@pytest.fixture
def create_osm_highway_dataframe():
    d = {'nodes': [['1', '2']]}

    return pd.DataFrame(data=d)

@pytest.fixture
def create_igraph_node_graph():
    g = ig.Graph(directed=False)

    v = g.add_vertex()
    v['osm_id'] = '1'
    
    v = g.add_vertex()
    v['osm_id'] = '2'

    return g