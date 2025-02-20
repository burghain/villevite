import bpy
import os
import sys
import unittest
import pytest

import bl_ext.user_default.cityGen as cityGen


class TestOperators(unittest.TestCase):
    def test_OBJECT_OT_AddBuilding(self):
        print("In test_OBJECT_OT_AddBuilding")
        self.assertEqual(1, 1)


if __name__ == "__main__":
    pytest.main(["-v", "./tests/"])
