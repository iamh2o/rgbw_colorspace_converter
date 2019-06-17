import os
import sys
import json


dmx_start = 1
device = 1
print "{"
while dmx_start <= 512:
    print '"%s": %s,' % (device, dmx_start)
    dmx_start = dmx_start+4
    device = device+1
print "}"
