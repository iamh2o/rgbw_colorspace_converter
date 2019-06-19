#!/usr/bin/env python2.7
import sys
import time
import traceback
import Queue
import threading
import signal

import led_strip
import led_shows as shows
import util

# fail gracefully if cherrypy isn't available
_use_cherrypy = False
try:
    import cherrypy
    _use_cherrypy = True
except ImportError:
    print "WARNING: CherryPy not found; web interface disabled"

def _stacktraces(signum, frame):
    txt = []
    for threadId, stack in sys._current_frames().items():
        txt.append("\n# ThreadID: %s" % threadId)
        for filename, lineno, name, line in traceback.extract_stack(stack):
            txt.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                txt.append("  %s" % (line.strip()))

    print "\n".join(txt)

signal.signal(signal.SIGQUIT, _stacktraces)

def speed_interpolation(val):
    """
    Interpolation function to map OSC input into ShowRunner speed_x

    Input values range from 0.0 to 1.0
    input 0.5 => 1.0
    input < 0.5 ranges from 2.0 to 1.0
    input > 0.5 ranges from 1.0 to 0.5
    """
    if val == 0.5:
        return 1.0
    elif val < 0.5:
        return low_interp(val)
    else:
        return hi_interp(val)

low_interp = util.make_interpolater(0.0, 0.5, 2.0, 1.0)
hi_interp  = util.make_interpolater(0.5, 1.0, 1.0, 0.5)

class ShowRunner(threading.Thread):
    def __init__(self, model, queue, max_showtime=240):
        super(ShowRunner, self).__init__(name="ShowRunner")
        self.model = model
        self.queue = queue

        self.running = True
        self.max_show_time = max_showtime
        self.show_runtime = 0

        # map of names -> show ctors
        self.shows = dict(shows.load_shows())
        self.randseq = shows.random_shows()

        # current show object & frame generator
        self.show = None
        self.framegen = None

        # current show parameters

        # show speed multiplier - ranges from 0.5 to 2.0
        # 1.0 is normal speed
        # lower numbers mean faster speeds, higher is slower
        self.speed_x = 1.0

    def status(self):
        if self.running:
            return "Running: %s (%d seconds left)" % (self.show.name, self.max_show_time - self.show_runtime)
        else:
            return "Stopped"

    def check_queue(self):
        msgs = []
        try:
            while True:
                m = self.queue.get_nowait()
                if m:
                    msgs.append(m)

        except Queue.Empty:
            pass

        if msgs:
            for m in msgs:
                self.process_command(m)

    def process_command(self, msg):
        if isinstance(msg,basestring):
            if msg == "shutdown":
                self.running = False
                print "ShowRunner shutting down"
            elif msg == "clear":
                self.clear()
                time.sleep(2)
            elif msg.startswith("run_show:"):
                self.running = True
                show_name = msg[9:]
                self.next_show(show_name)
            elif msg.startswith("inc runtime"):
                self.max_show_time = int(msg.split(':')[1])

        elif isinstance(msg, tuple):
            # osc message
            # ('/1/command', [value])
            print "OSC:", msg

            (addr,val) = msg
            addr = addr.split('/z')[0]
            val = val[0]
            assert addr[0] == '/'
            (ns, cmd) = addr[1:].split('/')
            if ns == '1':
                # control command
                if cmd == 'next':
                    self.next_show()
                elif cmd == 'previous':
                    if self.prev_show:
                        self.next_show(self.prev_show.name)
                elif cmd == 'speed':
                    self.speed_x = speed_interpolation(val)
                    print "setting speed_x to:", self.speed_x

                pass
            elif ns == '2':
                # show command
                if self.show_params:
                    self.show.set_param(cmd, val)

        else:
            print "ignoring unknown msg:", str(msg)

    def clear(self):
#        print "WE ARE GOING HERE"
        self.model.clear()


    def next_show(self, name=None):
        s = None
        if name:
            if name in self.shows:
                s = self.shows[name]
            else:
                print "unknown show:", name

        if not s:
            print "choosing random show"
            s = self.randseq.next()

        self.clear()
        self.prev_show = self.show

        self.show = s(self.model)
        print "next show:" + self.show.name
        self.framegen = self.show.next_frame()
        self.show_params = hasattr(self.show, 'set_param')
        if self.show_params:
            print "Show can accept OSC params!"
        self.show_runtime = 0

    def get_next_frame(self):
        "return a delay or None"
#        print "z"
        try:
#            print "zz"
            return self.framegen.next()
        except StopIteration:
#            print "zzz"
            return None

    def run(self):
        if not (self.show and self.framegen):
            self.next_show()
        print "1"
        while self.running:
            try:
                self.check_queue()

                d = self.get_next_frame()
#                print "2"
                self.model.go()
#                print "3"
                if d:
#                    print "4"
                    real_d = d * self.speed_x
                    time.sleep(real_d)
#                    print "5"
                    self.show_runtime += real_d
                    if self.show_runtime > self.max_show_time:
                        print "max show time elapsed, changing shows"
                        self.next_show()
                else:
                    print "show is out of frames, waiting..."
                    time.sleep(2)
                    self.next_show()

            except Exception:
                print "unexpected exception in show loop!"
                traceback.print_exc()
                self.next_show()
