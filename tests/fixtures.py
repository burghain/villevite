import bpy
import pytest
from bl_ext.user_default.villevite import assets


def clear_all():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
    for group in bpy.data.node_groups:
        bpy.data.node_groups.remove(group)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)


@pytest.fixture
def import_assets():
    assets.import_assets_and_nodes()
    yield
    clear_all()


@pytest.fixture(scope="module")
def import_assets_and_tests():
    assets.import_assets_and_nodes()
    assets.import_tests()
    yield
    clear_all()
