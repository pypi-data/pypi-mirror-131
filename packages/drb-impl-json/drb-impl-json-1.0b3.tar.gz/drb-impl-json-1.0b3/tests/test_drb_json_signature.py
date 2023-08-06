import os
import sys
import unittest

from drb.factory import DrbFactoryResolver
from drb.utils.logical_node import DrbLogicalNode


class TestJsonSignature(unittest.TestCase):
    path = 'tests/resources/test.json'

    @classmethod
    def setUpClass(cls) -> None:
        path = os.path.dirname(__file__)

        cls.mock_package_path = os.path.abspath(
            os.path.join(path, 'resources'))
        sys.path.append(cls.mock_package_path)

        cls.resolver = DrbFactoryResolver()

    @classmethod
    def tearDownClass(cls) -> None:
        sys.path.remove(cls.mock_package_path)

    def test_resolve_ok(self):
        node = DrbLogicalNode(self.path)
        signature = self.resolver.resolve(node)
        assert 'json' == signature[0].label
