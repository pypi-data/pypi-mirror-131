import logging
import signal
from pwd import getpwnam
from typing import Iterable

import daemon
import daemon.pidfile

from orcha.interfaces.service import ServiceWrapper
from orcha.lib.manager import Manager
from orcha.utils.logging_utils import get_logger

log = get_logger()


def register_service(
    manager: Manager,
    *,
    pidfile: str = None,
    fds: Iterable[int] = None,
    user: str = None,
    group: str = None,
    cwd: str = "/",
    stop_signal: int = signal.SIGTERM,
) -> ServiceWrapper:
    pid_file = daemon.pidfile.PIDLockFile(pidfile)
    preserved_fds = [
        handler.stream.fileno()
        for handler in log.handlers
        if isinstance(handler, logging.FileHandler) and handler.stream is not None
    ]
    if fds is not None:
        preserved_fds.extend(fds)

    uid = getpwnam(user) if user is not None else None
    gid = getpwnam(group) if group is not None else None

    return ServiceWrapper(
        manager,
        daemon.DaemonContext(
            working_directory=cwd,
            umask=0o022,
            pidfile=pid_file,
            files_preserve=preserved_fds,
            uid=uid,
            gid=gid,
            signal_map={stop_signal: lambda *_: manager.shutdown()},
        ),
    )


def start_service(service: ServiceWrapper):
    if service.context is not None:
        with service.context:
            return service.manager.serve()

    try:
        service.manager.start()
        service.manager.join()
    except KeyboardInterrupt:
        service.manager.shutdown()
        exit(0)


__all__ = ["register_service", "start_service"]
