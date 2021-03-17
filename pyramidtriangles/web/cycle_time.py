from __future__ import annotations
import cherrypy
from collections.abc import Mapping
from logging import getLogger
from queue import Queue

from ..core import RuntimeCmd
from .latest_status import LatestStatus

logger = getLogger(__name__)


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class CycleTime:
    def __init__(self, queue: Queue, status: LatestStatus):
        self.queue = queue
        self.status = status

    def GET(self) -> Mapping[str, int]:
        return {'value': self.status.latest().max_show_time}

    def POST(self) -> None:
        data = cherrypy.request.json
        if 'value' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'value'")
        value = data['value']

        logger.info('received new cycle time %s', value)
        self.queue.put(RuntimeCmd(int(value)))
