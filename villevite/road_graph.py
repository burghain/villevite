"""Road-graph discovery, validation, and default-graph loading.

The road graph is a plain wire mesh (vertices and edges, no faces) that the
user builds manually. The GeoCity geometry node group consumes it as its input
geometry and generates all road attributes and building floor plans itself.
"""

from typing import Optional

import bpy

from . import assets

DEFAULT_ROAD_GRAPH_NAME = "Default Road Graph"


def is_valid_road_graph(obj: Optional[bpy.types.Object]) -> bool:
    """
    A valid road graph is a local, editable wire mesh: at least one edge, no faces.
    """
    return (
        obj is not None
        and obj.type == "MESH"
        and obj.library is None
        and obj.override_library is None
        and len(obj.data.edges) > 0
        and len(obj.data.polygons) == 0
    )


def find_road_graph(context: bpy.types.Context) -> Optional[bpy.types.Object]:
    """
    Return the active object if it is a valid road graph, otherwise the first
    valid selected object, otherwise None.
    """
    active = context.view_layer.objects.active
    if is_valid_road_graph(active):
        return active
    for obj in context.selected_objects:
        if is_valid_road_graph(obj):
            return obj
    return None


def ensure_default_road_graph(context: bpy.types.Context) -> bpy.types.Object:
    """
    Return the Default Road Graph object, appending it from Nodes.blend if
    necessary, and guarantee it is linked into the current scene.
    """
    obj = assets.load_object(DEFAULT_ROAD_GRAPH_NAME)
    if obj.name not in context.scene.collection.all_objects:
        context.scene.collection.objects.link(obj)
    return obj
