import bpy


class VIEW3D_PT_SidePanel(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "villevite"
    bl_label = "villevite"

    def draw(self, context):
        parameters = context.scene.cityproperties
        layout = self.layout

        box = layout.box()
        box.row()
        box.prop(parameters, "source")
        # box.prop(parameters, "roadway_vehicle_density")
        # box.prop(parameters, "parking_lot_vehicle_density")
        layout.operator("villevite.generate_city")
        layout.operator("villevite.generate_street_mesh")
        layout.operator("villevite.surprise")
        layout.operator("villevite.clear_all")
