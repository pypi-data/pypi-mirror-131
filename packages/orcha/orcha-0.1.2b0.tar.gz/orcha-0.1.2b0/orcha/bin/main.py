import importlib
import pkgutil
import sys
from typing import Type

from ..plugins import BasePlugin
from orcha.utils.logging_utils import get_logger


log = get_logger()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Orcha command line utility for handling services")
    parser.add_argument(
        "--listen-address",
        metavar="ADDRESS",
        type=str,
        default="127.0.0.1",
        help="Listen address of the service",
    )
    parser.add_argument(
        "--port",
        metavar="N",
        type=int,
        default=50000,
        help="Listen port of the service",
    )
    parser.add_argument(
        "--key",
        metavar="KEY",
        type=str,
        default=None,
        help="Authentication key used for verifying clients",
    )
    subparsers = parser.add_subparsers(
        description="Available commands installed from external plugins",
        required=True,
        metavar="Commands",
    )

    discovered_plugins = {
        name: importlib.import_module(name)
        for _, name, _ in pkgutil.iter_modules()
        if name.startswith("orcha_")
    }

    plugins = set()

    for plugin, mod in discovered_plugins.items():
        pl: Type[BasePlugin] = getattr(mod, "plugin", None)
        if pl is None:
            log.warning(
                f'invalid plugin specified for "{plugin}". Is there a plugin export class defined in __init__?'
            )
            continue

        plugins.add(pl(subparsers))

    args = parser.parse_args()
    for plugin in plugins:
        if plugin.can_handle(args.owner):
            return plugin.handle(args)


if __name__ == "__main__":
    sys.exit(main())
