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
