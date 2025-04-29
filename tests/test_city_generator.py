import bpy


def atest_operator_generate_city():
    bpy.ops.villevite.generate_city()
    assert bpy.data.objects.get(
        "City") is not None, "City object was not created"
