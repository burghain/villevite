import bpy


class VIEW3D_PT_SidePanel(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "villevite"
    bl_label = "villevite"

    def draw(self, context):

        layout = self.layout
        layout.operator("object.generate_city")
        layout.operator("object.generate_street_mesh")
