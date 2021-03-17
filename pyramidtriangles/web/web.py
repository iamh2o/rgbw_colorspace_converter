from __future__ import annotations
from logging import getLogger
from pathlib import Path
from queue import Queue
import cherrypy
from typing import Optional

from ..core import PlaylistController
from .brightness import Brightness
from .cycle_time import CycleTime
from .latest_status import LatestStatus
from .playlist import Playlist
from .shows import Shows
from .show_knob import ShowKnob
from .speed import Speed
from .status import Status

# Suppressing logging to terminal for cherrypy access logs, which are really noisy.
# The log is still written to `log/cherrypy_access.log` though.
getLogger("cherrypy").propagate = False


class Web:
    """Web API for running triangle shows."""
    def __init__(self, command_queue: Queue, status_queue: Queue[Status]):
        # In-memory DB is easier than organizing thread-safety around all operations. At least one connection must stay
        # open. 'self.db' shouldn't be closed.
        self.db = PlaylistController()

        status = LatestStatus(status_queue)

        # These all are REST endpoints, path denoted by the variable name (e.g. /cycle_time).
        self.brightness = Brightness(command_queue, status)
        self.cycle_time = CycleTime(command_queue, status)
        self.playlist = Playlist(command_queue, self.db)
        self.shows = Shows(command_queue)
        self.show_knob = ShowKnob(command_queue)
        self.speed = Speed(command_queue, status)
        self.status = Status(status)

    @staticmethod
    def build_config(config: Optional[dict] = None) -> dict:
        """
        Builds a cherrypy config by merging settings into the config argument.
        Exposed so tests can reuse this config.
        """
        if config is None:
            config = {}

        config.update({
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.gzip.on': True,
                'tools.staticdir.on': True,
                'tools.staticdir.dir': Path(__file__).parent/'../../js/public',
                'tools.staticdir.index': 'index.html',
            }
        })
        return config

    def start(self, config):
        """Starts the cherrypy server and blocks."""
        config = self.build_config(config)
        cherrypy.config.update({
            'log.access_file': 'log/cherrypy_access.log',
            'log.screen': False,
        })

        # this method blocks until KeyboardInterrupt
        cherrypy.quickstart(self, '/', config=config)
