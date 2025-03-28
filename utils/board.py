import sys
import os.path as osp 
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from skimage import draw
import pygame
from pygame.math import Vector2

from .constants import *
from .puli import Puli
# from utils.isosceles import isosceles
# from utils.test import test


#TODO: add identifies sta pulia (is it a good idea?)
class Diamond():
    def __init__(self):
        pass

class Board():
    def __init__(
            self,
            win: pygame.surface.Surface=None,
        ):

        # tuple(ROW, COL)
        self.top_left_corner = (DEAD_AREA, DEAD_AREA)
        self.top_right_corner = self.p1_origin = (DEAD_AREA, WIDTH-DEAD_AREA)
        self.bottom_right_corner = self.p2_origin = (HEIGHT-DEAD_AREA, WIDTH-DEAD_AREA)
        self.bottom_left_corner = (HEIGHT-DEAD_AREA, DEAD_AREA)

        self.lane_storage = {str(i): {str(j): None for j in range(1, 7)} for i in range(1, 25)}
        self.win = win

        self.puli_p1 = Puli(
            win=win,
            color=PULI_COLOR_P1,
            radius=PULI_RADIUS
        )
        self.puli_p2 = Puli(
            win=win,
            color=PULI_COLOR_P2,
            radius=PULI_RADIUS
        )
        
        self._init_board(win)
        self._init_pulia()
        
        # self.puli_p1 = Puli(radius=puli_radius, color=[255, 0, 0])
        # self.puli_p2 = Puli(radius=puli_radius, color=[0, 0, 255])
        # self._place_pulia()

    def _init_board(
            self,
            win
        ):
        pygame.draw.rect(win, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(win, DARK_WOOD, (
                                        OUTLINE_THICKNESS, OUTLINE_THICKNESS,
                                        WIDTH-OUTLINE_THICKNESS*2, HEIGHT-OUTLINE_THICKNESS*2
                                        )
        )
        pygame.draw.rect(win, OUTLINE_COLOR, (
                                    OUTLINE_THICKNESS+DEAD_WOODEN_AREA, OUTLINE_THICKNESS+DEAD_WOODEN_AREA,
                                    WIDTH - (OUTLINE_THICKNESS+DEAD_WOODEN_AREA)*2, HEIGHT - (OUTLINE_THICKNESS+DEAD_WOODEN_AREA)*2
                                    )
        )
        pygame.draw.rect(win, DARK_WOOD, (DEAD_AREA, DEAD_AREA, WIDTH-(DEAD_AREA*2), HEIGHT-(DEAD_AREA*2)))

        self.start = WIDTH-DEAD_AREA 
        for hor in range(6):
            top_left_outline = [
                (DEAD_AREA + PULI_DIAMETER*hor, DEAD_AREA),
                (DEAD_AREA + int(PULI_DIAMETER/2)+PULI_DIAMETER*hor, PULI_DIAMETER*5),
                (DEAD_AREA + PULI_DIAMETER + PULI_DIAMETER*hor, DEAD_AREA)
            ]
            pygame.draw.polygon(screen, OUTLINE_COLOR, top_left_outline)
            top_left = [
                (DEAD_AREA + PULI_DIAMETER*hor + 2, DEAD_AREA),
                (DEAD_AREA + int(PULI_DIAMETER/2)+PULI_DIAMETER*hor, PULI_DIAMETER*5 - 10),
                (DEAD_AREA + PULI_DIAMETER + PULI_DIAMETER*hor - 2, DEAD_AREA)
            ]
            pygame.draw.polygon(screen, LIGHT_WOOD, top_left)

            top_right_outline = [
                (self.start - (hor*PULI_DIAMETER), DEAD_AREA),
                (self.start - (int(PULI_DIAMETER/2) + PULI_DIAMETER*hor), PULI_DIAMETER*5),
                (self.start - (PULI_DIAMETER + PULI_DIAMETER*hor), DEAD_AREA)
            ]
            pygame.draw.polygon(screen, OUTLINE_COLOR, top_right_outline)
            top_right = [
                (self.start - (hor*PULI_DIAMETER + 2), DEAD_AREA),
                (self.start - (int(PULI_DIAMETER/2) + PULI_DIAMETER*hor), PULI_DIAMETER*5 - 10),
                (self.start - (PULI_DIAMETER + PULI_DIAMETER*hor - 2), DEAD_AREA)
            ]
            pygame.draw.polygon(screen, LIGHT_WOOD, top_right)

            bottom_left_outline = [
                (DEAD_AREA + hor*PULI_DIAMETER, HEIGHT - DEAD_AREA - 1),
                (DEAD_AREA + int(PULI_DIAMETER/2) + PULI_DIAMETER*hor, HEIGHT - DEAD_AREA - PULI_DIAMETER*5 - 1),
                (DEAD_AREA + PULI_DIAMETER + PULI_DIAMETER*hor, HEIGHT - DEAD_AREA - 1)
            ]
            pygame.draw.polygon(screen, OUTLINE_COLOR, bottom_left_outline)
            bottom_left = [
                (DEAD_AREA + hor*PULI_DIAMETER + 2, HEIGHT - DEAD_AREA - 1),
                (DEAD_AREA + int(PULI_DIAMETER/2) + PULI_DIAMETER*hor, HEIGHT - DEAD_AREA - PULI_DIAMETER*5 + 9),
                (DEAD_AREA + PULI_DIAMETER + PULI_DIAMETER*hor - 2, HEIGHT - DEAD_AREA - 1)
            ]
            pygame.draw.polygon(screen, LIGHT_WOOD, bottom_left)

            bottom_right_outline = [
                (self.start - hor*PULI_DIAMETER, HEIGHT - DEAD_AREA - 1),
                (self.start - (int(PULI_DIAMETER/2) + PULI_DIAMETER*hor), HEIGHT - DEAD_AREA - PULI_DIAMETER*5 - 1),
                (self.start - (PULI_DIAMETER + PULI_DIAMETER*hor), HEIGHT - DEAD_AREA - 1)
            ]
            pygame.draw.polygon(screen, OUTLINE_COLOR, bottom_right_outline)
            bottom_right = [
                (self.start - (hor*PULI_DIAMETER + 2), HEIGHT - DEAD_AREA - 1),
                (self.start - (int(PULI_DIAMETER/2) + PULI_DIAMETER*hor), HEIGHT - DEAD_AREA - PULI_DIAMETER*5 + 9),
                (self.start - (PULI_DIAMETER + PULI_DIAMETER*hor - 2), HEIGHT - DEAD_AREA - 1)
            ]
            pygame.draw.polygon(screen, LIGHT_WOOD, bottom_right)

            pygame.draw.line(screen, [0, 0, 0], (DEAD_AREA + PULI_DIAMETER*6, DEAD_AREA), (DEAD_AREA + PULI_DIAMETER*6, HEIGHT-(DEAD_AREA+1)), width=3)
            pygame.draw.line(screen, [0, 0, 0], (DEAD_AREA + PULI_DIAMETER*7, DEAD_AREA), (DEAD_AREA + PULI_DIAMETER*7, HEIGHT-(DEAD_AREA+1)), width=3)

            for i in range(1, 25):
                if i >18:
                    lane_tmp = i-19
                    lane_range = list(reversed(np.arange(0, 6).tolist()))
                    position = Vector2(self.start - (PULI_DIAMETER*lane_range[lane_tmp] + PULI_RADIUS + 5), int(DEAD_AREA/4))
                elif i>12:
                    lane_tmp = i-13
                    lane_range = list(reversed(np.arange(0, 6).tolist()))
                    position = Vector2(self.start - (PULI_DIAMETER*(lane_range[lane_tmp]+7) + PULI_RADIUS + 5), int(DEAD_AREA/4))
                elif i>6:
                    position = Vector2((self.start - (PULI_DIAMETER*i + PULI_RADIUS + 5), HEIGHT - int(DEAD_AREA/1.2)))
                else: 
                    position = Vector2((self.start - (PULI_DIAMETER*(i-1) + PULI_RADIUS + 5), HEIGHT - int(DEAD_AREA/1.2)))
                
                font = pygame.font.SysFont('arial', size=10)
                text = font.render(str(i), True, [0, 0, 0])
                self.win.blit(text, position)

    def _init_pulia(self):
        init_pos = [(1, 2, 'p2'), (6, 5, 'p1'), (8, 3, 'p1'), (12, 5, 'p2'), (13, 5, 'p1'), (17, 3, 'p2'), (19, 5, 'p2'), (24, 2, 'p1')]
        for tup in init_pos:
            assert (tup[0]< 25 and tup[1] < 7)
        for tup in init_pos:
            for vpos in range(1, tup[1]+1):
                self.lane_storage[str(tup[0])][str(vpos)] = tup[2]
                self.move(tup[0], vpos, tup[2])

    def move(
            self,
            lane: int,
            vpos: int,
            player: str,
        ):
        
        assert isinstance(lane, int)
        assert isinstance(vpos, int)
        
        if self.lane_storage[str(lane)][str(vpos)]:
            if lane >18:
                lane_tmp = lane-19
                lane_range = list(reversed(np.arange(0, 6).tolist()))
                center = Vector2((self.start - (PULI_DIAMETER*lane_range[lane_tmp] + PULI_RADIUS), DEAD_AREA + PULI_DIAMETER*(vpos-1) + PULI_RADIUS))
            elif lane>12:
                lane_tmp = lane-13
                lane_range = list(reversed(np.arange(0, 6).tolist()))
                center = Vector2((self.start - (PULI_DIAMETER*(lane_range[lane_tmp]+7) + PULI_RADIUS), DEAD_AREA + PULI_DIAMETER*(vpos-1) + PULI_RADIUS))
            elif lane>6:
                center = Vector2(((self.start - (PULI_DIAMETER*(lane) + PULI_RADIUS), HEIGHT - (DEAD_AREA + PULI_RADIUS + PULI_DIAMETER*(vpos-1) + 1))))
            else: 
                center = Vector2((self.start - (PULI_DIAMETER*(lane-1) + PULI_RADIUS), HEIGHT - (DEAD_AREA + PULI_RADIUS + PULI_DIAMETER*(vpos-1) + 1)))
            
            if player == 'p1':
                self.puli_p1.draw(center=center)
            else:
                self.puli_p2.draw(center=center)

    def _place_pulia(self):
        num_pulia_up_right = 3
        num_lanes = 6
        diameter = self.puli_p1.radius*2
        for hor in range(num_lanes):
            h_offset = diameter*hor 
            for vert in range(0, num_pulia_up_right):
                v_offset = diameter*vert
                # top left
                for row in range(
                    self.top_left_corner+v_offset,
                    self.top_left_corner+diameter+v_offset
                    ):
                    for col in range(
                        self.top_left_corner + h_offset,
                        self.top_left_corner+diameter+h_offset
                        ):
                        self.board[row, col] = self.puli_p1.grid[row-(self.top_left_corner+v_offset), col-(self.top_left_corner+h_offset)]

                #bottom left
                for row in reversed(range(
                    self.board_height-(self.top_left_corner+diameter+(diameter*vert)),
                    self.board_height-(self.top_left_corner+(diameter*vert))
                    )):
                    for col in range(
                        self.top_left_corner + (diameter*hor),
                        self.top_left_corner+diameter+(diameter*hor)
                        ):
                        self.board[row, col] = self.puli_p1.grid[row-(self.board_height-(self.top_left_corner+(diameter*vert))), col-(self.top_left_corner+(diameter*hor))]
                
                #top right
                for row in range(
                    self.top_left_corner+(diameter*vert),
                    self.top_left_corner+diameter+(diameter*vert)
                    ):
                    for col in reversed(range(
                        self.board_width-(self.top_left_corner+diameter+(diameter*hor)),
                        self.board_width - (self.top_left_corner + (diameter*hor))
                        )):
                        self.board[row, col] = self.puli_p1.grid[row-(self.top_left_corner+(diameter*vert)), col-(self.board_width - (self.top_left_corner + (diameter*hor)))]
                
                #bottom right
                for row in reversed(range(
                    self.board_height-(self.top_left_corner+diameter+(diameter*vert)),
                    self.board_height-(self.top_left_corner+(diameter*vert))
                    )):
                    for col in reversed(range(
                        self.board_width-(self.top_left_corner+diameter+(diameter*hor)),
                        self.board_width - (self.top_left_corner + (diameter*hor))
                        )):
                        self.board[row, col] = self.puli_p1.grid[row-(self.board_height-(self.top_left_corner+(diameter*vert))), col-(self.board_width - (self.top_left_corner + (diameter*hor)))]


        # plt.imshow(self.board)
        # plt.show()
        return

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Test")

    circle_position = (200, 200) 
    circle_radius = 50

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        Board(
            win=screen,
        )
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()
