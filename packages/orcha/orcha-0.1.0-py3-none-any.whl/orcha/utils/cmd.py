import subprocess
import psutil
import signal
import shlex
from typing import Callable, Any

from .logging_utils import get_logger

log = get_logger()


def run_command(
    cmd: str,
    on_start: Callable[[subprocess.Popen], Any] = None,
    on_output: Callable[[str], Any] = None,
    on_finish: Callable[[int], Any] = None,
    cwd=None,
):
    if on_start is None:
        on_start = lambda _: None

    if on_output is None:
        on_output = lambda _: None

    if on_finish is None:
        on_finish = lambda _: None

    command = shlex.split(cmd)
    log.debug("$ %s", cmd)
    log.debug("> %s", command)

    with subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1,
        cwd=cwd,
    ) as proc:
        on_start(proc)
        for line in proc.stdout:
            on_output(line)

        ret = proc.wait()
    on_finish(ret)


def kill_proc_tree(pid, including_parent=True):
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.send_signal(signal.SIGTERM)
        if including_parent:
            parent.send_signal(signal.SIGTERM)
    except psutil.NoSuchProcess:
        log.warning("error while trying to kill proccess with id %d", pid)
