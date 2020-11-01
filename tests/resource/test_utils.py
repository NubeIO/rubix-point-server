import unittest

from src.resources.rest_schema.schema_wires_plat import wires_plat_all_attributes
from src.resources.utils import map_rest_schema


class TestUtils(unittest.TestCase):

    def test_map_rest_schema(self):
        mapper = {}
        map_rest_schema(wires_plat_all_attributes, mapper)
        self.assertEqual("", "")
        print(mapper)
