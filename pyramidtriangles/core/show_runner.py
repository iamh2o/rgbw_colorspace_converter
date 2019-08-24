from __future__ import annotations
from collections.abc import Generator, Iterable, Mapping
from dataclasses import dataclass
from logging import getLogger
from queue import Queue, Empty
import sqlite3
import time
from threading import Event, Thread
from typing import Optional, Any


from .. import util
from ..grid import Pyramid
from ..shows import Show, KnobValue, load_shows, random_shows
from .playlist_controller import PlaylistController

logger = getLogger(__name__)


def make_interpolator():
    low_interp = util.make_interpolator(0.0, 0.5, 2.0, 1.0)
    hi_interp = util.make_interpolator(0.5, 1.0, 1.0, 0.5)

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
    def __init__(self,
                 pyramid: Pyramid,
                 command_queue: Queue,
                 status_queue: Queue,
                 shutdown: Event,
                 max_showtime: int,
                 fail_hard: bool):
        # Set thread name
        super(ShowRunner, self).__init__(name=type(self).__name__)

        self.pyramid = pyramid
        self.command_queue = command_queue
        self.status_queue = status_queue
        self.shutdown = shutdown
        self.__max_show_time = max_showtime
        self.fail_hard = fail_hard

        # default settings
        self.__brightness_scale = 1.0
        self.__speed_scale = 1.0
        self.show_start_time = 0.0

        # map of names -> show constructors
        self.shows = dict(load_shows())
        self.random_show_sequence = random_shows()
        self.playlist = PlaylistController()

        # show state variables
        self.show: Optional[Show] = None
        self.prev_show: Optional[Show] = None
        self.framegen: Generator[float, None, None] = (_ for _ in ())

    def _send_status(self):
        """
        Enqueue a status update in queue for consumers.
        """
        status = self.status
        if status:
            self.status_queue.put(status)

    @property
    def status(self):
        """
        Returns the status of the ShowRunner.
        """
        if self.show is None:
            return None

        knobs_json = []
        if self.show.knobs:
            knobs_json = self.show.knobs.json_array

        # Represents JSON status object
        return Status(
            show=self.show.name,
            show_start_time=self.show_start_time,
            knobs=knobs_json,
            max_show_time=self.max_show_time,
            brightness_scale=self.brightness_scale,
            speed_scale=self.speed_scale)

    def process_command_queue(self):
        msgs = []
        while True:
            try:
                msgs.append(self.command_queue.get_nowait())
            except Empty:
                break
        [self._process_command(cmd) for cmd in msgs]

    def _process_command(self, msg):
        if isinstance(msg, ClearCmd):
            self.clear()
            self.shutdown.wait(2.0)
        elif isinstance(msg, RunShowCmd):
            self.next_show(msg.show)
        elif isinstance(msg, RuntimeCmd):
            self.max_show_time = msg.runtime
        elif isinstance(msg, BrightnessCmd):
            self.brightness_scale = msg.brightness
        elif isinstance(msg, SpeedCmd):
            self.speed_scale = msg.speed
        elif isinstance(msg, ShowKnobCmd):
            curr_show_name = self.show.name if self.show else ''
            if curr_show_name != msg.show:
                logger.info('Received knob value for show %s but show %s running', msg.show, curr_show_name)
                return
            if self.show.knobs:
                self.show.knobs[msg.name] = msg.value
        elif isinstance(msg, tuple):
            logger.debug('OSC: %s', msg)

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
                    logger.info('setting speed_x to: %f', self.speed_scale)

        else:
            logger.warning('ignoring unknown msg: %s', msg)

    def clear(self):
        """Clears all panels."""
        self.pyramid.clear()

    def next_show(self, name: Optional[str] = None):
        """
        Sets the next show to run, in priority of:
            1. Show passed as `name` argument
            2. Show in playlist
            3. Show from semi-random sequence generator
        """
        show_cls: Optional[type[Show]] = None
        if name:
            if name in self.shows:
                show_cls = self.shows[name]
            else:
                logger.warning('unknown show as argument: %s', name)

        if not show_cls:
            try:
                name = self.playlist.next()
            except sqlite3.DatabaseError as e:
                logger.error('error getting next show from playlist, skipping: %s', e)

            if name:
                if name in self.shows:
                    show_cls = self.shows[name]
                else:
                    logger.warning('unknown show from playlist: %s', name)

        if not show_cls:
            logger.info("choosing random show")
            (name, show_cls) = next(self.random_show_sequence)

        self.clear()
        self.prev_show = self.show

        logger.info('next show: %s', name)
        self.show = show_cls(self.pyramid)
        self.show_start_time = time.perf_counter()
        self.framegen = self.show.next_frame()
        self._send_status()

    def get_next_frame(self):
        """return a delay or None"""
        try:
            return next(self.framegen)
        except StopIteration:
            return None

    def run(self):
        if not self.show or not self.framegen:
            logger.info("Next Next Next")
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
                        logger.info("max show time elapsed, changing shows")
                        self.next_show()
                else:
                    logger.info("show is out of frames, waiting...")
                    self.shutdown.wait(2)
                    self.next_show()
            except KeyboardInterrupt:
                raise
            except Exception:
                logger.exception('unexpected exception in show loop while running %s', self.show.name)
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
        self._send_status()

    @property
    def brightness_scale(self) -> float:
        return self.__brightness_scale

    @brightness_scale.setter
    def brightness_scale(self, brightness: float):
        """Sets brightness in [0, 1]."""
        self.__brightness_scale = min(max(0.0, brightness), 1.0)
        self.pyramid.face.model.brightness = self.__brightness_scale
        self._send_status()

    @property
    def speed_scale(self) -> float:
        return self.__speed_scale

    @speed_scale.setter
    def speed_scale(self, speed: float):
        """Sets show speed multiplier in [0.5, 2.0], 1.0 is normal, lower is faster, higher is slower."""
        self.__speed_scale = min(max(0.5, speed), 2.0)
        self._send_status()


@dataclass
class Status:
    """Represents current status of ShowRunner"""
    show: str
    show_start_time: float
    max_show_time: int
    brightness_scale: float
    speed_scale: float
    # {show: [{knob1: {_some values_}}, ...]}
    knobs: Iterable[Mapping[str, Mapping[str, Any]]]
    seconds_remaining: int = 0


@dataclass(frozen=True)
class ClearCmd:
    """Clears panels and waits a couple seconds."""
    pass


@dataclass(frozen=True)
class RunShowCmd:
    """Run this show now."""
    show: Optional[str]


@dataclass(frozen=True)
class RuntimeCmd:
    """Change show running time."""
    runtime: int


@dataclass(frozen=True)
class BrightnessCmd:
    """Change brightness scale in [0, 1]."""
    brightness: float


@dataclass(frozen=True)
class ShowKnobCmd:
    show: str
    name: str
    value: KnobValue


@dataclass(frozen=True)
class SpeedCmd:
    speed: float
