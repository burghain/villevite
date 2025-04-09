import bpy
import os

from . import nodes
from . import assets
from .osm.blender_mesh_gen import BlenderMeshGen
from .osm.osm_parser import OSMParser


class OBJECT_OT_GenerateCity(bpy.types.Operator):
    "Generate a city with given parameters"
    bl_idname = "object.generate_city"
    bl_label = "Generate City"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        assets.import_assets()
        road_graph = bpy.data.objects.get("Example Road Graph")
        bpy.context.collection.objects.link(road_graph)
        nodes.add_to_object(road_graph, "Road Graph Test")
        return {"FINISHED"}


class OBJECT_OT_ReadOSM(bpy.types.Operator):
    bl_idname = "object.generate_street_mesh"
    bl_label = "Generate Street Mesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        library_path = os.path.join(os.path.dirname(__file__), "Assets")

        parser = OSMParser()
        g, v = parser.parse(os.path.join(library_path, 'potsdam-mini.osm'))
        gen = BlenderMeshGen(g)
        gen.generate()

        return {"FINISHED"}
