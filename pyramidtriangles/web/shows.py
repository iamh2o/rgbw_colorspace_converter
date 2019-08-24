from dataclasses import dataclass, asdict
from queue import Queue
import cherrypy

from ..core import RunShowCmd
from ..shows import load_shows


@dataclass(frozen=True)
class Show:
    name: str
    description: str


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Shows:
    def __init__(self, queue: Queue):
        self.queue = queue
        self.shows = [Show(name=name, description=cls.description()) for (name, cls) in load_shows()]
        self.show_names = list(map(lambda x: x.name, self.shows))

    def GET(self):
        """Returns listing of show names"""
        return {"shows": [asdict(show) for show in self.shows]}

    def POST(self):
        """Sets the current show to request's 'data' key."""
        data = cherrypy.request.json
        if 'data' not in data:
            raise cherrypy.HTTPError(400, "'data' parameter missing in request")
        show_name = data['data']

        if show_name is None or show_name not in self.show_names:
            raise cherrypy.HTTPError(400, f"'{show_name}' not an available show")

        self.queue.put(RunShowCmd(show_name))
