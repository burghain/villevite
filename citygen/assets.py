import bpy
import os

library_path = os.path.join(os.path.dirname(__file__), "Assets")


def import_nodes():
    import_asset(asset_name="Block Generator", asset_type="node_groups")


def import_group(name):
    import_asset(name, "node_groups")


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
                        if asset not in getattr(data_to, asset_type)
                    ]
                    all_objects = getattr(data_to, asset_type)
                    all_objects.extend(to_import)
                    setattr(data_to, asset_type, all_objects)
                    print(f"Imported {asset_type} {to_import}")


def append_node_group_to_geometry_nodes(modifier, node_group, position=(0, 0)):
    node_tree = modifier.node_group
    group_node = node_tree.nodes.new("GeometryNodeGroup")
    group_node.node_tree = node_group
    group_node.location = position

    return group_node


def import_asset(asset_name, asset_type, assets_only=True):
    asset_types = "objects, collections, node_groups"
    if asset_type not in asset_types:
        print("Unsupported asset type, must be one of", asset_types)
        return
    for file in os.listdir(library_path):
        if file.endswith(".blend"):
            blend_path = os.path.join(library_path, file)
            with bpy.data.libraries.load(
                blend_path, link=False, assets_only=assets_only
            ) as (
                data_from,
                _,
            ):
                data_list = getattr(data_from, asset_type)
                if asset_name in data_list:
                    with bpy.data.libraries.load(
                        blend_path, link=False, assets_only=assets_only
                    ) as (_, data_to):
                        setattr(data_to, asset_type, [asset_name])

                    print(f"Asset '{asset_name}' imported from {file}")

                    if asset_type == "OBJECT":
                        return bpy.data.objects.get(asset_name)
                    elif asset_type == "COLLECTION":
                        return bpy.data.collections.get(asset_name)
                    elif asset_type == "GROUP":
                        node_group = bpy.data.node_groups.get(asset_name)
                        if node_group and node_group.type == "GEOMETRY":
                            return node_group
                        else:
                            print(
                                f"Warning: Node group '{asset_name}' was found but is not a geometry node group"
                            )
                            return

    print(f"Asset '{asset_name}' not found in any .blend file in {library_path}")
