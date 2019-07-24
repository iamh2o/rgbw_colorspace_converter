from typing import Dict, List
PixelMap = Dict[int, List[int]]


# This cell -> pixels mapping is created from an old version, but it should produce something.
def demo_triangle_mapping() -> PixelMap:
    return {
        0: [73, 72, 71, 70, 69, 68],
        1: [52, 51, 50, 49, 48, 47],
        2: [65, 64, 63, 62, 61, 60],
        3: [46, 45, 44, 43, 42, 41],
        4: [19, 18, 17, 16, 15, 14],
        5: [27, 28, 29, 30, 31, 32],
        6: [13, 12, 11, 10, 9, 8],
        7: [33, 34, 35, 36, 37, 38],
        8: [7, 6, 5, 4, 3, 2]
    }
