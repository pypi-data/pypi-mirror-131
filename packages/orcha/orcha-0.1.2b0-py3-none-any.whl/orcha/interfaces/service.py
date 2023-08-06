from dataclasses import dataclass, field

from daemon import DaemonContext

from orcha.lib.manager import Manager


@dataclass(frozen=True)
class ServiceWrapper:
    manager: Manager = field(init=True, compare=False, hash=False)
    context: DaemonContext = field(init=True, compare=False, hash=False, default=None)


__all__ = ["ServiceWrapper"]
