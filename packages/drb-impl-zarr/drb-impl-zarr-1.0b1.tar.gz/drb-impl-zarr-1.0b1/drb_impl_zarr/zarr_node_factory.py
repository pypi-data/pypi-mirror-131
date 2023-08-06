from typing import Any, List, Dict, Tuple, Optional

from drb import DrbNode, AbstractNode
from drb.factory import DrbFactory
from drb.path import ParsedPath
import zarr

from drb_impl_zarr.exceptions import DrbZarrNodeException
from drb_impl_zarr.zarr_data_set_node import DrbZarrDataSetNode


class DrbZarrNode(AbstractNode):

    def __init__(self, base_node: DrbNode):
        super().__init__()

        self.base_node = base_node
        self._children: List[DrbNode] = None

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.base_node.parent

    @property
    def path(self) -> ParsedPath:
        return self.base_node.path

    @property
    def name(self) -> str:
        return self.base_node.name

    @property
    def namespace_uri(self) -> Optional[str]:
        return self.base_node.namespace_uri

    @property
    def value(self) -> Optional[Any]:
        return self.base_node.value

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self.base_node.attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        return self.base_node.get_attribute(name, namespace_uri)

    @property
    def children(self) -> List[DrbNode]:
        if self._children is None:
            try:
                root_data_set = zarr.open(self.base_node.path.name)
                root_node = DrbZarrDataSetNode.\
                    create_node_from_data_set(self, root_data_set)
                self._children = [root_node]
            except Exception as e:
                raise DrbZarrNodeException(f'Unable to read zarr file'
                                           f' {self.name} ') from e
        return self._children

    def has_child(self) -> bool:
        return True

    def has_impl(self, impl: type) -> bool:
        return self.base_node.has_impl(impl)

    def get_impl(self, impl: type) -> Any:
        return self.base_node.get_impl(impl)

    def close(self):
        self.base_node.close()


class DrbZarrFactory(DrbFactory):

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbZarrNode(base_node=node)
