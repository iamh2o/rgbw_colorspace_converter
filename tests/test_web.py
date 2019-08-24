import queue
import cherrypy
from cherrypy.test import helper

from pyramidtriangles.core import RunShowCmd, RuntimeCmd
from pyramidtriangles.web import Web

command_queue = queue.LifoQueue()
status_queue = queue.Queue()


class WebTest(helper.CPWebCase):
    interactive = False

    @staticmethod
    def setup_server():
        web = Web(
            command_queue,
            status_queue,
        )
        cherrypy.tree.mount(web, '/', Web.build_config({}))

    def test_index_returns_something(self):
        # index.html basically loads all the other content
        self.getPage('/')
        self.assertStatus(200)
        self.assertInBody('Triangle show control')

    def test_cycle_time(self):
        assert command_queue.empty()

        body = '{"value":30}'
        self.getPage(
            url='/cycle_time',
            headers=[
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(body))),
            ],
            method='POST',
            body=body,
        )
        self.assertStatus(200)

        assert command_queue.get() == RuntimeCmd(30)
        assert command_queue.empty()

    def test_get_shows(self):
        self.getPage(
            url='/shows',
            headers=[
                ('Content-Type', 'application/json'),
                ('Content-Length', '0'),
            ],
            method='GET',
        )
        self.assertStatus(200)
        self.assertInBody('Warp')

    def test_run_show(self):
        assert command_queue.empty()

        body = '{"data":"Warp"}'
        self.getPage(
            url='/shows',
            headers=[
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(body))),
            ],
            method='POST',
            body=body,
        )
        self.assertStatus(200)

        assert command_queue.get() == RunShowCmd('Warp')
        assert command_queue.empty()

        body = '{"data":"Invalid"}'
        self.getPage(
            url='/shows',
            headers=[
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(body))),
            ],
            method='POST',
            body=body,
        )
        self.assertStatus(400)

        body = 'Invalid'
        self.getPage(
            url='/shows',
            headers=[
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(body))),
            ],
            method='POST',
            body=body,
        )
        self.assertStatus(400)
