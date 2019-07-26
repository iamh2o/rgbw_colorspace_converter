from typing import Dict, List
PixelMap = Dict[int, List[int]]


# This cell -> pixels mapping is created from an old version, but it should produce something.
def demo_triangle_mapping() -> PixelMap:
    return {
        #Wiring coming in from the bottom left, this is the order of cells following the pixels
        1: [  2, 3, 4, 5, 6, 7, 8, 9],  
        3: [ 10, 11, 12, 13, 14, 15, 16, 17],
        2: [ 34, 33, 32, 31, 30, 29,28, 27 ],
        0: [ 35, 36, 37, 38, 39, 40, 41, 42]  # the last cell should the the top most cell of the triangle grid
        }

        
