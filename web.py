import cherrypy
import time

class SheepyWeb(object):
    def __init__(self, queue, runner, show_names):
        self.queue = queue
        self.runner = runner

        self.shows = show_names

    @cherrypy.expose
    def clear_show(self):
        self.queue.put("clear")
        return "<a href='.'/>Back</a>"

    @cherrypy.expose
    def change_run_time(self, run_time=None):
        try:
            print "RUNTIME XXXXX:::: %s" % run_time
            run_time = int(run_time)
            self.queue.put("inc runtime:%s"%run_time)
        except Exception as e:
            print "\n\nCRASH\n\n", e
            #probably a string... do nothing!
            pass
        return "<a href='.'/>Back</a>"

    @cherrypy.expose
    def index(self):
        # set a no-cache header so the show status is up to date
        cherrypy.response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate, max-age=0"
        cherrypy.response.headers['Expires'] = 0

        ret_html = "<h1></h1>"
        ret_html += "<p>" + self.runner.status() + "</p>"
        ret_html += "<b>Choose a show</b><ul>"

        for s in sorted(self.shows):
            ret_html += "<li><a href='run_show?show_name=%s' > %s</a>" % (s, s)
        ret_html += "<br><br><a href='clear_show' > CLEAR SHOW // STOP</a>"
        ret_html += """<br><br><h3>Set Show Cycle Time(seconds):<form name=change_run_time action='change_run_time'>
Seconds:<input type=text name=run_time value=60><input type=submit></form>
"""
        return(ret_html)

    @cherrypy.expose
    def run_show(self, show_name=None):
        if show_name:
            self.queue.put("run_show:"+show_name)
            print "setting show to:", show_name
        else:
            print "didn't get a show name"

        # XXX otherwise the runner.status() method
        # hasn't had time to update
        time.sleep(0.2)
        raise cherrypy.HTTPRedirect("/")

