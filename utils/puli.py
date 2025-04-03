import numpy as np
import pygame
from .constants import *
from skimage import draw
from pygame.math import Vector2

class Puli():
    def __init__(
            self,
            color: np.array=[255, 0, 0],
            lane: int=0,
            vpos: int=0
        ):
        self.color = color  
        self.lane = lane
        self.vpos = vpos           
        self.center = (0, 0)
        # self.draw(win)
        # self.grid=self._create()
    
    def _calc_coor(self):
        if self.lane >18:
            lane_tmp = self.lane-19
            lane_range = list(reversed(np.arange(0, 6).tolist()))
            center = Vector2((ACTIVE_WIDTH - (PULI_DIAMETER*lane_range[lane_tmp] + PULI_RADIUS), DEAD_AREA + PULI_DIAMETER*(self.vpos-1) + PULI_RADIUS))
        elif self.lane>12:
            lane_tmp = self.lane-13
            lane_range = list(reversed(np.arange(0, 6).tolist()))
            center = Vector2((ACTIVE_WIDTH - (PULI_DIAMETER*(lane_range[lane_tmp]+7) + PULI_RADIUS), DEAD_AREA + PULI_DIAMETER*(self.vpos-1) + PULI_RADIUS))
        elif self.lane>6:
            center = Vector2(((ACTIVE_WIDTH - (PULI_DIAMETER*(self.lane) + PULI_RADIUS), HEIGHT - (DEAD_AREA + PULI_RADIUS + PULI_DIAMETER*(self.vpos-1) + 1))))
        else: 
            center = Vector2((ACTIVE_WIDTH - (PULI_DIAMETER*(self.lane-1) + PULI_RADIUS), HEIGHT - (DEAD_AREA + PULI_RADIUS + PULI_DIAMETER*(self.vpos-1) + 1)))
        self.center = center


    def draw(self, win):
        self._calc_coor()
        pygame.draw.circle(win, OUTLINE_COLOR, self.center, PULI_RADIUS)
        pygame.draw.circle(win, self.color, self.center, PULI_RADIUS-3)
        pygame.draw.circle(win, OUTLINE_COLOR, self.center, int(PULI_RADIUS/2))
        pygame.draw.circle(win, self.color, self.center, int(PULI_RADIUS/2)-3)

    def move(self, lane, vpos):
        self.lane=lane
        self.vpos=vpos
        self._calc_coor()
# if __name__=="__main__":
#     test_comps()    

