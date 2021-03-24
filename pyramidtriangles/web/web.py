from __future__ import annotations
import logging
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from queue import Queue, Empty
import cherrypy
from typing import Optional
import orjson

from ..color import HSV
from ..show_runner import BrightnessCmd, Playlist, RuntimeCmd, RunShowCmd, ShowKnobCmd, SpeedCmd
from ..playlist import Settings
from ..grid import Pyramid
from ..model.null import NullModel
from ..shows import load_shows

# Suppressing logging to terminal for cherrypy access logs, which are really noisy.
# The log is still written to `log/cherrypy_access.log` though.
logging.getLogger("cherrypy").propagate = False

logger = logging.getLogger(__name__)


class Web:
    """
    Web API for running triangle shows.

    This is a CherryPy base, so each REST endpoint is assigned to it. For example, requests to `/cycle_time` route to
    self.cycle_time.

    There are two queues used to pass information in a thread-safe way. The command_queue passes commands from Web to
    the ShowRunner, which changes the behavior of running shows. The status_queue passes information from the ShowRunner
    to Web to display the current status of what's running.
    """
    def __init__(self, command_queue: Queue, status_queue: Queue[Status]):
        # In-memory DB is easier than organizing thread-safety around all operations. At least one connection must stay
        # open. 'self.db' shouldn't be closed.
        self.db = Playlist()

        status = LatestStatus(status_queue)

        # These all are REST endpoints, path denoted by the variable name (e.g. /cycle_time).
        self.brightness = Brightness(command_queue, status)
        self.cycle_time = CycleTime(command_queue, status)
        self.playlist = PlaylistWeb(command_queue, self.db)
        self.shows = Shows(command_queue)
        self.show_knob = ShowKnob(command_queue)
        self.speed = Speed(command_queue, status)
        self.status = Status(status)

    @staticmethod
    def build_config(config: Optional[dict] = None) -> dict:
        """
        Builds a cherrypy config by merging some default settings into the `config` argument.
        Exposed so tests can reuse this config.
        """
        if config is None:
            config = {}

        config.update({
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'request.body.processors': {'application/json': orjson_processor},
                'tools.json_out.handler': orjson_handler,
                'tools.gzip.on': True,
                'tools.staticdir.on': True,
                'tools.staticdir.dir': Path(__file__).parent/'../../js/public',
                'tools.staticdir.index': 'index.html',
            }
        })
        return config

    def start(self, config):
        """Starts the cherrypy server and blocks the current thread."""
        config = self.build_config(config)
        cherrypy.config.update({
            'log.access_file': 'log/cherrypy_access.log',
            'log.screen': False,
        })

        # this method blocks until KeyboardInterrupt
        cherrypy.quickstart(self, '/', config=config)


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Brightness:
    """
    Handles requests under /brightness.
    """
    def __init__(self, queue: Queue, status: LatestStatus):
        self.queue = queue
        self.status = status

    def GET(self) -> dict:
        if latest := self.status.latest():
            return {'value': int(latest.brightness_scale * 100)}
        return {'value': 100}

    def POST(self):
        data = cherrypy.request.json
        if 'value' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'value'")
        brightness = data['value']/100.0
        self.queue.put(BrightnessCmd(brightness))


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class CycleTime:
    """
    Handles requests under /cycle_time.
    """
    def __init__(self, queue: Queue, status: LatestStatus):
        self.queue = queue
        self.status = status

    def GET(self) -> dict:
        if latest := self.status.latest():
            return {'value': latest.max_show_time}
        return {'value': 60}

    def POST(self) -> None:
        data = cherrypy.request.json
        if 'value' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'value'")
        value = data['value']

        logger.info('received new cycle time %s', value)
        self.queue.put(RuntimeCmd(int(value)))


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class PlaylistWeb:
    """
    Handles requests under /playlist.
    """
    def __init__(self, queue: Queue, playlist: Playlist):
        self.entries = Entry(playlist)
        self.queue = queue
        self.playlist = playlist

    def _current_playlist(self) -> dict:
        return {
            'playlist': self.playlist.current_playlist(),
            'playing': self.playlist.current_entry(),
        }

    def GET(self) -> dict:
        """
        Returns the current playlist of shows. [(id, show),...].
        """
        return self._current_playlist()

    def POST(self) -> dict:
        """
        Appends a show to the playlist and returns the new playlist.
        """
        data = cherrypy.request.json
        if 'show' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'show'")

        self.playlist.append(data['show'])
        return self._current_playlist()

    def DELETE(self) -> None:
        """
        Deletes all shows.
        """
        self.playlist.clear()

    def PUT(self) -> None:
        """
        Runs the playlist entry with {entry_id} as the current show.

        It works by setting {entry_id} to be the next playlist entry, then triggers the ShowRunner to play the next
        show.
        """
        data = cherrypy.request.json
        if 'entry_id' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'entry_id'")
        entry_id = data['entry_id']
        self.playlist.set_next(entry_id)
        self.queue.put(RunShowCmd(None))


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
@cherrypy.popargs('entry_id')
class Entry:
    """
    Handles requests under /playlist/entries/{entry_id}.

    A playlist entry. A show can have multiple entries, each with different settings.
    """
    def __init__(self, playlist: Playlist):
        self.playlist = playlist

    def GET(self, entry_id: int) -> Settings:
        """
        Returns the settings for a playlist entry, if any.

        Setting entries have the form:
        {
          Color: { h: 1.0, s: 1.0, v: 1.0 },
          Speed: 1.5,
          ...
        }
        """
        return self.playlist.get_settings(entry_id)

    def POST(self, entry_id: int) -> Settings:
        """
        Sets the show settings for a playlist entry. Returns the new setting.

        Request data should be a JSON object mapping a setting name to a value.
        { Color: { h: 1.0, s: 1.0, v: 1.0 } }
        or
        { Speed: 1.5 }
        """
        data = cherrypy.request.json

        # Merges settings from request with settings from database, with minimal validation.
        settings = self.playlist.get_settings(entry_id)
        for (key, value) in data.items():
            if isinstance(value, (int, float, dict)):
                settings[key] = value

        self.playlist.set_settings(entry_id, settings)
        return self.playlist.get_settings(entry_id)

    def DELETE(self, entry_id: int) -> None:
        """
        Deletes a show from the playlist.
        """
        self.playlist.delete(entry_id)


