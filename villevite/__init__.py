# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""Handles the registration and unregistration of the add-on classes and properties."""
import bpy

from . import operators
from . import ui
from . import properties

classes = [
    ui.VIEW3D_PT_SidePanel,
    operators.OperatorGenerateCity,
    operators.OperatorReadOSM,
    operators.OperatorSurprise,
    properties.CityProperties,
    operators.OperatorClearAll,
]


def register() -> None:
    """
    Register the add-on classes and properties.
    """
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.cityproperties = bpy.props.PointerProperty(
        type=properties.CityProperties)


def unregister() -> None:
    """
    Unregister the add-on classes and properties.
    """
    del bpy.types.Scene.cityproperties
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
