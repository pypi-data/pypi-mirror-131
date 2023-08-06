import os
import uuid

from drb import DrbNode
from drb.factory import DrbSignature, DrbFactory, DrbSignatureType

from .json_node_factory import JsonNodeFactory


class DrbJsonSignature(DrbSignature):
    def __init__(self):
        self._factory = JsonNodeFactory()

    @property
    def uuid(self) -> uuid.UUID:
        return uuid.UUID('c6f7d210-4df0-11ec-81d3-0242ac130003')

    @property
    def label(self) -> str:
        return 'json'

    @property
    def category(self) -> DrbSignatureType:
        return DrbSignatureType.FORMATTING

    @property
    def factory(self) -> DrbFactory:
        return self._factory

    def match(self, node: DrbNode) -> bool:
        supported_ext = {
            '.json'
        }

        filename, file_extension = os.path.splitext(node.path.filename)
        if 'Content-Type' in node.attributes.keys():
            return 'json' in node.get_attribute('Content-Type')
        return file_extension and file_extension.lower() in supported_ext
