import sys
import json

with open(sys.argv[1]) as json_file:
    data = json.load(json_file)

n=1
for i in sorted(data):
    print('"%s": %s,' % (i, n))
    n = n+4

