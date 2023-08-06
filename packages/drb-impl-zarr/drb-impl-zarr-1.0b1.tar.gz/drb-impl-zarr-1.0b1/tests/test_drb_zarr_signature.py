import os
import sys
import unittest
from pathlib import Path

from drb.factory import DrbFactoryResolver
from drb.utils.logical_node import DrbLogicalNode

from drb.exceptions import DrbFactoryException


class TestDrbZarrSignature(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))

    zarr_ok2 = current_path / "files" / "sample.zarr"
    not_zarr_files = current_path / "files" / "empty.file"

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
        node = DrbLogicalNode(self.zarr_ok2)
        signature, node = self.resolver.resolve(node)
        self.assertEqual(signature.label, 'zarr')

    def test_resolve_no_zarr(self):
        node = DrbLogicalNode(self.not_zarr_files)
        try:
            signature, node = self.resolver.resolve(node)
            self.assertNotEqual(signature.label, 'zarr')
        except DrbFactoryException:
            pass
