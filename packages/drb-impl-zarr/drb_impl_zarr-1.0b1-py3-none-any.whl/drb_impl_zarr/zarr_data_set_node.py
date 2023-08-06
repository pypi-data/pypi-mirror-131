import enum
from abc import ABC
from typing import Any, List, Optional, Union, Dict, Tuple

import drb
import zarr

from drb import DrbNode, AbstractNode
from drb.exceptions import DrbNotImplementationException, DrbException
from drb.path import ParsedPath


class DrbZarrAttributeNames(enum.Enum):
    READ_ONLY = 'read_only'


class DrbZarrDataSetNode(AbstractNode, ABC):

    def __init__(self, parent: DrbNode, name: str,
                 data_set: Union[zarr.hierarchy.Group, zarr.core.Array]):
        super().__init__()

        self._data_set = data_set
        self._parent: DrbNode = parent
        self._name = name
        self._path = None
        self._attributes: Dict[Tuple[str, str], Any] = None

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    def close(self) -> None:
        pass

    @property
    def path(self) -> ParsedPath:
        if self._path is None:
            self._path = self.parent.path / self.name
        return self._path

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            for key in self._data_set.attrs.keys():
                self._attributes[key, None] = self._data_set.attrs[key]
            self._attributes[DrbZarrAttributeNames.READ_ONLY.value, None] = \
                self._data_set.read_only
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        key = (name, namespace_uri)
        if key in self.attributes.keys():
            return self.attributes[key]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    def value(self) -> Optional[Any]:
        return None

    def has_impl(self, impl: type) -> bool:
        if impl is self._data_set.__class__:
            return True

    def get_impl(self, impl: type) -> Any:
        if self.has_impl(impl):
            return self._data_set
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    @staticmethod
    def create_node_from_data_set(parent, data_set):
        name = data_set.name
        if name and name[0] == '/':
            name = name[1:]
        if not name:
            name = '.'
        if isinstance(data_set, zarr.hierarchy.Group):
            node = DrbZarrGroupNode(parent, name, data_set)
        else:
            node = DrbZarrArrayNode(parent, name, data_set)
        return node


class DrbZarrGroupNode(DrbZarrDataSetNode):

    def __init__(self, parent: DrbNode, name: str,
                 data_set: Union[zarr.hierarchy.Group, zarr.core.Array]):
        super().__init__(parent, name, data_set)
        self._children: List[DrbNode] = None

    @property
    @drb.resolve_children
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            self._data_set.visitvalues(self.add_data_set_children)
        return self._children

    def has_child(self) -> bool:
        return len(self.children) > 0

    def add_data_set_children(self, data_set):
        child = DrbZarrDataSetNode.create_node_from_data_set(self, data_set)
        self._children.append(child)

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: int = 1) -> Union[DrbNode, List[DrbNode]]:
        if occurrence is None or (not isinstance(occurrence, int)
                                  or occurrence < 0):
            raise DrbException(f'Invalid occurrence: {occurrence}')
        if self._children is None:
            try:
                if namespace_uri is None:
                    data_set = self._data_set[name]
                    if occurrence == 0:
                        return [self.create_node_from_data_set(self, data_set)]
                    elif occurrence == 1:
                        return self.create_node_from_data_set(self, data_set)
                raise DrbException(f'Child ({name},{occurrence}) not found')
            except (IndexError, TypeError, KeyError) as error:
                raise DrbException(f'Child ({name},{occurrence}) not found') \
                    from error
        else:
            return super()._get_named_child(name, namespace_uri, occurrence)


class DrbZarrArrayNode(DrbZarrDataSetNode):

    def __init__(self, parent: DrbNode, name: str,
                 data_set: Union[zarr.hierarchy.Group, zarr.core.Array]):
        super().__init__(parent, name, data_set)

    @property
    def children(self) -> List[DrbNode]:
        return []

    def has_child(self) -> bool:
        return False
