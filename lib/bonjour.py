import select
import sys
import pybonjour

"""
http://opensoundcontrol.org/topic/110
_osc._udp

linux may need lib:
libavahi-compat-libdnssd1
"""

def register_callback(sdRef, flags, errorCode, name, regtype, domain):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        print "Advertising Bonjour service '%s' %s (%s)" % (name, domain, regtype)
    else:
        print "error registering bonjour server!"
        print errorCode

def serve_forever(name, port, shutdownEvent, regtype = "_osc._udp"):

    sdRef = pybonjour.DNSServiceRegister(name = name,
                                         regtype = regtype,
                                         port = port,
                                         callBack = register_callback)

    try:
        try:
            while not shutdownEvent.is_set():
                ready = select.select([sdRef], [], [], 0.5) # timeout after 0.5 seconds
                if sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(sdRef)
        except KeyboardInterrupt:
            pass
    finally:
        print "Shutting down bonjour advertisement"
        sdRef.close()
