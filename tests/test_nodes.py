import bpy
import pytest
import os

from bl_ext.user_default.villevite import assets, nodes
from .fixtures import import_assets


def get_test_node_groups():
    """Retrieve all geometry node groups that start with '.test: '"""
    return [ng for ng in bpy.data.node_groups if ng.name.startswith('.test: ')]


def test_get_node_groups():
    print(get_test_node_groups())


def evaluate_node_group(node_group):
    """Evaluate the geometry node group and return the boolean result and error message."""
    # Create a temporary object and assign the node group
    mesh = bpy.data.meshes.new("TestMesh")
    obj = bpy.data.objects.new("TestObject", mesh)
    bpy.context.collection.objects.link(obj)

    modifier = obj.modifiers.new(name="TestModifier", type='NODES')
    modifier.node_group = node_group

    # Evaluate the modifier to trigger execution
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()

    # Retrieve the error status and message
    warnings = modifier.node_warnings
    print(warnings)
    error_occurred = False
    error_message = ""

    # Cleanup
    bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.meshes.remove(mesh)

    return error_occurred, error_message


# Dynamically create pytest functions for each test node group
test_node_groups = get_test_node_groups()


def pytest_generate_tests(metafunc):
    if 'node_group' in metafunc.fixturenames:
        metafunc.parametrize('node_group', test_node_groups, ids=[
                             ng.name for ng in test_node_groups])


def test_node_group(node_group, import_assets):
    error_occurred, error_message = evaluate_node_group(node_group)
    assert not error_occurred, f"Assertion failed in node group '{node_group.name}': {error_message}"
