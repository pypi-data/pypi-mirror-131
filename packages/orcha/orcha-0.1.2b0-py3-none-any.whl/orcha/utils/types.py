from abc import ABCMeta, abstractmethod
from typing import TypeVar


class _Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other) -> bool:
        ...


Comparable = TypeVar("Comparable", bound=_Comparable)
