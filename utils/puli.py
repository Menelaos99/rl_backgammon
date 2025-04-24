import numpy as np
import pygame
from .constants import *
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

    def draw(self, win, counts):
        # if counts>6:
        #     self.vpos = 6
        self.center = calc_coor(lane=self.lane, vpos=self.vpos, counts=self.vpos)
        pygame.draw.circle(win, OUTLINE_COLOR, self.center, PULI_RADIUS)
        pygame.draw.circle(win, self.color, self.center, PULI_RADIUS-3)
        pygame.draw.circle(win, OUTLINE_COLOR, self.center, int(PULI_RADIUS/2))
        pygame.draw.circle(win, self.color, self.center, int(PULI_RADIUS/2)-3)
        
        if self.lane > 26 or (counts>6 and self.lane<=24):
            font = pygame.font.SysFont('arial', size=10)
            text = font.render(f'x{counts}', True, [0, 255, 0])
            win.blit(text, self.center)

    def move(self, lane, vpos, counts=0):
        self.lane=lane
        self.vpos=vpos
        self.center  = calc_coor(self.lane, self.vpos, counts=counts)

def calc_coor(lane, vpos, counts=0):
    if counts>=6:
        vpos=6
    if lane == 27:
            center = Vector2((DEAD_AREA + 6*PULI_DIAMETER + PULI_RADIUS, ACTIVE_HEIGHT - (5*PULI_DIAMETER + PULI_RADIUS)))
    elif lane == 28:
            center = Vector2((DEAD_AREA + 6*PULI_DIAMETER + PULI_RADIUS, DEAD_AREA + 5*PULI_DIAMETER + PULI_RADIUS))
    elif lane == 26:
        center = Vector2((DEAD_AREA + 6*PULI_DIAMETER + PULI_RADIUS, DEAD_AREA + (vpos-1)*PULI_DIAMETER + PULI_RADIUS))
    elif lane == 25: 
        center = Vector2((DEAD_AREA + 6*PULI_DIAMETER + PULI_RADIUS, ACTIVE_HEIGHT - ((vpos-1)*PULI_DIAMETER + PULI_RADIUS)))
    elif lane >18:
        lane_tmp = lane-19
        lane_range = list(reversed(np.arange(0, 6).tolist()))
        center = Vector2((ACTIVE_WIDTH - (PULI_DIAMETER*lane_range[lane_tmp] + PULI_RADIUS), DEAD_AREA + PULI_DIAMETER*(vpos-1) + PULI_RADIUS))
    elif lane>12:
        lane_tmp = lane-13
        lane_range = list(reversed(np.arange(0, 6).tolist()))
        center = Vector2((ACTIVE_WIDTH - (PULI_DIAMETER*(lane_range[lane_tmp]+7) + PULI_RADIUS), DEAD_AREA + PULI_DIAMETER*(vpos-1) + PULI_RADIUS))
    elif lane>6:
        center = Vector2(((ACTIVE_WIDTH - (PULI_DIAMETER*(lane) + PULI_RADIUS), HEIGHT - (DEAD_AREA + PULI_RADIUS + PULI_DIAMETER*(vpos-1) + 1))))
    else: 
        center = Vector2((ACTIVE_WIDTH - (PULI_DIAMETER*(lane-1) + PULI_RADIUS), HEIGHT - (DEAD_AREA + PULI_RADIUS + PULI_DIAMETER*(vpos-1) + 1)))
    
    return center