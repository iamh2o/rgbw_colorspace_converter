#!/usr/bin/env python
import sys
import optparse
import threading

from collections import defaultdict

from lib.OSC import *
from lib.OSC import _readString, _readFloat, _readInt

# define a message-handler function for the server to call.
def printing_handler(addr, tags, stuff, source):
    msg_string = "%s [%s] %s" % (addr, tags, str(stuff))
    sys.stdout.write("OSCServer Got: '%s' from %s\n" % (msg_string, getUrlStr(source)))

    # send a reply to the client.
    msg = OSCMessage("/printed")
    msg.append(msg_string)
    return msg

def server_test(_threading=False, _forking=False):
    # Now an OSCServer...
    print "\nInstantiating OSCServer:"

    listen_address=('0.0.0.0', 5700)

    if _threading:
        # s = ThreadingOSCServer(listen_address, c, return_port=listen_address[1])
        s = ThreadingOSCServer(listen_address)
    elif _forking:
        # s = ForkingOSCServer(listen_address, c, return_port=listen_address[1])
        s = ForkingOSCServer(listen_address)
    else:
        # s = OSCServer(listen_address, c, return_port=listen_address[1])
        s = OSCServer(listen_address)

    print s

    # Set Server to return errors as OSCMessages to "/error"
    s.setSrvErrorPrefix("/error")
    # Set Server to reply to server-info requests with OSCMessages to "/serverinfo"
    s.setSrvInfoPrefix("/serverinfo")

    # this registers a 'default' handler (for unmatched messages),
    # an /'error' handler, an '/info' handler.
    # And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
    s.addDefaultHandlers()

    s.addMsgHandler("/print", printing_handler)

    # if client & server are bound to 'localhost', server replies return to itself!
    s.addMsgHandler("/printed", s.msgPrinter_handler)
    s.addMsgHandler("/serverinfo", s.msgPrinter_handler)

    # setupServerHandlers(s)

    print "Registered Callback-functions:"
    for addr in s.getOSCAddressSpace():
        print addr

    print "\nStarting OSCServer. Use ctrl-C to quit."
    st = threading.Thread(target=s.serve_forever)
    st.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted!"
        s.close()
        # s.shutdown()

def create_server(listen_address, queue, debug=False):

    THROTTLE_TIME = 0.1 # seconds
    last_msg = defaultdict(float)

    def _handler(addr, tags, data, source):
        now = time.time()
        sincelast = now - last_msg[addr]

        if sincelast >= THROTTLE_TIME:
            if debug:
                print "%s [%s] %s" % (addr, tags, str(data))

            last_msg[addr] = now
            queue.put( (addr, data) )

    s = OSCServer(listen_address)

    # Set Server to return errors as OSCMessages to "/error"
    s.setSrvErrorPrefix("/error")
    # Set Server to reply to server-info requests with OSCMessages to "/serverinfo"
    s.setSrvInfoPrefix("/serverinfo")

    s.addMsgHandler('default', _handler)
    return s

if __name__=='__main__':
    server_test()
