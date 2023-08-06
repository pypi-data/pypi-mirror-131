import os
import uuid

from drb.factory import DrbSignature, DrbSignatureType, DrbFactory

from drb import DrbNode
from .image_node_factory import DrbImageFactory


class DrbImageSignature(DrbSignature):
    def __init__(self):
        self._factory = DrbImageFactory()

    @property
    def uuid(self) -> uuid.UUID:
        return uuid.UUID('b7e03ac0-2b62-11ec-8d3d-0242ac130003')

    @property
    def label(self) -> str:
        return 'image'

    @property
    def category(self) -> DrbSignatureType:
        return DrbSignatureType.FORMATTING

    @property
    def factory(self) -> DrbFactory:
        return self._factory

    def match(self, node: DrbNode) -> bool:
        supported_ext = {
            '.tif',
            '.tiff',
            '.image',
            '.jp2',
            '.png',
            '.gif',
            '.webp',
            '.bmp',
            '.jpeg',
            '.jpg',
            # '.blx',
            # '.kap',
            # '.dt0',
            # '.dt1',
            # '.bin',
            # '.gpkg',
            # '.mem'
        }

        filename, file_extension = os.path.splitext(node.path.filename)
        return file_extension and file_extension.lower() in supported_ext
