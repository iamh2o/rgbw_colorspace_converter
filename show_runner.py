import logging
from dataclasses import dataclass
from queue import Queue, Empty
import time
from threading import Event, Thread
from typing import Optional, Generator

import shows
import util
from grid import Pyramid
from shows import ShowBase

logger = logging.getLogger("pyramidtriangles")


def make_interpolator():
    low_interp = util.make_interpolater(0.0, 0.5, 2.0, 1.0)
    hi_interp = util.make_interpolater(0.5, 1.0, 1.0, 0.5)

    def interpolation(val):
        """
        Interpolation function to map OSC input into ShowRunner speed_x
        Values range from 0.0 to 1.0
        input 0.5 => 1.0
        input < 0.5 ranges from 2.0 to 1.0
        input > 0.5 ranges from 1.0 to 0.5
        """
        if val == 0.5:
            return 1.0
        elif val < 0.5:
            return low_interp(val)
        else:
            return hi_interp(val)
    return interpolation


speed_interpolation = make_interpolator()


class ShowRunner(Thread):
    __max_show_time: int
    __brightness_scale = 1.0
    __speed_scale = 1.0
    show_start_time = 0.0
    show: Optional[ShowBase] = None
    prev_show: Optional[ShowBase] = None
    framegen: Generator[float, None, None] = iter(())

    def __init__(self,
                 pyramid: Pyramid,
                 command_queue: Queue,
                 shutdown: Event,
                 max_showtime: int = 240,
                 fail_hard: bool = True):
        # Set thread name
        super(ShowRunner, self).__init__(name=type(self).__name__)

        self.pyramid = pyramid
        self.command_queue = command_queue
        self.shutdown = shutdown
        self.__max_show_time = max_showtime
        self.fail_hard = fail_hard

        # map of names -> show constructors
        self.shows = dict(shows.load_shows())
        self.random_show_sequence = shows.random_shows()

    @property
    def status(self):
        """
        Returns the status of the ShowRunner.
        """
        if self.show is None:
            return "Not running"
        else:
            now = time.perf_counter()
            elapsed = now - self.show_start_time
            remaining = self.max_show_time - elapsed
            return "Running %s (%d seconds left)" % (self.show.name, remaining)

    def process_command_queue(self):
        msgs = []
        while True:
            try:
                msgs.append(self.command_queue.get_nowait())
            except Empty:
                break
        [self._process_command(cmd) for cmd in msgs]

    def _process_command(self, msg) -> None:
        if isinstance(msg, ClearCmd):
            self.clear()
            self.shutdown.wait(2.0)
        elif isinstance(msg, RunShowCmd):
            self.next_show(msg.show)
        elif isinstance(msg, RuntimeCmd):
            self.max_show_time = msg.runtime
        elif isinstance(msg, BrightnessCmd):
            self.brightness_scale = msg.brightness
        elif isinstance(msg, tuple):
            logger.debug(f'OSC: {msg}')

            (addr, val) = msg
            addr = addr.split('/z')[0]
            val = val[0]
            assert addr[0] == '/'
            (ns, cmd) = addr[1:].split('/')
            if ns == '1':
                # control command
                if cmd == 'next':
                    self.next_show()
                elif cmd == 'previous':
                    if self.prev_show:
                        self.next_show(self.prev_show.name)
                elif cmd == 'speed':
                    self.speed_scale = speed_interpolation(val)
                    print(f"setting speed_x to: '{self.speed_scale}'")

        else:
            logger.warning(f"ignoring unknown msg: '{msg}'")

    def clear(self):
        """Clears all panels."""
        self.pyramid.clear()

    def next_show(self, name=None):
        """
        Sets the next show to run, in priority of:
            1. Show passed as argument
            2. Show from semi-random sequence generator
        """
        show_cls = None
        if name:
            if name in self.shows:
                show_cls = self.shows[name]
            else:
                logger.warning(f"unknown show as argument: '{name}'")

        if not show_cls:
            logger.info("choosing random show")
            (name, show_cls) = next(self.random_show_sequence)

        self.clear()
        self.prev_show = self.show

        print(f'next show: {name}')
        self.show = show_cls(self.pyramid)
        self.show_start_time = time.perf_counter()
        self.framegen = self.show.next_frame()

    def get_next_frame(self):
        """return a delay or None"""
        try:
            return next(self.framegen)
        except StopIteration:
            return None

    def run(self):
        if not (self.show and self.framegen):
            print("Next Next Next")
            self.next_show()

        # Loops until the shutdown event is triggered
        while not self.shutdown.is_set():
            try:
                self.process_command_queue()

                delay = self.get_next_frame()
                self.pyramid.go()
                if delay:
                    real_delay = delay * self.speed_scale
                    self.shutdown.wait(real_delay)  # shutdown.wait() is like time.sleep() but can be interrupted

                    now = time.perf_counter()
                    elapsed = now - self.show_start_time
                    if elapsed > self.max_show_time:
                        print("max show time elapsed, changing shows")
                        self.next_show()
                else:
                    print("show is out of frames, waiting...")
                    self.shutdown.wait(2)
                    self.next_show()

            except Exception:
                logger.exception("unexpected exception in show loop!")
                if self.fail_hard:
                    raise
                self.next_show()

    @property
    def max_show_time(self) -> int:
        return self.__max_show_time

    @max_show_time.setter
    def max_show_time(self, show_time: int):
        """Sets show_time, at least 5 seconds."""
        self.__max_show_time = show_time if show_time >= 5 else 5

    @property
    def brightness_scale(self) -> float:
        return self.__brightness_scale

    @brightness_scale.setter
    def brightness_scale(self, brightness: float):
        """Sets brightness in [0, 1]."""
        self.__brightness_scale = min(max(0.0, brightness), 1.0)
        self.pyramid.face.model.brightness = self.__brightness_scale

    @property
    def speed_scale(self):
        return self.__speed_scale

    @speed_scale.setter
    def speed_scale(self, speed: float):
        """Sets show speed multiplier in [0.5, 2.0], 1.0 is normal, lower is faster, higher is slower."""
        self.__speed_scale = min(max(0.5, speed), 2.0)


@dataclass(frozen=True)
class ClearCmd:
    """Clears panels and waits a couple seconds."""
    pass


@dataclass(frozen=True)
class RunShowCmd:
    """Run this show now."""
    show: str


@dataclass(frozen=True)
class RuntimeCmd:
    """Change show running time."""
    runtime: int


@dataclass(frozen=True)
class BrightnessCmd:
    """Change brightness scale in [0, 1]."""
    brightness: float
