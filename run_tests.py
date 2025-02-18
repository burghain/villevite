import bpy
import time
import argparse
import unittest
import pytest
import os
import sys


def install_addon(addon_path):
    bpy.ops.preferences.addon_install(filepath=addon_path)
    bpy.ops.preferences.addon_enable(module="cityGen")
    bpy.ops.wm.save_userpref()


install_addon("/mnt/Daten/Blender/cityGen/cityGen.zip")
installed_addons = bpy.context.preferences.addons.keys()
print(installed_addons)
if "cityGen" in installed_addons and bpy.context.preferences.addons["cityGen"].module:
    print("cityGen installed successfully!")

import cityGen

pytest.main(["/home/josua/.config/blender/4.3/scripts/addons/cityGen/tests/", "-v"])
