import queue
import cherrypy
from jinja2 import escape
from cherrypy.test import helper

from web import TriangleWeb

command_queue = queue.LifoQueue()


class FakeRunner(object):
    @staticmethod
    def status():
        return "Everything's fine"


class WebTest(helper.CPWebCase):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(TriangleWeb(
            command_queue,
            FakeRunner(),
            ['ShowFoo', 'ShowBar']
        ), '/', {})

    def test_index_includes_shows(self):
        self.getPage('/')

        self.assertStatus(200)
        [self.assertInBody(show) for show in ['ShowFoo', 'ShowBar']]

    def test_index_includes_show_status(self):
        self.getPage('/')

        self.assertStatus(200)
        self.assertInBody(escape(FakeRunner.status()))

    def test_clear_show(self):
        assert command_queue.empty()
        self.getPage('/clear_show', method='POST')

        self.assertStatus(303)
        assert "clear" == command_queue.get()
        assert command_queue.empty()

    def test_change_run_time(self):
        assert command_queue.empty()
        self.getPage('/change_run_time', method='POST', body='run_time=30')

        self.assertStatus(303)
        assert "inc runtime:30" == command_queue.get()
        assert command_queue.empty()

    def test_run_show(self):
        assert command_queue.empty()
        self.getPage('/run_show', method='POST', body='show_name=ShowBar')

        self.assertStatus(303)
        assert "run_show:ShowBar" == command_queue.get()
        assert command_queue.empty()

        self.getPage('/run_show', method='POST', body='show_name=Invalid')
        self.assertStatus(400)
        assert command_queue.empty()
