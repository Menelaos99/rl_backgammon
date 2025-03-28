import numpy as np
import pygame
from constants import *
from skimage import draw

class Puli():
    def __init__(
            self,
            win: pygame.surface.Surface=None,
            radius: int=20,
            color: np.array=[255, 0, 0]
        ):
        self.win = win
        self.radius = radius
        self.color = color             
        # self.draw(win)
        # self.grid=self._create()
    
    def draw(self, center):
        pygame.draw.circle(self.win, OUTLINE_COLOR, center, self.radius)
        pygame.draw.circle(self.win, self.color, center, self.radius-3)
        pygame.draw.circle(self.win, OUTLINE_COLOR, center, int(self.radius/2))
        pygame.draw.circle(self.win, self.color, center, int(self.radius/2)-3)

# if __name__=="__main__":
#     test_comps()    

