import os
import sys
import psutil
import argparse
import faulthandler
import logging
import sys
import time
import queue
import threading

import cherrypy

from cherrypy.process.plugins import SimplePlugin

from grid import Pyramid
from model.sacn_model import sACN
from model.simulator import SimulatorModel

import netifaces
import osc_serve
import shows
import util
from web import TriangleWeb

# Prints stack trace on failure
faulthandler.enable()

logger = logging.getLogger("pyramidtriangles")


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
hi_interp = util.make_interpolater(0.5, 1.0, 1.0, 0.5)


class ShowRunner(threading.Thread):

    def __init__(self, pyramid, queue, max_showtime=240, fail_hard=True,brightness_scale=1.0):
        super(ShowRunner, self).__init__(name="ShowRunner")
        self.pyramid = pyramid
        self.queue = queue

        self.fail_hard = fail_hard
        self.running = True
        self.max_show_time = max_showtime
        self.show_runtime = 0
        self.brightness_scale = brightness_scale

        # map of names -> show ctors
        self.shows = dict(shows.load_shows())
        self.randseq = shows.random_shows()
        self.show_params = False

        # current show object & frame generator
        self.show = None
        self.framegen = None
        self.prev_show = None

        # current show parameters

        # show speed multiplier - ranges from 0.5 to 2.0
        # 1.0 is normal speed
        # lower numbers mean faster speeds, higher is slower
        self.speed_x = 1.0

    def restart_program(self,reset_show=None, brightness_scale=1.0):
        """Restarts the current program, with orig arguments passed back.  reset_show=True will re-start running from a known good show.BUGGY as it assumed the show is the last argument always. """
        if reset_show is None:
            reset_show = self.show.name

        try:
            p = psutil.Process(os.getpid())
            for handler in p.get_open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            logging.error(e)
            
        python = sys.executable

        cmd = list(sys.argv)    
        cmd[-1] = reset_show
        try: 
            x = cmd.index('--brightness-scale') 
            cmd[x+1] = str(brightness_scale)
        except Exception as e: 
            cmd.insert(-1,'--brightness-scale') 
            cmd.insert(-1,str(brightness_scale)) 
        os.execl(python, python, *cmd)

    def status(self):
        if self.running:
            return "Running %s (%d seconds left)" % (self.show.name, self.max_show_time - self.show_runtime)
        else:
            return "Stopped"

    def check_queue(self):
        msgs = []
        try:
            while True:
                m = self.queue.get_nowait()
                if m:
                    msgs.append(m)

        except queue.Empty:
            pass

        if msgs:
            for m in msgs:
                self.process_command(m)

    def process_command(self, msg):
        if isinstance(msg, str):
            if msg == "shutdown":
                self.running = False
                logger.info("ShowRunner shutting down")
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
            logger.debug(f'OSC: {msg}')

            (addr, val) = msg
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
                    print("setting speed_x to:", self.speed_x)

                pass
            elif ns == '2':
                # show command
                if self.show_params:
                    self.show.set_param(cmd, val)

        else:
            print("ignoring unknown msg:", str(msg))

    def clear(self):
        """Clears all panels."""
        self.pyramid.clear()

    def next_show(self, name=None):
        show = None
        if name:
            if name in self.shows:
                show = self.shows[name]
            else:
                logger.warning(f'unknown show: {name}')

        if not show:
            logger.info("choosing random show")
            (name, show) = next(self.randseq)

        self.clear()
        self.prev_show = self.show

        self.show = show(self.pyramid)
        print(f'next show: {name}')
        self.framegen = self.show.next_frame()
        self.show_params = hasattr(self.show, 'set_param')
        if self.show_params:
            print("Show can accept OSC params!")
        self.show_runtime = 0

    def get_next_frame(self):
        "return a delay or None"
        try:
            return next(self.framegen)
        except StopIteration:
            return None

    def run(self):
        if not (self.show and self.framegen):
            print("Next Next Next")
            self.next_show()

        while self.running:
            try:
                self.check_queue()

                d = self.get_next_frame()
                self.pyramid.go()
                if d:
                    real_d = d * self.speed_x
                    time.sleep(real_d)
                    self.show_runtime += real_d
                    if self.show_runtime > self.max_show_time:
                        print("max show time elapsed, changing shows")
                        self.next_show()
                else:
                    print("show is out of frames, waiting...")
                    time.sleep(2)
                    self.next_show()

            except Exception:
                logger.exception("unexpected exception in show loop!")
                if self.fail_hard:
                    raise
                else:
                    self.next_show()


def osc_listener(q, port=5700):
    """Create the OSC Listener thread"""

    listen_address = ('0.0.0.0', port)
    logger.info(f'Starting OSC Listener on {listen_address}')
    osc_serve.create_server(listen_address, q)


 
