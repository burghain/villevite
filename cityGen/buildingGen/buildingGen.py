import bpy
import os


def add_building():
    bpy.ops.mesh.primitive_plane_add()
    return {"FINISHED"}


def append_nodes():
    filepath = "/mnt/Daten/Blender/cityGen/core/buildingGen/nodes/buildingGen.blend"

    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.node_groups = ["buildingGen"]
