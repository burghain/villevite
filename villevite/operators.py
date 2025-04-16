import bpy
import os
from .osm.blender_mesh_gen import BlenderMeshGen
from .osm.osm_parser import OSMParser
from .city.cityGenerator import CityGenerator
from .tree.treeGenerator import generate_tree


def clear_all():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
    for group in bpy.data.node_groups:
        bpy.data.node_groups.remove(group)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)


class OBJECT_OT_GenerateCity(bpy.types.Operator):
    "Generate a city with given parameters"
    bl_idname = "villevite.generate_city"
    bl_label = "Generate City"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        clear_all()
        parameters = context.scene.cityproperties
        citygen = CityGenerator(parameters)
        city = citygen.generate()
        return {"FINISHED"}


class OBJECT_OT_ReadOSM(bpy.types.Operator):
    bl_idname = "villevite.generate_street_mesh"
    bl_label = "Generate Street Mesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        library_path = os.path.join(os.path.dirname(__file__), "Assets")

        parser = OSMParser()
        g, a, v = parser.parse(os.path.join(library_path, 'potsdam-mini.osm'))
        gen = BlenderMeshGen(g, a)
        gen.generate()

        return {"FINISHED"}


class OBJECT_OT_Surprise(bpy.types.Operator):
    bl_idname = "villevite.surprise"
    bl_label = "Surprise me!"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        generate_tree("acer")
        return {"FINISHED"}
