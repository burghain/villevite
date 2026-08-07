"""This module contains functions to add node groups to objects and set their parameters."""

from typing import Any, Dict, List
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


def set_inputs(modifier: bpy.types.NodesModifier, inputs: Dict[str, Any]) -> List[str]:
    """
    Set the input parameters for a node group modifier based on a parameter dictionary.

    Returns the names that were applied; names the node group does not know are reported and
    skipped, so a parameter set outliving a node group change is visible rather than fatal.
    """
    interface_items = modifier.node_group.interface.items_tree
    applied: List[str] = []
    for input_name, input_value in inputs.items():
        if input_name in interface_items.keys():
            set_input(modifier, interface_items[input_name].identifier, input_value)
            applied.append(input_name)
        else:
            print(
                f"Input '{input_name}' not found in node group interface of group {modifier.node_group.name}"
            )
    return applied


def set_input(modifier: bpy.types.NodesModifier, identifier: str, value: Any) -> None:
    """
    Set one node group input by its socket identifier.

    Blender 5.0 moved modifier inputs off the modifier's ID properties and onto
    `modifier.properties.inputs`, where each socket is a struct with a `value`. Assigning the
    old way raises "id properties not supported for this type" there, so pick by what the
    running Blender offers rather than by version number.
    """
    properties = getattr(modifier, "properties", None)
    if properties is not None and hasattr(properties, "inputs"):
        getattr(properties.inputs, identifier).value = value
    else:
        modifier[identifier] = value