@dataclass
class Show:
    """Show is a simple object for JSON"""
    name: str
    description: str


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Shows:
    """
    Handles requests under /shows.
    """
    def __init__(self, queue: Queue):
        self.queue = queue
        self.shows = [Show(name=name, description=cls.description()) for (name, cls) in load_shows()]
        self.show_names = list(map(lambda x: x.name, self.shows))

    def GET(self) -> dict:
        """Returns listing of show names"""
        return {"shows": self.shows}

    def POST(self) -> None:
        """Sets the current show to request's 'data' key."""
        data = cherrypy.request.json
        if 'data' not in data:
            raise cherrypy.HTTPError(400, "'data' parameter missing in request")
        show_name = data['data']

        if show_name is None or show_name not in self.show_names:
            raise cherrypy.HTTPError(400, f"'{show_name}' not an available show")

        self.queue.put(RunShowCmd(show_name))


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class ShowKnob:
    """
    Handles requests under /show_knob.
    """
    def __init__(self, queue: Queue):
        self.queue = queue
        self.knobs = defaultdict(list)  # if the knob doesn't exist, you'll get []

        # load each show with a null model to get the available show knobs
        null_pyramid = Pyramid.build_single(NullModel())
        for (name, cls) in load_shows():
            show = cls(null_pyramid)
            if show.knobs:
                self.knobs[name] = show.knobs.json_array

    @cherrypy.popargs('show')
    def GET(self, show) -> list:
        """
        Returns the available knobs for the given show.

        [{
            name: 'Main Color',
            value: {
              default: { h: 1.0, s: 1.0, v: 1.0},
            },
            type: 'HSVKnob'
        }, {
            name: 'Speed',
            value: {
              default: 1.0,
            },
            type: 'ValueKnob'
        },
        ...]
        """
        return self.knobs[show]

    def POST(self) -> None:
        """
        Sets the knob `name` to value `value` for show `show`
        """
        data = cherrypy.request.json
        for p in ['show', 'name', 'value']:
            if p not in data.keys():
                raise cherrypy.HTTPError(400, f"missing parameter '{p}'")

        value = data['value']

        if isinstance(value, dict):
            if any([c not in value.keys() for c in 'hsv']):
                raise cherrypy.HTTPError(400, 'missing HSV parameter')

            try:
                value = HSV(*[value[c] for c in 'hsv'])
            except TypeError as e:
                raise cherrypy.HTTPError(400, e)

        self.queue.put_nowait(ShowKnobCmd(show=data['show'], name=data['name'], value=value))


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Speed:
    """
    Handles requests under /speed.

    Speed exposes the speed multiplier of the ShowRunner to get/set.
    """
    def __init__(self, queue: Queue, status: LatestStatus):
        self.queue = queue
        self.status = status

    def GET(self) -> dict:
        if latest := self.status.latest():
            return {"value": latest.speed_scale}
        return {"value": "1.0"}

    def POST(self) -> None:
        data = cherrypy.request.json
        if 'value' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'value'")
        speed = data['value']
        self.queue.put(SpeedCmd(speed))


@cherrypy.expose
@cherrypy.tools.json_out()
class Status:
    """
    Handles requests under /status.

    Status returns the current status of the ShowRunner.
    """
    def __init__(self, status: LatestStatus):
        self.status = status

    def GET(self):
        return self.status.latest()


class LatestStatus:
    """
    Wraps a Queue of Status updates to supply the most recent status.
    """
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


def orjson_processor(entity):
    """
    Read application/json data into request.json.

    This is an alternative to cherrypy's json_processor which sucks. This uses orjson which does a lot more.
    """
    if not entity.headers.get("Content-Length"):
        raise cherrypy.HTTPError(411)

    body = entity.fp.read()
    with cherrypy.HTTPError.handle(ValueError, 400, 'Invalid JSON document'):
        cherrypy.serving.request.json = orjson.loads(body)


def orjson_handler(*args, **kwargs):
    """Cherrypy response processor to serialize json because the builtin one sucks. This uses orjson."""
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return orjson.dumps(value)
