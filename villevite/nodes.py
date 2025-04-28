"""This module contains functions to add node groups to objects and set their parameters."""

from typing import Any, Dict
import bpy


def add_to_object(
        target_object: bpy.types.Object,
        group_name: str,
        parameters: Dict[str, Any]) -> bpy.types.Object:
    """
    Add a node group to a Blender object and set its parameters.

    Args:
        target_object (bpy.types.Object): The Blender object to which the node group will be added.
        group_name (str): The name of the node group to add.
        parameters (Dict[str, Any]): A dictionary of parameter names and their values to set in the node group.
    Returns:
        bpy.types.Object: The modified Blender object with the node group added.
    """
    modifier = target_object.modifiers.new(group_name, "NODES")
    modifier.node_group = bpy.data.node_groups[group_name]
    set_inputs(modifier, parameters)
    return target_object


def set_inputs(modifier: bpy.types.NodesModifier, inputs: Dict[str, Any]) -> None:
    """
    Set the input parameters for a node group modifier based on a parameter dictionary.
    """
    interface_items = modifier.node_group.interface.items_tree
    for input_name, input_value in inputs.items():
        if input_name in interface_items.keys():
            identifier = interface_items[input_name].identifier
            modifier[identifier] = input_value
        else:
            print(
                f"Input '{input_name}' not found in node group interface of group {modifier.node_group.name}"
            )
