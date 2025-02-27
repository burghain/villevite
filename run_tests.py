import bpy
import os
import sys
import unittest
import pytest


if __name__ == "__main__":
    result = pytest.main(["./tests/"])
    if result != 0:
        sys.exit(1)
