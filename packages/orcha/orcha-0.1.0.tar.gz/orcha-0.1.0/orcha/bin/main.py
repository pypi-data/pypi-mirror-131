import importlib
import pkgutil
import sys
from typing import Type

from ..plugins import BasePlugin
from orcha.utils.logging_utils import get_logger
import orcha.plugins


log = get_logger()


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


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
        for finder, name, ispkg in iter_namespace(orcha.plugins)
    }

    plugins = set()

    for plugin, mod in discovered_plugins:
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
