import bpy
import time
import argparse
import unittest
import pytest
import os
import sys

from .buildingGen import buildingGen


def install_addon(addon_path):
    bpy.ops.preferences.addon_install(filepath=addon_path)
    bpy.ops.preferences.addon_enable(module="cityGen")
    bpy.ops.wm.save_userpref()


install_addon("/mnt/Daten/Blender/cityGen/cityGen.zip")
installed_addons = bpy.context.preferences.addons.keys()

if "cityGen" in installed_addons and bpy.context.preferences.addons["cityGen"].module:
    print("[info] cityGen installed successfully!")


# pytest.main(["-v"])
