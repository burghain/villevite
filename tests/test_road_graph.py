import bpy
import pytest

from bl_ext.user_default.villevite import road_graph

GEO_CITY_GROUP = "GeoCity"
DEFAULT_NAME = road_graph.DEFAULT_ROAD_GRAPH_NAME


@pytest.fixture(autouse=True)
def clean_scene():
    bpy.ops.villevite.clear_all()
    yield
    bpy.ops.villevite.clear_all()


def _geocity_modifiers(obj):
    return [
        modifier for modifier in obj.modifiers
        if modifier.type == 'NODES'
        and modifier.node_group is not None
        and modifier.node_group.name == GEO_CITY_GROUP
    ]


def test_load_default_road_graph():
    bpy.ops.villevite.load_default_road_graph()
    obj = bpy.data.objects.get(DEFAULT_NAME)
    assert obj is not None, f"'{DEFAULT_NAME}' should exist after loading"
    assert bpy.context.view_layer.objects.active == obj, "Loaded graph should be active"
    assert obj.type == "MESH"
    assert len(obj.data.edges) > 0, "Road graph should have edges"
    assert len(obj.data.polygons) == 0, "Road graph should have no faces"
    assert road_graph.is_valid_road_graph(obj)


def test_load_default_road_graph_idempotent():
    bpy.ops.villevite.load_default_road_graph()
    bpy.ops.villevite.load_default_road_graph()
    assert bpy.data.objects.get(f"{DEFAULT_NAME}.001") is None, \
        "Loading twice should not create a duplicate"


def test_generate_city_attaches_modifier():
    # Empty scene: the operator auto-loads the Default Road Graph
    bpy.ops.villevite.generate_city()
    obj = bpy.data.objects.get(DEFAULT_NAME)
    assert obj is not None, "Generate City should auto-load the default road graph"
    assert len(_geocity_modifiers(obj)) == 1, "Exactly one GeoCity modifier expected"

    # Rerunning must not stack a second modifier
    bpy.ops.villevite.generate_city()
    assert len(_geocity_modifiers(obj)) == 1, "Rerun must not stack GeoCity modifiers"
