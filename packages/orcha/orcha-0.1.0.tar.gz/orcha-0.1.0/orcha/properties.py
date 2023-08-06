"""When working with an Orcha project, properties are expected to be stored here"""
from typing import Optional


# When defining a <SyncManager>, "listen_address" specifies where to listen to
listen_address: str = "127.0.0.1"

# When creating a <SyncManager>, the port to listen to
port: int = 50000

# When creating a <SyncManager>, the authentication key used by other processes
authkey: Optional[bytes] = None

# Extra properties that you may want to store when working with the project
extras = {}


__all__ = ["listen_address", "port", "authkey", "extras"]
