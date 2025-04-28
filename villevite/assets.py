"""This module provides functions to import test node groups and assets from the Assets folder."""

import os
from typing import List
import bpy


library_path = os.path.join(os.path.dirname(__file__), "Assets")


def import_tests() -> None:
    """
    Import test node groups from .blend files located in the Assets directory.

    This function loads node groups from .blend files that start with ".test: "
    and are not already present in the current Blender data.
    """
    for file in os.listdir(library_path):
        if file.endswith(".blend"):
            blend_path = os.path.join(library_path, file)
            with bpy.data.libraries.load(blend_path, link=False, assets_only=False) as (
                data_from,
                data_to,
            ):
                to_import: List[str] = [
                    test_group
                    for test_group in data_from.node_groups
                    if test_group not in bpy.data.node_groups and test_group.startswith(".test: ")
                ]
                all_node_groups = data_to.node_groups
                all_node_groups.extend(to_import)
                data_to.node_groups = all_node_groups


def import_assets() -> None:
    """
    Import assets (objects, collections, and node groups) that have not been imported yet
    from .blend files located in the Assets directory.
    """
    for file in os.listdir(library_path):
        if file.endswith(".blend"):
            blend_path = os.path.join(library_path, file)
            with bpy.data.libraries.load(blend_path, link=False, assets_only=True) as (
                data_from,
                data_to,
            ):
                asset_types = ("objects", "collections", "node_groups")
                for asset_type in asset_types:
                    to_import: List[str] = [
                        asset
                        for asset in getattr(data_from, asset_type)
                        if asset not in getattr(bpy.data, asset_type)
                    ]
                    all_objects = getattr(data_to, asset_type)
                    all_objects.extend(to_import)
                    setattr(data_to, asset_type, all_objects)
