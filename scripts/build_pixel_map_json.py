import os
import sys


num_ux = int(sys.argv[1])

pixel_num = 1
print("{")
for ux in range(1, num_ux+1):
    dmx_start = 1
    if ux in (3,6,9,12):
        while dmx_start < 176:
            print('"{0}": [{1}, {2}],'.format(pixel_num,ux,dmx_start))
            pixel_num += 1
            dmx_start += 4
    else:
        while dmx_start < 512:
            print('"{0}": [{1}, {2}],'.format(pixel_num,ux,dmx_start))
            pixel_num += 1
            dmx_start += 4

print("}")
