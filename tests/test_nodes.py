import bpy
import pytest
import os

from bl_ext.user_default.villevite import assets, nodes
from .fixtures import import_assets


@pytest.fixture
def setup_one_plane(clean_scene, building_gen_import):
    plane = bpy.ops.mesh.primitive_plane_add(size=20)
    plane = bpy.context.active_object
    plane.name = "TestPlane"
    geo_mod = plane.modifiers.new("Building Generator", "NODES")
    geo_mod.node_group = bpy.data.node_groups["buildingGen"]


def test_building_gen_exists(import_assets):
    assert "buildingGen" in bpy.data.node_groups


def building_generator_creates_instances(self, clean_scene):
    """Test if buildingGen node group properly generates building instances from a plane"""

    # 1. Create input plane
    bpy.ops.mesh.primitive_plane_add(size=10)
    plane = bpy.context.active_object
    plane.name = "TestPlane"

    # Store the initial scene state
    initial_object_count = len(bpy.data.objects)

    # 2. Apply buildingGen node group
    # Check if the node group exists, skip test if not
    if "buildingGen" not in bpy.data.node_groups:
        pytest.skip("buildingGen node group not found")

    # Create the modifier and assign the node group
    geo_mod = plane.modifiers.new("Building Generator", "NODES")
    geo_mod.node_group = bpy.data.node_groups["buildingGen"]

    # 3. For testing, we need to realize the instances
    # Add a "Realize Instances" node to the end of our node tree
    # This is a temporary modification to make instances countable
    node_group = bpy.data.node_groups["buildingGen"]

    # Store original links to restore later
    output_node = None
    original_connections = []

    for node in node_group.nodes:
        if node.bl_idname == "NodeGroupOutput":
            output_node = node
            # Store original connections to restore
            for link in node_group.links:
                if (
                    link.to_node == output_node
                    and link.to_socket.identifier == "Geometry"
                ):
                    original_connections.append(
                        (link.from_node, link.from_socket))
            break

    # Add realize instances node
    realize_node = node_group.nodes.new("GeometryNodeRealizeInstances")
    realize_node.location = (output_node.location.x -
                             200, output_node.location.y)

    # Reconnect the nodes
    if original_connections:
        for node, socket in original_connections:
            # Connect source → realize_node
            node_group.links.new(socket, realize_node.inputs["Geometry"])
            # Connect realize_node → output
            node_group.links.new(
                realize_node.outputs["Geometry"], output_node.inputs["Geometry"]
            )

    # 4. Apply the modifier to evaluate results
    # Select the plane
    bpy.ops.object.select_all(action="DESELECT")
    plane.select_set(True)
    bpy.context.view_layer.objects.active = plane

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier=geo_mod.name)

    # 5. Perform assertions
    # Check if geometry was created (instance count can be measured in various ways)

    # Method 1: Count actual mesh elements (should increase from plane)
    mesh = plane.data
    assert len(
        mesh.vertices) > 4, "No geometry was generated beyond the original plane"
    assert len(mesh.polygons) > 1, "No building faces were generated"

    # Method 2: Check for hierarchical structure (if building uses collections)
    # This depends on how your buildingGen is implemented

    # Method 3: Check for height (buildings should extend in Z)
    z_coords = [v.co.z for v in mesh.vertices]
    max_height = max(z_coords)
    assert max_height > 0.1, f"Building height seems too low: {max_height}"

    # Method 4: Check for material slots (if your building generator assigns materials)
    if hasattr(plane, "material_slots"):
        assert (
            len(plane.material_slots) > 0
        ), "No materials were assigned to the building"

    # 6. Restore the original node group (clean up)
    # Remove the realize node
    if realize_node:
        # Restore original connections
        for node, socket in original_connections:
            for link in node_group.links:
                if link.to_node == realize_node:
                    node_group.links.remove(link)
                if link.from_node == realize_node:
                    node_group.links.remove(link)

            # Reconnect original setup
            node_group.links.new(socket, output_node.inputs["Geometry"])

        # Remove the realize node
        node_group.nodes.remove(realize_node)
