import os
import sys
import unittest
from pathlib import Path

from drb.factory import DrbFactoryResolver
from drb.utils.logical_node import DrbLogicalNode

from drb.exceptions import DrbFactoryException


class TestDrbImageSignature(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    image_tif_one = current_path / "files" / 'GeogToWGS84GeoKey5.tif'
    image_png = current_path / "files" / 'png-248x300.png'
    image_jp2 = current_path / "files" / 'relax.jp2'
    empty_file = current_path / "files" / 'empty_file'

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

    def test_resolve_tif_ok(self):
        node = DrbLogicalNode(self.image_tif_one)
        signature, node = self.resolver.resolve(node)
        self.assertEqual(signature.label, 'image')

    def test_resolve_png_ok(self):
        node = DrbLogicalNode(self.image_png)
        signature, node = self.resolver.resolve(node)
        self.assertEqual(signature.label, 'image')

    def test_resolve_jp2_ok(self):
        node = DrbLogicalNode(self.image_jp2)
        signature, node = self.resolver.resolve(node)
        self.assertEqual(signature.label, 'image')

    def test_resolve_no_image(self):
        node = DrbLogicalNode(self.empty_file)
        try:
            signature, node = self.resolver.resolve(node)
            self.assertNotEqual(signature.label, 'image')
        except DrbFactoryException:
            pass
