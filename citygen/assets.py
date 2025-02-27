import bpy
import os

library_name = "cityGen-Assets"
library_path = os.path.join(os.path.dirname(__file__), "Assets")


def register_library():
    if library_path not in bpy.context.preferences.filepaths.asset_libraries:
        bpy.context.preferences.filepaths.asset_libraries.new(
            name=library_name, directory=library_path
        )


def import_nodes():
    import_asset(asset_name="Block Generator", asset_type="GROUP")


def import_asset(asset_name, asset_type="OBJECT"):
    """
    Import an asset from a folder of .blend files without knowing which file contains it

    Args:
        library_path: Path to the folder containing .blend files
        asset_name: Name of the asset to import
        asset_type: Type of asset ('OBJECT', 'COLLECTION', 'GROUP')

    Returns:
        The imported asset or None if not found
    """
    if asset_type == "OBJECT":
        target_datablocks = "objects"
    elif asset_type == "COLLECTION":
        target_datablocks = "collections"
    elif asset_type == "GROUP":
        target_datablocks = "node_groups"
    else:
        print(f"Unsupported asset type: {asset_type}")
        return None

    for blend_file in os.listdir(library_path):
        if blend_file.endswith(".blend"):
            blend_path = os.path.join(library_path, blend_file)

            try:
                with bpy.data.libraries.load(
                    blend_path, link=False, assets_only=True
                ) as (data_from, _):
                    data_list = getattr(data_from, target_datablocks)
                    if asset_name in data_list:
                        with bpy.data.libraries.load(
                            blend_path, link=False, assets_only=True
                        ) as (_, data_to):
                            setattr(data_to, target_datablocks, [asset_name])

                        print(f"Asset '{asset_name}' imported from {blend_file}")

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
                                return None
            except Exception as e:
                print(f"Error processing {blend_path}: {e}")

    print(f"Asset '{asset_name}' not found in any .blend file in {library_path}")
    return None


def append_node_group_to_geometry_nodes(modifier, node_group, position=(0, 0)):
    """
    Adds an imported geometry node group to a geometry nodes modifier

    Args:
        modifier: The geometry nodes modifier to add the node group to
        node_group: The node group to add
        position: The position to place the node

    Returns:
        The newly created node group node
    """
    # Create a node group node
    node_tree = modifier.node_group
    group_node = node_tree.nodes.new("GeometryNodeGroup")
    group_node.node_tree = node_group
    group_node.location = position

    return group_node
