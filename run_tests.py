import bpy
import pytest
import os
import sys


def install_addon(addon_path):
    bpy.ops.preferences.addon_install(filepath=os.path.abspath(addon_path))
    bpy.ops.preferences.addon_enable(module="cityGen")
    bpy.ops.wm.save_userpref()


install_addon("cityGen.zip")
installed_addons = bpy.context.preferences.addons.keys()
if "cityGen" in installed_addons and bpy.context.preferences.addons["cityGen"].module:
    print("cityGen installed successfully!")

import cityGen

print(sys.modules["cityGen"])

pytest.main(["/home/josua/.config/blender/4.3/scripts/addons/cityGen/tests/", "-v"])
