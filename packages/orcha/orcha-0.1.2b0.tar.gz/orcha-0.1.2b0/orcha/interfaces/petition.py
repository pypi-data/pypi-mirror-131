from queue import Queue
import subprocess
from abc import ABC
from dataclasses import dataclass, field
from typing import Callable, Union, NoReturn, Type, TypeVar

ProcT = Union[subprocess.Popen, int]
ActionCallbackT = Callable[[ProcT], NoReturn]

P = TypeVar("P", bound="Petition")


@dataclass(order=True)
class Petition(ABC):
    priority: int = field(init=False)
    id: int = field(compare=False)
    queue: Queue = field(compare=False, repr=False)
    action: Callable[[ActionCallbackT, Type[P]], NoReturn] = field(compare=False, repr=False)
    condition: Callable[[Type[P]], bool] = field(compare=False, repr=False)


@dataclass(init=False)
class EmptyPetition(Petition):
    priority = float("inf")
    id = -1
    queue = None
    action = None
    condition = None

    def __init__(self):
        pass


__all__ = ["ProcT", "ActionCallbackT", "Petition", "EmptyPetition"]
