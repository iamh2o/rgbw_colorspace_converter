from itertools import cycle
import pprint
import time

from pyramidtriangles.model.sacn_model import sACN, demo_triangle_mapping
from pyramidtriangles import grid
from pyramidtriangles.grid import CELLS

model = sACN(model_json="./data/pixel_map.json",
             pixelmap=demo_triangle_mapping())
tri = grid.make_triangle(model, 2)

tri.go()

colors = cycle(range(3))
for cell in sorted(CELLS):
    print(cell)
    co = next(colors)

    for addr in CELLS[cell]:
        model.leds[addr.universe][addr.offset + co] = 128
        model.leds[addr.universe][addr.offset + 3] = 64

    tri.go()
    time.sleep(0.1)


# for i in range(511, 0, -4):
#     model.leds[3][i] = 200
#     tri.go()
#     time.sleep(0.02)

# for d in range(1, 13):
#     u = model.leds[d]
#     u[3] = 200
#     if d > 1:
#         model.leds[d - 1][510] = 200
#         model.leds[d - 1][505] = 200
#         model.leds[d - 1][500] = 200
#     tri.go()
