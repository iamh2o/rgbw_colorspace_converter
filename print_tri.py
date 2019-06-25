import os
import sys




p1 = [400.00,100.0]
p2 = [325.0,225.0]
p3 = [475.0,225.0]

i = 0
def calc_next_row(p1,p2,p3, i):
    p_1 = []
    p_2 = []
    p_3 = []

    btm_dist = p2[0]-p1[0]
    height = p3[1]-p1[1]


    p_1 = [p1[0]+(btm_dist/2.0), p1[1]+height]
    p_2 = [p_1[0]-btm_dist, p1[1]+height]
    p_3 = p2
    print "triangle({0},{1},{2},{3},{4},{5});".format(p_1[0],p_1[1], p_2[0],p_2[1], p3[0],p3[1])

    i += 1
    if i > 5:
        raise


    calc_next_row(p_1,p_2,p_3, i)
        
print
print "triangle({0},{1},{2},{3},{4},{5});".format(p1[0],p1[1], p2[0],p2[1], p3[0],p3[1])

calc_next_row(p1,p2,p3,0)
