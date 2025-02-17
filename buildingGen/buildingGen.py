import bpy


def add_building():
    bpy.ops.mesh.primitive_plane_add()
    return {"FINISHED"}
