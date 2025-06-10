"""
This module defines various operators for the Villevite Blender add-on.

Operators include functionality for generating cities, reading OSM data, clearing all objects, and adjusting the clipping distance in the 3D viewport.
"""

import bpy
from .osm.osm_generator import OSMGenerator
from .city.city_generator import CityGenerator
from . import assets


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
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.clip_start = 0.1
                    space.clip_end = 100000.0


class OperatorGenerateCity(bpy.types.Operator):
    """
    Blender Operator to generate a city with the given parameters.
    """
    bl_idname: str = "villevite.generate_city"
    bl_label: str = "Generate City"
    bl_options: set = {"REGISTER", "UNDO"}

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
        parameters = context.scene.cityproperties
        citygen = CityGenerator(parameters)
        citygen.generate()
        return {"FINISHED"}


class OperatorReadOSM(bpy.types.Operator):
    """
    Operator to generate street meshes from OSM data.

    Attributes:
        bl_idname (str): Unique identifier for the operator.
        bl_label (str): Display name for the operator.
        bl_options (set): Options for the operator, such as undo support.
    """
    bl_idname: str = "villevite.generate_street_mesh"
    bl_label: str = "Generate Street Mesh"
    bl_options: set = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        """
        Execute the operator to generate street meshes from OSM data.
        """
        parameters = context.scene.cityproperties

        OSMGenerator(stringcoords=parameters.coordinates).generate()
        return {"FINISHED"}


class OperatorSurprise(bpy.types.Operator):
    """
    Operator to execute a surprise action, such as importing test assets.
    """
    bl_idname: str = "villevite.surprise"
    bl_label: str = "Surprise me!"
    bl_options: set = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        """
        Execute the operator to perform a surprise action.

        Args:
            context(bpy.types.Context): The current Blender context.

        Returns:
            set[str]: A set containing the execution status.
        """
        bpy.ops.object.select_all(action='DESELECT')


        obj = bpy.data.objects.get("City")
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        # Apply the visual geometry to objects operator
        bpy.ops.object.visual_geometry_to_objects()

        # Join all objects with 'Wall' in their name
        wall_objs = [obj for obj in bpy.data.objects if "Wall" in obj.name]
        if wall_objs:
            # Deselect all, then select only wall objects
            for obj in bpy.data.objects:
                obj.select_set(False)
            for obj in wall_objs:
                obj.select_set(True)
            context.view_layer.objects.active = wall_objs[0]
            bpy.ops.object.join()

        # Organize all other objects into collections by the name before the first '.'
        for obj in bpy.data.objects:
            if "Wall" in obj.name:
                continue  # Skip the joined wall object
            # Use the part before the first '.' as the collection name
            col_name = obj.name.split('.', 1)[0]
            if col_name not in bpy.data.collections:
                new_col = bpy.data.collections.new(col_name)
                bpy.context.scene.collection.children.link(new_col)
            else:
                new_col = bpy.data.collections[col_name]
            # Remove from all collections except the new one
            for col in obj.users_collection:
                if col != new_col:
                    col.objects.unlink(obj)
            # Link to the new collection if not already linked
            if obj.name not in new_col.objects:
                new_col.objects.link(obj)

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
