import os
import sys

curr_cell = 1
end_led = 1059
n = end_led

ds = {1:1,
      2:3,
      3:5,
      4:7,
      5:9,
      6:11,
      7:13,
      8:15,
      9:17,
      10:19,
      11:21
      }
u = end_led -7
d = end_led

for i in range (1,12):
    n_cells = ds[i]

    is_up = True
    tot_u_add = 0
    tot_d_add = 0
    for cell in range (1, n_cells+1):
        if is_up:
            print('{0}: [{1},{2},{3},{4},{5},{6},{7},{8}],'.format(curr_cell, u, u+1, u+2 , u+3, u+4, u+5, u+6, u+7))
            is_up = False
            u += 8
            tot_u_add += 8
        else:
            print('{0}: [{1},{2},{3},{4},{5},{6},{7},{8}],'.format(curr_cell, d ,d+1, d+2, d+3, d+4,d+5,d+6, d+7))
            d += 8
            tot_d_add +=8
            is_up = True

        curr_cell += 1

    md = 0
    if i == 1:
        md = (i*8)+tot_d_add
    else:
        md = 9+((n_cells)*8)+tot_d_add
    d -= md

    mu = 9+((n_cells+2)*8)+tot_u_add
    u -= mu
