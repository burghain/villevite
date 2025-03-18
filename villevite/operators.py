import bpy
import os

from . import nodes
from . import assets
from .osm.blender_mesh_gen import BlenderMeshGen
from .osm.osm_parser import OSMParser


class OBJECT_OT_AddBuilding(bpy.types.Operator):
    "Create and initialize a new building"
    bl_idname = "object.add_building"
    bl_label = "Add Building"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=4)
        obj = bpy.context.object
        obj.name = "Building"
        group_name = "buildingGen"
        nodes.add_to_object(obj, group_name)
        modifier = obj.modifiers[group_name]
        inputs = {
            "Max Number Of Floors": 5,
            "Min Number of Floors": 4,
        }
        nodes.set_inputs(modifier, inputs)
        return {"FINISHED"}


class OBJECT_OT_Tests(bpy.types.Operator):
    "Deletes the selected building"
    bl_idname = "object.delete_building"
    bl_label = "Tests"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        return {"FINISHED"}


class OBJECT_OT_AppendBuildingGen(bpy.types.Operator):
    bl_idname = "object.add_building_gen"
    bl_label = "Import Assets"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        assets.import_assets()
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
