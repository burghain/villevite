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
        layout = self.layout

        layout.operator("villevite.load_default_road_graph",
                        text="Load Default Road Graph")
        layout.operator("villevite.generate_city", text="Generate City")
        layout.operator("villevite.generate_city",
                        text="Prepare for Scanning").for_scanning = True
        layout.operator("villevite.clear_all", text="Clear All")
