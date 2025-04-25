import bpy
import os
from .osm.osm_generator import OSMGenerator
from .city.cityGenerator import CityGenerator
from .tree.treeGenerator import generate_tree


def clear_all():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
    for group in bpy.data.node_groups:
        bpy.data.node_groups.remove(group)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)


def increase_clipping_distance():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Near clip distance (default is 0.1)
                    space.clip_start = 0.1
                    space.clip_end = 100000.0


class OBJECT_OT_GenerateCity(bpy.types.Operator):
    "Generate a city with given parameters"
    bl_idname = "villevite.generate_city"
    bl_label = "Generate City"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        parameters = context.scene.cityproperties
        citygen = CityGenerator(parameters)
        city = citygen.generate()
        return {"FINISHED"}


class OBJECT_OT_ReadOSM(bpy.types.Operator):
    bl_idname = "villevite.generate_street_mesh"
    bl_label = "Generate Street Mesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        parameters = context.scene.cityproperties
        city_map = OSMGenerator(parameters.source_file).generate()

        return {"FINISHED"}


class OBJECT_OT_Surprise(bpy.types.Operator):
    bl_idname = "villevite.surprise"
    bl_label = "Surprise me!"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        generate_tree("")
        return {"FINISHED"}


class OBJECT_OT_ClearAll(bpy.types.Operator):
    bl_idname = "villevite.clear_all"
    bl_label = "Clear all"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        clear_all()
        increase_clipping_distance()
        return {"FINISHED"}
