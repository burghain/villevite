import bpy
import pytest
from bl_ext.user_default.villevite import assets
from .fixtures import import_assets


def test_assets_import_all(import_assets):
    assert "City Generator" in bpy.data.node_groups


def test_assets_import_all_twice(import_assets):
    duplicate_existed_before = "City Generator.001" in bpy.data.node_groups
    assets.import_assets()
    assert "City Generator" in bpy.data.node_groups
    assert duplicate_existed_before == (
        "City Generator.001" in bpy.data.node_groups)
