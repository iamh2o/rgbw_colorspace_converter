import os
import sys
import json



ds = None
with open(sys.argv[1], 'r') as json_file:
    ds = json.load(json_file)



ctr = 1
print "{"
for i in ds:
    print '"{0}": [0, {1}, {2}],'.format(i, ds[i], ctr)
    ctr += 1
print "}"


