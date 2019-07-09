dmx_start = 1
device = 1
print("{")
while dmx_start <= 512:
    print('"%s": [0, %s],' % (device, dmx_start))
    dmx_start = dmx_start+4
    device = device+1

dmx_start = 1

#Panel ID is a key to an array of universe#, DMXstartAddress, Annotation(only used for sheep)
while dmx_start <= 512:
    print('"%s": [1, %s, 0],' % (device, dmx_start))
    dmx_start = dmx_start+4
    device = device+1
print("}")
