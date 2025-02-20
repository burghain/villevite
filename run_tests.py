import bpy
import os
import sys
import unittest
import pytest

import bl_ext.user_default.cityGen as cityGen

if __name__ == "__main__":
    result = pytest.main(["./tests/"])
    if result != 0:
        sys.exit(1)
