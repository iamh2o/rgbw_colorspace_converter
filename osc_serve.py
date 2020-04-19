from collections import defaultdict
import logging
from queue import Queue
from threading import Event
import time

from osc4py3 import as_allthreads as osc
from osc4py3 import oscbuildparse
from osc4py3 import oscmethod

THROTTLE_TIME = 0.1  # seconds

logger = logging.getLogger("pyramidtriangles")


def server_test():
    logger.info("Instantiating OSCServer:")

    osc.osc_startup()
    osc.osc_udp_server('0.0.0.0', 5700, "main")

    def printing_handler(addr, tags, stuff, source):
        msg_string = "%s [%s] %s" % (addr, tags, str(stuff))
        logger.info("OSCServer Got: '%s' from %s", msg_string, source)

        # send a reply to the client.
        msg = oscbuildparse.OSCMessage("/printed", None, msg_string)
        osc.osc_send(msg, "main")
        osc.osc_process()

    osc.osc_method("/print", printing_handler, argscheme=oscmethod.OSCARG_ADDRESS + oscmethod.OSCARG_DATAUNPACK)

    logger.info("Starting OSC server. Use ctrl-C to quit.")

    try:
        while True:
            osc.osc_process()
    except KeyboardInterrupt:
        logger.info("Closing OSC server")
        osc.osc_terminate()


def create_server(shutdown: Event, queue: Queue, host: str = '0.0.0.0', port: int = 5700):
    """Creates an OSC server to listen and place messages on queue. Blocks until shutdown event signaled."""
    last_msg = defaultdict(float)

    def handler(addr, tags, data, source):
        now = time.time()
        sincelast = now - last_msg[addr]

        if sincelast >= THROTTLE_TIME:
            logger.debug(f'OSC message received: {addr} [{tags}] {data}')
            last_msg[addr] = now
            queue.put((addr, data))

    logger.info(f'Starting OSC Listener on {host}:{port}')
    osc.osc_startup()
    osc.osc_udp_server(host, port, "main")
    osc.osc_method("/*", handler, argscheme=oscmethod.OSCARG_ADDRESS + oscmethod.OSCARG_DATAUNPACK)
    # osc.osc_process() isn't necessary when using as_allthreads module

    # Blocks execution until shutdown is signaled, then cleans up
    shutdown.wait()
    osc.osc_terminate()


if __name__ == '__main__':
    server_test()
