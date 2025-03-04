import bpy


class VIEW3D_PT_SidePanel(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "villevite"
    bl_label = "villevite"

    def draw(self, context):

        layout = self.layout
        layout.operator("object.add_building")
        layout.operator("object.delete_building")
        layout.operator("object.add_building_gen")
