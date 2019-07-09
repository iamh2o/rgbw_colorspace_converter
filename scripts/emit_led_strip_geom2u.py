dmx_start = 1
device = 1
top_neighbor = 0
print("\t".join(["Device", "TopNeighbor", "BottomNeighbor"]))
while device <= 128:
    print("%s\t%s\t%s" %(device, top_neighbor, device+1))
    top_neighbor += 1
    device += 1
