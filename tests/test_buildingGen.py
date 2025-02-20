from bl_ext.user_default.cityGen.buildingGen import append_node_group


def test_add_nodes():
    print(dir(buildingGen))
    # buildingGen.append_node_group("buildingGen")

    assert bpy.data.node_groups.get("buildingGen") is not None
