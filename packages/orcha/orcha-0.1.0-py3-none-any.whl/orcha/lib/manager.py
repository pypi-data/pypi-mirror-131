from abc import ABC, abstractmethod
import multiprocessing
from multiprocessing.managers import SyncManager
from queue import Queue
from typing import Callable, Optional, Union

from orcha.exceptions import ManagerShutdownError
from orcha.interfaces.message import Message

from orcha.utils.logging_utils import get_logger
from orcha.interfaces import Petition
from orcha.processor import Processor
from orcha import properties

log = get_logger()
_queue = multiprocessing.Queue()
_finish_queue = multiprocessing.Queue()


class Manager(ABC):
    def __init__(
        self,
        listen_address: str = properties.listen_address,
        port: int = properties.port,
        auth_key: bytes = properties.authkey,
        create_processor: bool = True,
        queue: Queue = None,
        finish_queue: Queue = None,
        is_client: bool = False,
    ):
        self.manager = SyncManager(address=(listen_address, port), authkey=auth_key)
        self.create_processor = create_processor
        self.is_client = is_client
        self._set_lock = multiprocessing.Lock()
        self._enqueued_messages = set()
        self._shutdown = multiprocessing.Value("b", False)

        # clients don't need any processor
        if create_processor and not is_client:
            log.debug("creating processor for <%s>", self)
            queue = queue or _queue
            finish_queue = finish_queue or _finish_queue
            self.processor = Processor(queue, finish_queue, self)

        log.debug("manager created - running setup...")
        self.setup()

    @property
    def processor(self) -> Processor:
        if not self.create_processor or self.is_client:
            raise RuntimeError("this manager has no processor")

        return self._processor

    @processor.setter
    def processor(self, processor: Processor):
        if not self.create_processor or self.is_client:
            raise RuntimeError("this manager does not support processors")

        self._processor = processor

    def connect(self):
        log.debug("connecting to manager")
        self.manager.connect()

    def start(self):
        log.debug("starting manager")
        self.manager.start()

    def serve(self):
        server = self.manager.get_server()
        server.serve_forever()

    def shutdown(self):
        self._shutdown.value = True
        try:
            if self.create_processor and not self.is_client:
                log.debug("shutting down processor")
                self.processor.shutdown()

            log.debug("finishing manager")
            self.manager.shutdown()
            self.manager.join()

            log.debug("parent handler finished")
        except Exception as e:
            log.critical(f"unexpected error during shutdown! -> {e}", exc_info=True)

    def join(self):
        log.debug("waiting for manager...")
        self.manager.join()
        log.debug("manager joined")

    def register(self, name: str, func: Optional[Callable] = None, **kwargs):
        log.debug('registering callable "%s" with name "%s"', func, name)
        self.manager.register(name, func, **kwargs)

        def temp(*args, **kwds):
            return getattr(self.manager, name)(*args, **kwds)

        setattr(self, name, temp)

    def send(self, m: Message):
        """stub"""

    def finish(self, m: Union[Message, int]):
        """stub"""

    def _add_message(self, m: Message):
        if not self._shutdown.value:
            return self.processor.enqueue(m)

        log.debug("we're off - enqueue petition not accepted for message with ID %d", m.id)
        raise ManagerShutdownError("manager has been shutdown - no more petitions are accepted")

    def _finish_message(self, m: Union[Message, int]):
        if not self._shutdown.value:
            return self.processor.finish(m)

        log.debug(
            "we're off - finish petition not accepted for message with ID %d",
            m.id if isinstance(m, Message) else m,
        )
        raise ManagerShutdownError("manager has been shutdown - no more petitions are accepted")

    def setup(self):
        send_fn = None if self.is_client else self._add_message
        finish_fn = None if self.is_client else self._finish_message

        self.register("send", send_fn)
        self.register("finish", finish_fn)

    def is_running(self, x: Union[Message, Petition, int]):
        if isinstance(x, (Message, Petition)):
            x = x.id

        with self._set_lock:
            return x in self._enqueued_messages

    @property
    def running_processes(self) -> int:
        with self._set_lock:
            return len(self._enqueued_messages)

    @abstractmethod
    def convert_to_petition(self, m: Message) -> Optional[Petition]:
        raise RuntimeError("must override!")

    @abstractmethod
    def on_start(self, p: Petition):
        with self._set_lock:
            self._enqueued_messages.add(p.id)
        log.info("starts execution of petition %d", p.id)

    @abstractmethod
    def on_finish(self, p: Petition):
        with self._set_lock:
            self._enqueued_messages.remove(p.id)
        log.info("finishes execution of petition %d", p.id)


__all__ = ["Manager"]
