import bpy
import os

library_path = os.path.join(os.path.dirname(__file__), "Assets")


def import_all():
    for file in os.listdir(library_path):
        if file.endswith(".blend"):
            blend_path = os.path.join(library_path, file)
            with bpy.data.libraries.load(blend_path, link=False, assets_only=True) as (
                data_from,
                data_to,
            ):
                asset_types = ("objects", "collections", "node_groups")
                for asset_type in asset_types:
                    to_import = [
                        asset
                        for asset in getattr(data_from, asset_type)
                        if asset not in getattr(bpy.data, asset_type)
                    ]
                    all_objects = getattr(data_to, asset_type)
                    all_objects.extend(to_import)
                    setattr(data_to, asset_type, all_objects)
