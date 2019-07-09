from collections import defaultdict
import logging
from osc4py3 import as_allthreads as osc
from osc4py3 import oscbuildparse
from osc4py3 import oscmethod
import time

THROTTLE_TIME = 0.1  # seconds


def server_test():
    logging.info("Instantiating OSCServer:")

    osc.osc_startup()
    osc.osc_udp_server('0.0.0.0', 5700, "main")

    def printing_handler(addr, tags, stuff, source):
        msg_string = "%s [%s] %s" % (addr, tags, str(stuff))
        logging.info("OSCServer Got: '%s' from %s", msg_string, source)

        # send a reply to the client.
        msg = oscbuildparse.OSCMessage("/printed", None, msg_string)
        osc.osc_send(msg, "main")
        osc.osc_process()

    osc.osc_method("/print", printing_handler, argscheme=oscmethod.OSCARG_ADDRESS + oscmethod.OSCARG_DATAUNPACK)

    logging.info("Starting OSC server. Use ctrl-C to quit.")

    try:
        while True:
            osc.osc_process()
    except KeyboardInterrupt:
        logging.info("Closing OSC server")
        osc.osc_terminate()


def create_server(listen_address, queue):
    last_msg = defaultdict(float)

    def handler(addr, tags, data, source):
        now = time.time()
        sincelast = now - last_msg[addr]

        if sincelast >= THROTTLE_TIME:
            logging.debug("%s [%s] %s", addr, tags, str(data))
            last_msg[addr] = now
            queue.put((addr, data))

    osc.osc_startup()
    osc.osc_udp_server(*listen_address, "main")
    osc.osc_method("/*", handler, argscheme=oscmethod.OSCARG_ADDRESS + oscmethod.OSCARG_DATAUNPACK)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

    server_test()
