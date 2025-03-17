import bpy
import os

from . import nodes
from . import assets
from .osm.blender_mesh_gen import BlenderMeshGen
from .osm.osm_parser import OSMParser


def evaluate_node_group(test_group):

    mesh = bpy.data.meshes.new("TestMesh")
    obj = bpy.data.objects.new("TestObject", mesh)
    bpy.context.collection.objects.link(obj)

    modifier = obj.modifiers.new(name="TestModifier", type='NODES')
    node_tree = bpy.data.node_groups.new(
        name='NewGeometryNodesTree', type='GeometryNodeTree')
    modifier.node_group = node_tree

    input_node = node_tree.nodes.new('NodeGroupInput')

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

    errors = [warning.message for warning in modifier.node_warnings]

    # Cleanup
    bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.meshes.remove(mesh)
    bpy.data.node_groups.remove(node_tree)
    return errors


class OBJECT_OT_AddBuilding(bpy.types.Operator):
    "Create and initialize a new building"
    bl_idname = "object.add_building"
    bl_label = "Add Building"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=4)
        obj = bpy.context.object
        obj.name = "Building"
        group_name = "buildingGen"
        nodes.add_to_object(obj, group_name)
        modifier = obj.modifiers[group_name]
        inputs = {
            "Max Number Of Floors": 5,
            "Min Number of Floors": 4,
        }
        nodes.set_inputs(modifier, inputs)
        return {"FINISHED"}


class OBJECT_OT_Tests(bpy.types.Operator):
    "Deletes the selected building"
    bl_idname = "object.delete_building"
    bl_label = "Tests"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        assets.import_tests()
        test_groups = [
            ng for ng in bpy.data.node_groups if ng.name.startswith('.test: ')]
        for test in test_groups:
            for error_message in evaluate_node_group(test):
                print(error_message)
        return {"FINISHED"}


class OBJECT_OT_AppendBuildingGen(bpy.types.Operator):
    bl_idname = "object.add_building_gen"
    bl_label = "Import Assets"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        assets.import_all()
        return {"FINISHED"}


class OBJECT_OT_ReadOSM(bpy.types.Operator):
    bl_idname = "object.generate_street_mesh"
    bl_label = "Generate Street Mesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        library_path = os.path.join(os.path.dirname(__file__), "Assets")

        parser = OSMParser()
        g, v = parser.parse(os.path.join(library_path, 'potsdam-mini.osm'))
        gen = BlenderMeshGen(g)
        gen.generate()

        return {"FINISHED"}
