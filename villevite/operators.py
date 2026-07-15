"""
This module defines various operators for the Villevite Blender add-on.

Operators include functionality for loading the default road graph, generating
cities, clearing all objects, and adjusting the clipping distance in the 3D viewport.
"""

import bpy
from .city.city_generator import CityGenerator
from . import assets
from . import road_graph


def clear_all() -> None:
    """
    Remove all objects, node groups, and collections from the Blender scene to reset it for debug purposes.
    """
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    for group in bpy.data.node_groups:
        bpy.data.node_groups.remove(group, do_unlink=True)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection, do_unlink=True)


def increase_clipping_distance() -> None:
    """
    Increase the clipping distance for the 3D viewport in the current workspace. Neccessary to view large cities.
    """
    if bpy.context.screen is None:  # background mode has no viewport
        return
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.clip_start = 0.1
                    space.clip_end = 100000.0


class OperatorGenerateCity(bpy.types.Operator):
    """
    Blender Operator to generate a city from a road graph.

    Uses the active (or first valid selected) road graph object; if none is
    found, the Default Road Graph is loaded from Nodes.blend and used instead.
    """
    bl_idname: str = "villevite.generate_city"
    bl_label: str = "Generate City"
    bl_options: set = {"REGISTER", "UNDO"}

    for_scanning: bpy.props.BoolProperty(
        name="Prepare for Scanning",
        description="Bake the city to real objects and extract scan paths",
        default=False,
    )

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        """
        Should only be executable in object mode.
        """
        return context.mode == "OBJECT"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """
        Execute the operator to generate a city.
        """
        graph = road_graph.find_road_graph(context)
        if graph is None:
            try:
                graph = road_graph.ensure_default_road_graph(context)
            except (ValueError, OSError) as error:
                self.report({'ERROR'}, str(error))
                return {'CANCELLED'}
            self.report({'INFO'}, f"No road graph selected, using '{graph.name}'")

        citygen = CityGenerator(graph)

        if not self.for_scanning:
            citygen.generate()
            self.report(
                {'INFO'},
                f"GeoCity modifier attached to '{graph.name}'. Edit parameters on the modifier.",
            )
            return {"FINISHED"}

        result = citygen.generate_for_scanning()

        if not result:
            self.report({'WARNING'}, "Failed to generate city for scanning.")
            return {'CANCELLED'}

        # Check for scan paths
        scan_paths = result.get(f"{citygen.SCAN_PATH_NAME}s")
        if scan_paths and len(scan_paths.objects) > 0:
            self.report({'INFO'}, f"Successfully created {len(scan_paths.objects)} scan path(s)")
        else:
            self.report({'WARNING'}, "No scan paths were created!")
        return {"FINISHED"}


class OperatorLoadDefaultRoadGraph(bpy.types.Operator):
    """
    Operator to append the Default Road Graph from Nodes.blend and make it active.
    """
    bl_idname: str = "villevite.load_default_road_graph"
    bl_label: str = "Load Default Road Graph"
    bl_options: set = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        """
        Should only be executable in object mode.
        """
        return context.mode == "OBJECT"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """
        Execute the operator to load the Default Road Graph.
        """
        try:
            obj = road_graph.ensure_default_road_graph(context)
        except (ValueError, OSError) as error:
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}

        for other in context.selected_objects:
            other.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        self.report({'INFO'}, f"'{obj.name}' is active")
        return {"FINISHED"}


class OperatorClearAll(bpy.types.Operator):
    """
    Operator to clear all objects, node groups, and collections from the scene.
    """
    bl_idname: str = "villevite.clear_all"
    bl_label: str = "Clear all"
    bl_options: set = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        """
        Execute the operator to clear all objects, node groups, and collections.
        """
        clear_all()
        increase_clipping_distance()
        return {"FINISHED"}
