from queue import Queue
import cherrypy

from ..core import SpeedCmd
from .latest_status import LatestStatus


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Speed:
    def __init__(self, queue: Queue, status: LatestStatus):
        self.queue = queue
        self.status = status

    def GET(self):
        return {"value": self.status.latest().speed_scale}

    def POST(self):
        data = cherrypy.request.json
        if 'value' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'value'")
        speed = data['value']
        self.queue.put(SpeedCmd(speed))
