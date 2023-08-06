import multiprocessing
import random
import subprocess
from queue import Queue, PriorityQueue
from threading import Lock, Thread, Event
from time import sleep
from typing import Union, Dict, List, Optional

from orcha import properties
from orcha.interfaces.message import Message
from orcha.interfaces.petition import Petition, EmptyPetition
from orcha.utils.cmd import kill_proc_tree
from orcha.utils.logging_utils import get_logger


log = get_logger()


class Processor:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if Processor.__instance__ is None:
            instance = object.__new__(cls)
            instance.__must_init__ = True
            Processor.__instance__ = instance
        return Processor.__instance__

    def __init__(
        self,
        queue: multiprocessing.Queue = None,
        finishq: multiprocessing.Queue = None,
        manager=None,
    ):
        if self.__must_init__:
            if not all((queue, finishq, manager)):
                raise ValueError("queue & manager objects cannot be empty during init")

            self.lock = Lock()
            self.queue = queue
            self.finishq = finishq
            self.manager = manager
            self.running = True

            self._internalq = PriorityQueue()
            self._signals = Queue()
            self._threads: List[Thread] = []
            self._petitions: Dict[int, int] = {}
            self._gc_event = Event()
            self._process_t = Thread(target=self._process)
            self._internal_t = Thread(target=self._internal_process)
            self._finished_t = Thread(target=self._signal_handler)
            self._signal_t = Thread(target=self._internal_signal_handler)
            self._gc_t = Thread(target=self._gc)
            self._process_t.start()
            self._internal_t.start()
            self._finished_t.start()
            self._signal_t.start()
            self._gc_t.start()
            self.__must_init__ = False

    @property
    def running(self) -> bool:
        return self._running

    @running.setter
    def running(self, v: bool):
        with self.lock:
            self._running = v

    def exists(self, m: Union[Message, int]) -> bool:
        return self.manager.is_running(m)

    def enqueue(self, m: Message):
        self.queue.put(m)

    def finish(self, m: Union[Message, int]):
        if isinstance(m, Message):
            m = m.id

        log.debug("received petition for finish message with ID %d", m)
        self.finishq.put(m)

    def _process(self):
        log.debug("fixing internal digest key")
        multiprocessing.current_process().authkey = properties.authkey

        while self.running:
            log.debug("waiting for message...")
            m = self.queue.get()
            if m is not None:
                log.debug('converting message "%s" into a petition', m)
                p: Optional[Petition] = self.manager.convert_to_petition(m)
                if p is not None:
                    log.debug("> %s", p)
                    if self.exists(p.id):
                        log.warning("received message (%s) already exists", p)
                        p.queue.put(f'message with ID "{p.id}" already exists\n')
                        p.queue.put(None)
                        continue
                else:
                    log.debug(f'message "%s" is invalid, skipping...', m)
                    continue
            else:
                p = EmptyPetition()
            self._internalq.put(p)

    def _internal_process(self):
        last_seen = None
        while self.running:
            log.debug("waiting for internal petition...")
            p: Petition = self._internalq.get()
            if not isinstance(p, EmptyPetition):
                if p.condition(p):
                    log.debug('petition "%s" satisfied condition', p)
                    launch_t = Thread(target=self._start, args=(p,))
                    launch_t.start()
                    self._threads.append(launch_t)
                else:
                    log.debug('petition "%s" did not satisfy the condition, re-adding to queue', p)
                    self._internalq.put(p)
                    if p.id == last_seen:
                        log.debug(
                            'petition "%s" was already enqueued! waiting some time before polling',
                            p,
                        )
                        sleep(random.uniform(0.1, 0.5))
                    last_seen = p.id
            else:
                log.debug("received empty petition")

    def _start(self, p: Petition):
        log.debug('launching petition "%s"', p)

        def assign_pid(proc: Union[subprocess.Popen, int]):
            pid = proc if isinstance(proc, int) else proc.pid
            log.debug('assigning pid to "%d"', pid)
            self._petitions[p.id] = pid
            self.manager.on_start(p)

        try:
            # self.manager.on_start(p)
            p.action(assign_pid, p)
        except Exception as e:
            log.warning(
                'unhandled exception while running petition "%s" -> "%s"', p, e, exc_info=True
            )
        finally:
            log.debug('petition "%s" finished, triggering callbacks', p)
            self._petitions.pop(p.id, None)
            self._gc_event.set()
            self.manager.on_finish(p)

    def _signal_handler(self):
        log.debug("fixing internal digest key")
        multiprocessing.current_process().authkey = properties.authkey

        while self.running:
            log.debug("waiting for finish message...")
            m = self.finishq.get()
            self._signals.put(m)

    def _internal_signal_handler(self):
        while self.running:
            log.debug("waiting for internal signal...")
            m = self._signals.get()
            if isinstance(m, Message):
                m = m.id

            if m is not None:
                log.debug('received signal petition for message with ID "%d"', m)
                if m not in self._petitions:
                    log.warning('message with ID "%d" not found or not running!', m)

                pid = self._petitions[m]
                # proc.send_signal(signal.SIGINT)
                kill_proc_tree(pid, including_parent=False)
                log.debug('sent signal to process "%d" and all of its children', pid)

    def _gc(self):
        while self.running:
            self._gc_event.wait()
            self._gc_event.clear()
            for thread in self._threads:
                if not thread.is_alive():
                    log.debug('pruning thread "%s"', thread)
                    self._threads.remove(thread)

    def shutdown(self):
        try:
            log.info("finishing processor")
            self.running = False
            self.queue.put(None)
            self.finishq.put(None)
            self._gc_event.set()

            log.info("waiting for pending processes...")
            self._process_t.join()
            self._internal_t.join()

            log.info("waiting for pending signals...")
            self._finished_t.join()
            self._signal_t.join()

            log.info("waiting for garbage collector...")
            self._gc_t.join()

            log.info("waiting for pending operations...")
            for thread in self._threads:
                thread.join()

            log.info("finished")
        except Exception as e:
            log.critical(f"unexpected error during shutdown! -> {e}", exc_info=True)


__all__ = ["Processor"]
