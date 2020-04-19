import argparse
import faulthandler
import logging
import sys
import time
import queue
import threading
import cherrypy
import netifaces

from grid import Pyramid
from model import ModelBase
from model.sacn_model import sACN
from model.simulator import SimulatorModel
import osc_serve
import shows
from web import TriangleWeb
from show_runner import ShowRunner

# Prints stack trace on failure
faulthandler.enable()

logger = logging.getLogger("pyramidtriangles")


class TriangleServer:
    def __init__(self, model: ModelBase, pyramid: Pyramid, args):
        self.model = model
        self.pyramid = pyramid
        self.args = args

        self.queue = queue.LifoQueue()
        self.shutdown = threading.Event()  # Used to signal a shutdown event

        self.runner = None

        self.running = False
        self._create_services()

    def _create_services(self):
        """Create TRI services, trying to fail gracefully on missing dependencies"""

        # XXX can this also advertise the web interface?
        # XXX should it only advertise services that exist?

        # OSC listener
        t = threading.Thread(target=osc_serve.create_server, args=(self.shutdown, self.queue))
        t.start()

        self.runner = ShowRunner(
            pyramid=self.pyramid,
            command_queue=self.queue,
            shutdown=self.shutdown,
            max_showtime=self.args.max_time,
            fail_hard=self.args.fail_hard)

        if self.args.shows:
            print("setting show:", self.args.shows[0])
            self.runner.next_show(self.args.shows[0])

    def start(self):
        if self.running:
            logger.warning("start() called, but tri_grid is already running!")
            return

        try:
            self.runner.start()
            self.running = True
        except Exception:
            logger.exception("Exception starting ShowRunner")

    def stop(self):
        # safe to call multiple times
        self.shutdown.set()
        self.model.stop()

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

        # When control of the TriangleServer thread is passed to cherrypy, this registers a callback for shutdown
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
        model = sACN(bind)

    pyramid = Pyramid.build_single(model)
    if args.panels:
        dump_panels(pyramid)
        sys.exit(0)

    model.activate(pyramid.cells)

    # TriangleServer only needs model for model.stop()
    app = TriangleServer(model=model, pyramid=pyramid, args=args)

    try:
        app.start()  # start related service threads
        app.go_web()  # enter main blocking event loop
    except Exception:
        logger.exception("Unhandled exception running TRI!")
