from __future__ import annotations
import cherrypy
from collections.abc import Mapping
from queue import Queue

from ..core import BrightnessCmd
from .latest_status import LatestStatus


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Brightness:
    def __init__(self, queue: Queue, status: LatestStatus):
        self.queue = queue
        self.status = status

    def GET(self) -> Mapping[str, int]:
        brightness = int(self.status.latest().brightness_scale * 100)
        return {'value': brightness}

    def POST(self):
        data = cherrypy.request.json
        if 'value' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'value'")
        brightness = data['value']/100.0
        self.queue.put(BrightnessCmd(brightness))
