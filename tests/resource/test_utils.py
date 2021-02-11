import unittest

from src.resources.rest_schema.schema_network import network_all_attributes
from src.resources.utils import map_rest_schema


class TestUtils(unittest.TestCase):

    def test_map_rest_schema(self):
        mapper = {}
        map_rest_schema(network_all_attributes, mapper)
        print(mapper)
