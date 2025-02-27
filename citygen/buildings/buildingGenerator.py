import bpy
import os


class buildingGenerator:

    def __init__(self):
        self.group_name = "buildingGen"

    def add_building(self):
        bpy.ops.mesh.primitive_plane_add()
        return {"FINISHED"}

    def append_node_group(self):

        pass

    def assign_node_group_to(self, obj):
        geo_mod = obj.modifiers.new(name=self.group_name, type="NODES")
        geo_mod.node_group = bpy.data.node_groups[self.group_name]
        return obj
