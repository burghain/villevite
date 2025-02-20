import bpy
from .buildings import buildings


class OBJECT_OT_AddBuilding(bpy.types.Operator):
    "Create and initialize a new building"
    bl_idname = "object.add_building"
    bl_label = "Add Building"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add()
        return {"FINISHED"}


class OBJECT_OT_DeleteBuilding(bpy.types.Operator):
    "Deletes the selected building"
    bl_idname = "object.delete_building"
    bl_label = "Delete Building"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.object.delete(confirm=False)
        return {"FINISHED"}


class OBJECT_OT_AppendBuildingGen(bpy.types.Operator):
    bl_idname = "object.add_building_gen"
    bl_label = "Append BuildingGen"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        buildings.append_node_group()
        return {"FINISHED"}
