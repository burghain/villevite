import bpy
import pytest
from bl_ext.user_default.villevite import assets
from ..fixtures import import_assets_and_tests


def get_test_groups_names():
    assets.import_tests()
    return [
        ng.name for ng in bpy.data.node_groups if ng.name.startswith('.test: ')]


def evaluate_node_group(group_name: str):
    test_group = bpy.data.node_groups[group_name]
    mesh = bpy.data.meshes.new("TestMesh")
    obj = bpy.data.objects.new("TestObject", mesh)
    bpy.context.collection.objects.link(obj)
    modifier = obj.modifiers.new(name="TestModifier", type='NODES')
    node_tree = bpy.data.node_groups.new(
        name='NewGeometryNodesTree', type='GeometryNodeTree')
    modifier.node_group = node_tree

    node_tree.nodes.new('NodeGroupInput')

    output_node = node_tree.nodes.new('NodeGroupOutput')

    test_node = node_tree.nodes.new("GeometryNodeGroup")
    test_node.node_tree = test_group

    node_tree.interface.new_socket(
        name="Geometry", socket_type='NodeSocketGeometry', in_out="OUTPUT",)
    node_tree.interface.new_socket(
        name="Error", socket_type='NodeSocketBool', in_out="OUTPUT",)
    node_tree.links.new(
        test_node.outputs['Error'], output_node.inputs['Error'])

    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()

    errors = [
        warning.message for warning in modifier.node_warnings if warning.type == 'ERROR']

    # Cleanup
    bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.meshes.remove(mesh)
    bpy.data.node_groups.remove(node_tree)
    return errors


@pytest.mark.parametrize("group_name", get_test_groups_names())
def test_node_group(group_name, import_assets_and_tests, ):
    results = evaluate_node_group(group_name)
    print(f"Testing {group_name} with {len(results)} errors")
    assert len(
        results) == 0, str(results)
