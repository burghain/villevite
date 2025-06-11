"""
This module defines the UI elements for the villevite addon in Blender.

It includes a side panel in the 3D Viewport UI that provides various operators
for generating and managing city elements.
"""

import bpy


class VIEW3D_PT_SidePanel(bpy.types.Panel):
    """
    A custom side panel for the villevite addon in the 3D Viewport UI.

    Attributes:
        bl_space_type (str): Specifies the space type where the panel is displayed.
        bl_region_type (str): Specifies the region type where the panel is displayed.
        bl_category (str): The tab category under which the panel appears.
        bl_label (str): The label displayed at the top of the panel.
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "villevite"
    bl_label = "villevite"

    def draw(self, context: bpy.types.Context) -> None:
        parameters = context.scene.cityproperties
        layout = self.layout

        box = layout.box()
        row1 = box.row()
        row2 = box.row()
        row2.prop(parameters, "coordinates")

        layout.operator("villevite.generate_city", text="Generate City")
        layout.operator("villevite.generate_street_mesh",
                        text="Generate Street Mesh")
        layout.operator("villevite.surprise", text="Surprise Me")
        layout.operator("villevite.clear_all", text="Clear All")
