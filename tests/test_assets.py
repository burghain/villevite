import bpy
import pytest
from bl_ext.user_default.villevite import assets
from .fixtures import import_assets


@pytest.fixture
def import_assets_twice(import_assets):
    assets.import_all()


def test_assets_import_all(import_assets):
    assert "buildingGen" in bpy.data.node_groups


def test_assets_import_all_twice(import_assets_twice):
    assert "buildingGen" in bpy.data.node_groups
    assert "buildingGen.001" not in bpy.data.node_groups
