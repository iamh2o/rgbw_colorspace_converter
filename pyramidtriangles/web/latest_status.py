from __future__ import annotations
import time
from queue import Queue, Empty
from typing import Optional

from ..core import Status


class LatestStatus:
    """Wraps a Queue of Status updates to supply the most recent status."""
    def __init__(self, queue: Queue[Status]):
        self.queue = queue
        self.status: Optional[Status] = None

    def latest(self) -> Optional[Status]:
        while True:
            try:
                self.status = self.queue.get_nowait()
            except Empty:
                break

        status = self.status
        now = time.perf_counter()
        if status:
            status.seconds_remaining = status.max_show_time - int(now - status.show_start_time)
        return status
