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
    d = {'id': ['1'],
         'lat': ['52.3961586'],
         'lon': ['13.0360831']}
    
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