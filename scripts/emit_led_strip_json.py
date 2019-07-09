dmx_start = 1
device = 1
print('{"1":{')
while dmx_start <= 512:
    print('"%s": %s,' % (device, dmx_start))
    dmx_start = dmx_start+4
    device = device+1
print("}}")
