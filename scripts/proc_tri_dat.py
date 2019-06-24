import os
import sys
import numpy as np

fh = open(sys.argv[1])

arr = []
ctr = 0
for i in fh:
    sl = i.strip().split(',')
    
    if ctr == 0:
        pass
    else:

        a2 = [sl[1], sl[2],sl[3],sl[4],sl[5],sl[6]]
        arr.append(a2)

        

    ctr += 1
a = np.array(arr)


z = a[np.lexsort(np.transpose(a)[::-2])]

ds = {}

curr_row = 0
cells_added = 0
total_cells_added_this_row = 0
total_cells_next_row = 1
for i in z:
        


    if curr_row == 0:
        ds[curr_row] = [i]
    else:
        ds[curr_row].append(i)

    total_cells_added_this_row += 1
    if total_cells_added_this_row == total_cells_next_row:
        curr_row += 1
        total_cells_next_row = total_cells_added_this_row + 2
        total_cells_added_this_row = 0
        ds[curr_row] = []
        

        

c=1
for q in ds:
#    for ii in sorted(ds[q]):
#    print ds[q]
    for iii in np.lexsort(np.transpose(ds[q])[::-1]):
#        print iii
        ii =ds[q][iii]
        print "triangle({0},{1},{2},{3},{4},{5});".format(ii[0],ii[1],ii[2],ii[3],ii[4],ii[5])
        #print "triangle,{0},{1},{2},{3},{4},{5},{6}".format(ii[0],ii[1],ii[2],ii[3],ii[4],ii[5],c)

        c  +=1 
