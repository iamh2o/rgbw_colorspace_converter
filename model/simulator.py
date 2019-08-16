"""
Model to communicate with a Simulator over a TCP socket.
"""
import logging
import queue
import socket

from color import Color
from grid import Address, Cell
from .base import ModelBase

SIM_DEFAULT = (188, 210, 229)  # BCD2E5, "off" color for simulator
logger = logging.getLogger("pyramidtriangles")


class SimulatorModel(ModelBase):
    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.hostname, self.port))

        # queue of 'dirty' messages to send
        self.message_queue = queue.SimpleQueue()

    def __repr__(self):
        return f'{__class__.__name__} (hostname={self.hostname}, port={self.port})'

    def set(self, cell: Cell, addr: Address, color: Color):
        # Enqueue a message to simulator, sets address
        msg = f"{str(cell.id)} {','.join(map(str, color.rgb))}\n"
        self.message_queue.put(msg)

    def go(self):
        while not self.message_queue.empty():
            msg = self.message_queue.get()
            logger.debug(msg)
            self.sock.send(msg.encode())