#        print "X"

def osc_listener(q, port=5700):
    "Create the OSC Listener thread"
    import osc_serve

    listen_address=('0.0.0.0', port)
    print "Starting OSC Listener on %s:%d" % listen_address
    osc = osc_serve.create_server(listen_address, q)
    st = threading.Thread(name="OSC Listener", target=osc.serve_forever)
    st.daemon = True
    return st

def bonjour_server(name="LedStrip", port=5700):
    "Create the bonjour server, returns (thread, shutdownEvent)"
    from lib import bonjour
    shutdownEvent = threading.Event()
    st = threading.Thread(name="Bonjour broadcaster", target=bonjour.serve_forever, args=(name, port, shutdownEvent))
    return (st, shutdownEvent)

class LEDServer(object):
    def __init__(self, led_model, args):
        self.args = args
        self.led_model = led_model

        self.queue = Queue.LifoQueue()

        self.runner = None

        self.osc_thread = None

        self.bonjour_thread = None
        self.bonjour_exit_flag = None

        self.running = False
        self._create_services()

    def _create_services(self):
        "Create LED services, trying to fail gracefully on missing dependencies"
        # Bonjour advertisement
        # XXX can this also advertise the web interface?
        # XXX should it only advertise services that exist?
        try:
            (t, flag) = bonjour_server(name="LEDStrip@" + util.get_hostname("unknown"))
            self.bonjour_thread = t
            self.bonjour_exit_flag = flag
        except Exception, e:
            print "WARNING: Can't create bonjour service"

        # OSC listener
        try:
            self.osc_thread = osc_listener(self.queue)
        except Exception, e:
            print "WARNING: Can't create OSC listener"

        # Show runner
        self.runner = ShowRunner(self.led_model, self.queue, args.max_time)
        if args.shows:
            print "setting show:", args.shows[0]
            self.runner.next_show(args.shows[0])

    def start(self):
        if self.running:
            print "start() called, but led_strip is already running!"
            return

        try:
            if self.bonjour_thread:
                self.bonjour_thread.start()

            if self.osc_thread:
                self.osc_thread.start()

            self.runner.start()

            self.running = True
        except Exception, e:
            print "Exception starting led_strip!"
            traceback.print_exc()

    def stop(self):
        if self.running: # should be safe to call multiple times
            try:
                if self.bonjour_thread:
                    print "Setting bonjour exit flag"
                    self.bonjour_exit_flag.set()

                # OSC listener is a daemon thread so it will clean itself up

                # ShowRunner is shut down via the message queue
                self.queue.put("shutdown")

                self.running = False
            except Exception, e:
                print "Exception stopping led_strip!"
                traceback.print_exc()

    def go_headless(self):
        "Run without the web interface"
        print "Running without web interface"
        try:
            while True:
                time.sleep(999) # control-c breaks out of time.sleep
        except KeyboardInterrupt:
            print "Exiting on keyboard interrupt"

        self.stop()

    def go_web(self):
        "Run with the web interface"
        import cherrypy
        from web import SheepyWeb

        # XXX clean up who manages the canonical show list
        show_names = dict(shows.load_shows()).keys()
        print show_names

        cherrypy.engine.subscribe('stop', self.stop)

        port = 9990
        config = {
            'global': {
                'server.socket_host' : '0.0.0.0',
                'server.socket_port' : port,
                # 'engine.timeout_monitor.on' : True,
                # 'engine.timeout_monitor.frequency' : 240,
                # 'response.timeout' : 60*15
            }
        }

        # this method blocks until KeyboardInterrupt
        cherrypy.quickstart(SheepyWeb(self.queue, self.runner, show_names),
                            '/',
                            config=config)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Baaahs Light Control')

    parser.add_argument('--max-time', type=float, default=float(60),
                        help='Maximum number of seconds a show will run (default 60)')

    parser.add_argument('--simulator',dest='simulator',action='store_true')

    parser.add_argument('--list', action='store_true', help='List available shows')
    parser.add_argument('shows', metavar='show_name', type=str, nargs='*',
                        help='name of show (or shows) to run')

    args = parser.parse_args()

    if args.list:
        print "Available shows:"
        print ', '.join([s[0] for s in shows.load_shows()])
        sys.exit(0)

    if args.simulator:
        sim_host = "localhost"
        sim_port = 4444
        print "Using LEDSimulator at %s:%d" % (sim_host, sim_port)
        raise Exception("LED Simulator not Supported")
        from model.simulator import SimulatorModel
        model = SimulatorModel(sim_host, port=sim_port)
        led_strip = led_strip.make_led(model)
    else:
        universe = 1
        print "Using OLA model universe=%d" % universe
        from model.ola_model import OLAModel
        model = OLAModel(800, universe=universe,model_json="./data/led_strip.json")
        led_strip_model = led_strip.make_led(model, './data/led_strip.geom')

    app = LEDServer(led_strip_model, args)
    try:
        app.start() # start related service threads

        # enter main blocking event loop
        if _use_cherrypy:
            app.go_web()
        else:
            app.go_headless()

    except Exception, e:
        print "Unhandled exception running LED!"
        traceback.print_exc()
    finally:
        app.stop()
