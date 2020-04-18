from queue import Queue
import time
from typing import List
import cherrypy
from jinja2 import Environment, PackageLoader, select_autoescape


class TriangleWeb:
    """Web API for running triangle shows."""
    def __init__(self, queue: Queue, runner: "ShowRunner", show_names: List[str]):
        self.queue = queue
        self.runner = runner
        self.shows = show_names

        self.env = Environment(
            loader=PackageLoader(__name__, 'templates'),
            autoescape=select_autoescape(default_for_string=True, default=True)
        )

    @cherrypy.expose
    def index(self):
        # set a no-cache header so the show status is up to date
        cherrypy.response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate, max-age=0"
        cherrypy.response.headers['Expires'] = 0

        template = self.env.get_template("index.html")
        return template.render(status=self.runner.status(), shows=self.shows)

    @cherrypy.expose
    def clear_show(self):
        self.queue.put("clear")
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def change_run_time(self, run_time=None):
        try:
            run_time = int(run_time)
        except ValueError:
            raise cherrypy.HTTPError(400)

        print(f'changing run_time to: {run_time}')
        self.queue.put(f'inc runtime:{run_time}')
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def change_brightness(self, brightness_scale=1.0):
        self.queue.put(f'brightness:{brightness_scale}')
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def run_show(self, show_name=None):
        if show_name is None or show_name not in self.shows:
            raise cherrypy.HTTPError(400)

        self.queue.put(f'run_show:{show_name}')
        print(f'setting show to: {show_name}')

        # XXX otherwise the runner.status() method hasn't had time to update
        time.sleep(0.2)
        raise cherrypy.HTTPRedirect('/')
