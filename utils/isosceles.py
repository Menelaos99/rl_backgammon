import numpy as np
from skimage import draw
from utils.constants import *

class isosceles():
    def __init__(
            self,
            width: int,
            height: int,
            reverse: bool
        ):
        
        self.grid = np.zeros((height, width, 3), dtype=np.uint8)
        self.grid[:, :] = DARK_WOOD
        start_color=False
        if reverse:
            rr, cc = draw.line(0, 0, height-1, int(width/2))
            self.grid[rr, cc] = LIGHT_WOOD
            rr, cc = draw.line(0, width-1, height-1, int(width/2))
            self.grid[rr, cc] = LIGHT_WOOD

            for x in range(width):
                for y in reversed(range(height)):
                    if np.array_equal(self.grid[y, x], LIGHT_WOOD):
                        self.grid[y:y+2, x] = BLACK
                        start_color=True
                    if start_color:
                        self.grid[y, x]= LIGHT_WOOD
                    if y == 0:
                        start_color=False
        else:
            rr, cc = draw.line(height-1, 0, 0, int(width/2))
            self.grid[rr, cc] = LIGHT_WOOD
            rr, cc = draw.line(height-1, width-1, 0, int(width/2))
            self.grid[rr, cc] = LIGHT_WOOD
        
            for x in range(width):
                for y in range(height):
                    if np.array_equal(self.grid[y, x], LIGHT_WOOD):
                        self.grid[y-2:y, x] = BLACK
                        # self.grid[y-2, x] = [0, 0, 0]
                        start_color=True
                    if start_color:
                        self.grid[y, x]= LIGHT_WOOD
                    if y == self.grid.shape[0]-1:
                        start_color=False

        # plt.imshow(self.grid)
        # plt.show()
        # print(self.grid)