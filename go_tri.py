import argparse
import cherrypy
import logging
import netifaces
import queue
import sys
import threading

from pyramidtriangles import osc_serve
from pyramidtriangles.show_runner import ShowRunner
from pyramidtriangles.playlist import Playlist
from pyramidtriangles.grid import Pyramid
from pyramidtriangles.model import Model
from pyramidtriangles.model.sacn_model import sACN
from pyramidtriangles.model.simulator import SimulatorModel
import pyramidtriangles.shows as shows
from pyramidtriangles.web import Web

logger = logging.getLogger(__name__)


# Threading Model
#
# The main thread parses commandline arguments and creates a TriangleServer. A threading.Event is created to signal a
# shutdown to any other threads, allowing them to shutdown gracefully.
#
# TriangleServer.start() starts threads for the ShowRunner and the OSC listener.
# Then TriangleServer may startup with a web server or run headless:
# 1. TriangleServer.go_web() launches and joins cherrypy, which is multi-threaded itself.
# 2. TriangleServer.go_headless() joins to the shutdown event and has nothing more to do.


class TriangleServer:
    def __init__(self, model: Model, pyramid: Pyramid, args):
        self.model = model
        self.pyramid = pyramid

        # Commands for the ShowRunner to process
        self.command_queue = queue.Queue()
        # Sequence of status updates from ShowRunner to Web
        self.status_queue = queue.Queue()
        # Event to synchronize shutting down
        self.shutdown = threading.Event()
        # Set up the database for playlist management
        Playlist.setup_database()

        self.runner = ShowRunner(
            pyramid=self.pyramid,
            command_queue=self.command_queue,
            status_queue=self.status_queue,
            shutdown=self.shutdown,
            max_showtime=args.max_time,
            fail_hard=args.fail_hard)

        self.osc_listener = threading.Thread(target=osc_serve.create_server, args=(self.shutdown, self.command_queue))

        self.running = False

        if args.shows:
            logger.info("setting show: %s", args.shows[0])
            self.runner.next_show(args.shows[0])

    def start(self):
        if self.runner.is_alive():
            logger.warning("start() called, but tri_grid is already running!")
            return
        self.osc_listener.start()
        self.runner.start()
        self.running = True

    def stop(self):
        # safe to call multiple times
        self.shutdown.set()
        self.model.stop()

    def go_headless(self):
        """Run without the web interface"""
        logger.info("Running without web interface")
        try:
            self.shutdown.wait()
        except KeyboardInterrupt:
            logger.info("Exiting on keyboard interrupt")

        self.stop()

    def go_web(self):
        """Run with the web interface"""
        show_names = ', '.join([name for (name, cls) in shows.load_shows()])
        logger.info('loaded shows: %s', show_names)

        # When cherrypy publishes to 'stop' bus (e.g. Autoreloader) trigger stop for other threads.
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
        logger.info("Running with web interface at http://localhost:9990")

        web = Web(self.command_queue, self.status_queue)
        # this method blocks until KeyboardInterrupt
        web.start(config)


def dump_panels(pyramid: Pyramid):
    for i, face in enumerate(pyramid.faces):
        print(f'Face {i + 1}:')

        for j, panel in enumerate(sorted(face.panels, key=lambda panel: panel.start)):
            print(f'  Panel {j + 1}:')
            print(f'    origin: {panel.geom.origin}')
            print(f'    start:  {panel.start}')

        print()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s|%(name)s|\t%(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Triangle Light Control')
    parser.add_argument('--max-time', type=float, default=float(60),
                        help='Maximum number of seconds a show will run (default 60)')

    parser.add_argument('--bind', help='Local address to use for sACN')
    parser.add_argument('--simulator', dest='simulator', action='store_true')

    parser.add_argument('--list', action='store_true', help='List available shows')
    parser.add_argument('--panels', action='store_true', help='Show face and panel attributes')
    parser.add_argument('shows', metavar='show_name', type=str, nargs='*', help='name of show (or shows) to run')
    parser.add_argument('--fail-hard', action='store_true',
                        help="For production runs, when shows fail, the show runner moves to the next show")

    args = parser.parse_args()

    if args.list:
        logger.info("Available shows: %s", ', '.join([name for (name, cls) in shows.load_shows()]))
        sys.exit(0)

    if args.simulator:
        sim_host = "localhost"
        sim_port = 4444
        logger.info('Using TriSimulator at %s:%d', sim_host, sim_port)

        model = SimulatorModel(sim_host, port=sim_port)
    else:
        bind = args.bind
        if not bind:
            gateways = netifaces.gateways()[netifaces.AF_INET]

            for _, interface, _ in gateways:
                for a in netifaces.ifaddresses(interface).get(netifaces.AF_INET, []):
                    if a['addr'].startswith('192.168.0'):
                        logger.info('Auto-detected Pyramid local IP: %s', a['addr'])
                        bind = a['addr']
                        break
                if bind:
                    break

            if not bind:
                parser.error('Failed to auto-detect local IP. Are you on Pyramid Scheme wifi or ethernet?')

        model = sACN(bind)

    pyramid = Pyramid.build_single(model)
    if args.panels:
        dump_panels(pyramid)
        sys.exit(0)

    model.activate(pyramid.cells)

    app = TriangleServer(model=model, pyramid=pyramid, args=args)

    try:
        app.start()  # start related service threads
        app.go_web()  # enter main blocking event loop
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.exception("Unhandled exception from cherrypy thread")
