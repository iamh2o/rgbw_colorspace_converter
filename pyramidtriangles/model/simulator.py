from __future__ import annotations
from collections.abc import Iterable
from logging import getLogger
import queue
import socket

from . import DisplayColor
from ..grid import Cell

SIM_DEFAULT = (188, 210, 229)  # BCD2E5, "off" color for simulator
logger = getLogger(__name__)


class SimulatorModel:
    """
    Model to communicate with a Processing simulator over a TCP socket.
    """
    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port

        try:
            self.sock = socket.create_connection((self.hostname, self.port), 2.0)  # 2 second timeout
        except ConnectionError as e:
            e.filename = f"{self.hostname}:{self.port}"
            raise

        # queue of 'dirty' messages to send
        self.message_queue = queue.SimpleQueue()

    def __repr__(self):
        return f'{SimulatorModel.__name__} (hostname={self.hostname}, port={self.port})'

    def set(self, cell: Cell, addr, color: DisplayColor):
        # Enqueue a message to simulator, sets address
        msg = f"{str(cell.id)} {','.join(map(str, color.rgb256))}\n"
        self.message_queue.put(msg)

    def go(self):
        while not self.message_queue.empty() and self.sock is not None:
            msg = self.message_queue.get()
            logger.debug(msg)
            self.sock.send(msg.encode())

    def activate(self, cells: Iterable[Cell]):
        """No activation needed for simulator."""
        pass

    def stop(self):
        self.sock.close()
        self.sock = None
