from math import *
from main import *

def has_line_of_sight(start_px, end_px, tilemap, tile_size):
    x0, y0 = start_px
    x1, y1=  end_px
    tx0, ty0 = pixel_to_tile(x0, y0, tile_size)
    tx1, ty1 = pixel_to_tile(x1, y1, tile_size)
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return True
    
    step_x = dx / steps
    step_y = dy / steps

    x, y = x0, y0

    for _ in range(steps):
        if y < 0 or y >= len(tilemap) or x < 0 or x >= len(tilemap[0]):
            return False

        if tilemap[int(y)][int(x)] == 1:
            return False
        
        x += step_x
        y += step_y
    return True

