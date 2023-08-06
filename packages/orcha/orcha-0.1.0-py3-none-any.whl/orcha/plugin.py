import argparse
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(init=False)
class BasePlugin(ABC):
    name: str = field(init=False)
    aliases: tuple = field(init=False, default=())
    help: str = field(init=False, default=None)

    def __init__(self, subparser):
        self._subparser = subparser
        self.parser = self.create_parser(self._parser)

    @property
    def _parser(self) -> argparse.ArgumentParser:
        kwargs = {
            "name": self.name,
            "aliases": self.aliases,
        }
        if self.help is not None:
            kwargs["help"] = self.help

        p = self._subparser.add_parser(**kwargs)
        p.set_defaults(owner=self)
        return p

    def can_handle(self, owner) -> bool:
        return self == owner

    @abstractmethod
    def create_parser(self, parser: argparse.ArgumentParser):
        ...

    @abstractmethod
    def handle(self, namespace: argparse.Namespace) -> int:
        ...


__all__ = ["BasePlugin"]
