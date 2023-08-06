import os
import uuid

from drb.factory import DrbSignature, DrbSignatureType, DrbFactory

from drb import DrbNode
from drb_impl_zip import DrbZipNode

from .zarr_node_factory import DrbZarrFactory


class DrbZarrSignature(DrbSignature):
    def __init__(self):
        self._factory = DrbZarrFactory()

    @property
    def uuid(self) -> uuid.UUID:
        return uuid.UUID('56e6509c-3666-11ec-8d3d-0242ac130003')

    @property
    def label(self) -> str:
        return 'zarr'

    @property
    def category(self) -> DrbSignatureType:
        return DrbSignatureType.FORMATTING

    @property
    def factory(self) -> DrbFactory:
        return self._factory

    def match(self, node: DrbNode) -> bool:
        supported_ext = {
            '.zarr'
        }

        if isinstance(node, DrbZipNode):
            try:
                if node.has_child() and node['.zarray'] is not None:
                    return True
            except Exception:
                pass

        filename, file_extension = os.path.splitext(node.path.filename)
        return file_extension and file_extension.lower() in supported_ext
