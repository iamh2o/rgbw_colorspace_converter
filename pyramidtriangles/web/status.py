from dataclasses import asdict
import cherrypy

from .latest_status import LatestStatus


@cherrypy.expose
@cherrypy.tools.json_out()
class Status:
    def __init__(self, status: LatestStatus):
        self.status = status

    def GET(self):
        return asdict(self.status.latest())
