"""This module provides functions to import test node groups and assets from the Assets folder."""

import os
from typing import List
import bpy


assets_path = os.path.join(os.path.dirname(__file__), "Assets")
nodes_path = os.path.join(os.path.dirname(__file__), "GeometryNodes")

def import_tests() -> None:
    """
    Import test node groups from .blend files located in the Assets directory.

    This function loads node groups from .blend files that start with ".test: "
    and are not already present in the current Blender data.
    """
    for file in os.listdir(nodes_path):
        if file.endswith(".blend"):
            blend_path = os.path.join(nodes_path, file)
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

def import_assets_and_nodes() -> None:
    """
    Import assets (objects, collections) and node groups that have not been imported yet
    from .blend files located in the Assets and GeometryNodes directory.
    """
    import_assets(assets_path)
    import_nodes(nodes_path)


def import_assets(path) -> None:
    """
    Import assets (objects, collections) that have not been imported yet
    from .blend files located in the given directory.
    """
    for file in os.listdir(path):
        if file.endswith(".blend"):
            blend_path = os.path.join(path, file)
            with bpy.data.libraries.load(blend_path, link=False, assets_only=True) as (
                data_from,
                data_to,
            ):
                asset_types = ("objects", "collections")
                for asset_type in asset_types:
                    to_import: List[str] = [
                        asset
                        for asset in getattr(data_from, asset_type)
                        if asset not in getattr(bpy.data, asset_type)
                    ]
                    all_objects = getattr(data_to, asset_type)
                    all_objects.extend(to_import)
                    setattr(data_to, asset_type, all_objects)

def import_nodes(path):
    """
    Import node groups that have not been imported yet
    from .blend files located in the given directory.
    """
    for file in os.listdir(path):
        if file.endswith(".blend"):
            blend_path = os.path.join(path, file)
            with bpy.data.libraries.load(blend_path, link=False, assets_only=True) as (
                data_from,
                data_to,
            ):
                to_import: List[str] = [
                    group
                    for group in data_from.node_groups
                    if group not in bpy.data.node_groups
                ]
                all_groups = data_to.node_groups
                all_groups.extend(to_import)
                data_to.node_groups = all_groups