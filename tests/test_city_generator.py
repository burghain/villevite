import bpy

def test_city_collections_exist():
    bpy.ops.villevite.generate_city()
    scan_path_collection = bpy.data.collections.get("Scan Paths")
    assert scan_path_collection is not None, "Collection 'Scan Paths' should exist"
    assert bpy.data.collections.get("Instances") is not None, "Collection 'Instances' should exist"
    assert bpy.data.collections.get("Assets") is not None, "Collection 'Assets' should exist"

    assert len(scan_path_collection.objects) > 0, "Collection 'Scan Paths' should not be empty"
    for obj in scan_path_collection.objects:
        assert obj.type == "CURVE", f"Object {obj.name} in 'Scan Paths' should be a CURVE, found {obj.type}"
