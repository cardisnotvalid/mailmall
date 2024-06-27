from typing import MutableSequence, TypeVar, Generic, Iterator, List


ListItemT = TypeVar("ListItemT")


class ListModel(MutableSequence, Generic[ListItemT]):
    _items: List[ListItemT]

    def __init__(self, items: List[ListItemT] = None) -> None:
        self._items = items if items is not None else []

    def __getitem__(self, index: int) -> ListItemT:
        return self._items[index]

    def __setitem__(self, index: int, value: ListItemT) -> None:
        self._items[index] = value

    def __delitem__(self, index: int) -> None:
        del self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[ListItemT]:
        return iter(self._items)

    def __repr__(self) -> str:
        return repr(self._items)

    def __str__(self) -> str:
        return str(self._items)

    def insert(self, index: int, value: ListItemT) -> None:
        self._items.insert(index, value)
