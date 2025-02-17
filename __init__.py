# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy


class OBJECT_OT_add_building(bpy.types.Operator):
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


class OBJECT_OT_delete_building(bpy.types.Operator):
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


class VIEW3D_PT_cube_business(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "cityGen"
    bl_label = "cityGen"

    def draw(self, context):

        layout = self.layout
        layout.operator("object.add_building")
        layout.operator("object.delete_building")


classes = [
    OBJECT_OT_add_building,
    VIEW3D_PT_cube_business,
    OBJECT_OT_delete_building,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