class TriangleServer(object):
    def __init__(self, pyramid, args):
        self.args = args

        self.brightness_scale = args.brightness_scale
        self.pyramid = pyramid

        self.queue = queue.LifoQueue()

        self.runner = None

        self.running = False
        self._create_services()

    def _create_services(self):
        """Create TRI services, trying to fail gracefully on missing dependencies"""

        # XXX can this also advertise the web interface?
        # XXX should it only advertise services that exist?

        # OSC listener
        try:
            osc_listener(self.queue)
        except Exception:
            logger.warning("Can't create OSC listener", exc_info=True)

        # Show runner
        self.runner = ShowRunner(

            self.pyramid, self.queue, args.max_time, fail_hard=args.fail_hard, brightness_scale=self.brightness_scale)
        if args.shows:
            print("setting show:", args.shows[0])
            self.runner.next_show(args.shows[0])

    def start(self):
        if self.running:
            logger.warning("start() called, but tri_grid is already running!")
            return

        try:
            self.runner.start()
            self.running = True
        except Exception:
            logger.exception("Exception starting tri_grid!!")

    def stop(self):
        if self.running:  # should be safe to call multiple times
            try:
                # OSC listener is a daemon thread so it will clean itself up

                # ShowRunner is shut down via the message queue
                self.queue.put("shutdown")

                self.running = False
            except Exception:
                logger.exception("Exception stopping tri_grid!!")

        self.runner.restart_program(str(self.runner.show.name)) 
 
        #Fucked up threading handling in SACN preventing chrerrypy from restarting cleanly with any code change (a really REALLY nice feature when writing shows).  I gave up after 2 hrs of debugging mystery threads and applied the sleedge hammer above.  Love- Major
#      time.sleep(2)  
#      self.runner.grid._model.__del__() 
#      del(self.runner.grid._model) 
#      self.runner.grid._model.sender._output_thread._socket.close() 
#      self.runner.grid._model.sender._output_thread.join()   
#      self.runner.grid._model.__del__()   


    

    def go_headless(self):
        """Run without the web interface"""
        logger.info("Running without web interface")
        try:
            while True:
                time.sleep(999)  # control-c breaks out of time.sleep
        except KeyboardInterrupt:
            print("Exiting on keyboard interrupt")

        self.stop()

    def go_web(self):
        """Run with the web interface"""
        logger.info("Running with web interface")

        show_names = [name for (name, cls) in shows.load_shows()]
        print(f'shows: {show_names}')

#        webplugin(cherrypy.engine).subscribe()

        cherrypy.engine.subscribe('stop', self.stop) 
        config = {
            'global': {
                'server.socket_host': '0.0.0.0',
                'server.socket_port': 9990,
                # 'engine.timeout_monitor.on' : True,
                # 'engine.timeout_monitor.frequency' : 240,
                # 'response.timeout' : 60*15
            }
        }

        # this method blocks until KeyboardInterrupt
        cherrypy.quickstart(TriangleWeb(self.queue, self.runner, show_names),
                            '/',
                            config=config)



def dump_panels(pyramid: Pyramid):
    for i, face in enumerate(pyramid.faces):
        print(f'Face {i + 1}:')

        for j, panel in enumerate(sorted(face.panels, key=lambda panel: panel.start)):
            print(f'  Panel {j + 1}:')
            print(f'    origin: {panel.geom.origin}')
            print(f'    start:  {panel.start}')

        print()


if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(console)

    parser = argparse.ArgumentParser(description='Triangle Light Control')

    parser.add_argument('--max-time', type=float, default=float(60),
                        help='Maximum number of seconds a show will run (default 60)')

    parser.add_argument('--bind', help='Local address to use for sACN')
    parser.add_argument('--simulator', dest='simulator', action='store_true')

    parser.add_argument('--list', action='store_true',
                        help='List available shows')
    parser.add_argument('--panels', action='store_true',
                        help='Show face and panel attributes')
    parser.add_argument('shows', metavar='show_name', type=str, nargs='*',
                        help='name of show (or shows) to run')
    parser.add_argument('--fail-hard', type=bool, default=True,
                        help="For production runs, when shows fail, the show runner moves to the next show")
    parser.add_argument('--brightness-scale',type=float,default=1.0, 
                        help="Adjust the global brightness of the shows from 0.0-1.0")

    args = parser.parse_args()

    if args.list:
        logger.info("Available shows: %s", ', '.join(
            [name for (name, cls) in shows.load_shows()]))
        sys.exit(0)
 
    if args.simulator:
        sim_host = "localhost"
        sim_port = 4444
        logger.info(f'Using TriSimulator at {sim_host}:{sim_port}')

        model = SimulatorModel(sim_host, port=sim_port)
    else:
        bind = args.bind
        if not bind:
            gateways = netifaces.gateways()[netifaces.AF_INET]

            for _, interface, _ in gateways:
                for a in netifaces.ifaddresses(interface).get(netifaces.AF_INET, []):
                    if a['addr'].startswith('192.168.0'):
                        logger.info(
                            f"Auto-detected Pyramid local IP: {a['addr']}")
                        bind = a['addr']
                        break
                if bind:
                    break

            if not bind:
                parser.error(
                    'Failed to auto-detect local IP. Are you on Pyramid Scheme wifi or ethernet?')

        logger.info("Starting sACN")

        model = sACN(bind, args.rows, args.brightness_scale))

    pyramid = Pyramid.build(model)
    if args.panels:
        dump_panels(pyramid)
        sys.exit(0)

    model.activate(pyramid.cells)

    app = TriangleServer(pyramid, args)

    try:
        app.start()  # start related service threads
        app.go_web()  # enter main blocking event loop
    except Exception:
        logger.exception("Unhandled exception running TRI!")
    finally:
        app.stop
