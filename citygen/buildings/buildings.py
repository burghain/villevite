import bpy
import os


def add_building():
    bpy.ops.mesh.primitive_plane_add()
    return {"FINISHED"}


def append_node_group(name):
    filepath = os.path.join(os.path.dirname(__file__), f"nodes/{name}.blend")
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.node_groups = [name]
