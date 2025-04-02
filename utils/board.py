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
    def __init__(self,):
        self.board_storage = {i: {j: None for j in range(1, 7)} for i in range(1, 25)}
        self._init_pulia_on_board()
        
    def _draw_board(
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

        for hor in range(6):
            top_left_outline = [
                (DEAD_AREA + PULI_DIAMETER*hor, DEAD_AREA),
                (DEAD_AREA + int(PULI_DIAMETER/2)+PULI_DIAMETER*hor, PULI_DIAMETER*5),
                (DEAD_AREA + PULI_DIAMETER + PULI_DIAMETER*hor, DEAD_AREA)
            ]
            pygame.draw.polygon(win, OUTLINE_COLOR, top_left_outline)
            top_left = [
                (DEAD_AREA + PULI_DIAMETER*hor + 2, DEAD_AREA),
                (DEAD_AREA + int(PULI_DIAMETER/2)+PULI_DIAMETER*hor, PULI_DIAMETER*5 - 10),
                (DEAD_AREA + PULI_DIAMETER + PULI_DIAMETER*hor - 2, DEAD_AREA)
            ]
            pygame.draw.polygon(win, LIGHT_WOOD, top_left)

            top_right_outline = [
                (ACTIVE_WIDTH - (hor*PULI_DIAMETER), DEAD_AREA),
                (ACTIVE_WIDTH - (int(PULI_DIAMETER/2) + PULI_DIAMETER*hor), PULI_DIAMETER*5),
                (ACTIVE_WIDTH - (PULI_DIAMETER + PULI_DIAMETER*hor), DEAD_AREA)
            ]
            pygame.draw.polygon(win, OUTLINE_COLOR, top_right_outline)
            top_right = [
                (ACTIVE_WIDTH - (hor*PULI_DIAMETER + 2), DEAD_AREA),
                (ACTIVE_WIDTH - (int(PULI_DIAMETER/2) + PULI_DIAMETER*hor), PULI_DIAMETER*5 - 10),
                (ACTIVE_WIDTH - (PULI_DIAMETER + PULI_DIAMETER*hor - 2), DEAD_AREA)
            ]
            pygame.draw.polygon(win, LIGHT_WOOD, top_right)

            bottom_left_outline = [
                (DEAD_AREA + hor*PULI_DIAMETER, ACTIVE_HEIGHT - 1),
                (DEAD_AREA + int(PULI_DIAMETER/2) + PULI_DIAMETER*hor, ACTIVE_HEIGHT - PULI_DIAMETER*5 - 1),
                (DEAD_AREA + PULI_DIAMETER + PULI_DIAMETER*hor, ACTIVE_HEIGHT - 1)
            ]
            pygame.draw.polygon(win, OUTLINE_COLOR, bottom_left_outline)
            bottom_left = [
                (DEAD_AREA + hor*PULI_DIAMETER + 2, ACTIVE_HEIGHT - 1),
                (DEAD_AREA + int(PULI_DIAMETER/2) + PULI_DIAMETER*hor, ACTIVE_HEIGHT - PULI_DIAMETER*5 + 9),
                (DEAD_AREA + PULI_DIAMETER + PULI_DIAMETER*hor - 2, ACTIVE_HEIGHT - 1)
            ]
            pygame.draw.polygon(win, LIGHT_WOOD, bottom_left)

            bottom_right_outline = [
                (ACTIVE_WIDTH - hor*PULI_DIAMETER, ACTIVE_HEIGHT - 1),
                (ACTIVE_WIDTH - (int(PULI_DIAMETER/2) + PULI_DIAMETER*hor), ACTIVE_HEIGHT - PULI_DIAMETER*5 - 1),
                (ACTIVE_WIDTH - (PULI_DIAMETER + PULI_DIAMETER*hor), ACTIVE_HEIGHT - 1)
            ]
            pygame.draw.polygon(win, OUTLINE_COLOR, bottom_right_outline)
            bottom_right = [
                (ACTIVE_WIDTH - (hor*PULI_DIAMETER + 2), ACTIVE_HEIGHT - 1),
                (ACTIVE_WIDTH - (int(PULI_DIAMETER/2) + PULI_DIAMETER*hor), ACTIVE_HEIGHT - PULI_DIAMETER*5 + 9),
                (ACTIVE_WIDTH - (PULI_DIAMETER + PULI_DIAMETER*hor - 2), ACTIVE_HEIGHT - 1)
            ]
            pygame.draw.polygon(win, LIGHT_WOOD, bottom_right)

            pygame.draw.line(win, [0, 0, 0], (DEAD_AREA + PULI_DIAMETER*6, DEAD_AREA), (DEAD_AREA + PULI_DIAMETER*6, HEIGHT-(DEAD_AREA+1)), width=3)
            pygame.draw.line(win, [0, 0, 0], (DEAD_AREA + PULI_DIAMETER*7, DEAD_AREA), (DEAD_AREA + PULI_DIAMETER*7, HEIGHT-(DEAD_AREA+1)), width=3)

            for i in range(1, 25):
                if i >18:
                    lane_tmp = i-19
                    lane_range = list(reversed(np.arange(0, 6).tolist()))
                    position = Vector2(ACTIVE_WIDTH - (PULI_DIAMETER*lane_range[lane_tmp] + PULI_RADIUS + 5), int(DEAD_AREA/4))
                elif i>12:
                    lane_tmp = i-13
                    lane_range = list(reversed(np.arange(0, 6).tolist()))
                    position = Vector2(ACTIVE_WIDTH - (PULI_DIAMETER*(lane_range[lane_tmp]+7) + PULI_RADIUS + 5), int(DEAD_AREA/4))
                elif i>6:
                    position = Vector2((ACTIVE_WIDTH - (PULI_DIAMETER*i + PULI_RADIUS + 5), HEIGHT - int(DEAD_AREA/1.2)))
                else: 
                    position = Vector2((ACTIVE_WIDTH - (PULI_DIAMETER*(i-1) + PULI_RADIUS + 5), HEIGHT - int(DEAD_AREA/1.2)))
                
                font = pygame.font.SysFont('arial', size=10)
                text = font.render(str(i), True, [0, 0, 0])
                win.blit(text, position)

    def _init_pulia_on_board(self):
        init_pos = [(1, 2, 'p2'), (6, 5, 'p1'), (8, 3, 'p1'), (12, 5, 'p2'), (13, 5, 'p1'), (17, 3, 'p2'), (19, 5, 'p2'), (24, 2, 'p1')]
        for tup in init_pos:
            assert (tup[0]< 25 and tup[1] < 7)
            for vpos in range(1, tup[1]+1):
                if tup[2] == 'p1':
                    color=PULI_COLOR_P1,
                else:
                    color=PULI_COLOR_P2,
                
                self.board_storage[tup[0]][vpos] = \
                    Puli(
                        color=color,
                        lane=tup[0],
                        vpos=vpos
                    )
                
    def move(
            self,
            puli: Puli,
            lane: int,
            vpos: int,
        ):
        
        assert isinstance(lane, int)
        assert isinstance(vpos, int)

        if self.board_storage[lane][vpos]:
            self.board_storage[puli.lane][puli.vpos], self.board_storage[lane][vpos] = self.board_storage[lane][vpos], self.board_storage[puli.lane][puli.vpos]
            puli.move(lane=lane, vpos=vpos)
    
    def draw(
        self,
        win
    ):
        self._draw_board(win=win)
        for lane in range(1, LANES+1):
            for vpos in range(1, VPOS+1):
                puli = self.board_storage[lane][vpos]
                if puli:
                    puli.draw(win, lane, vpos)

    def get_piece(self, lane, vpos):
        return self.board_storage[lane][vpos]
    
    def _criterion(self, list, roll, lane, puli):
            if puli.color == PULI_COLOR_P1:
                lane = lane + roll
                if (set(self.board_storage[lane][1]).color != set(PULI_COLOR_P2)) and (lane < LANES):    
                    list.append(lane)
                elif (set(self.board_storage[lane][1]).color == set(PULI_COLOR_P2)) and (lane < LANES):
                    count_pulia = 0
                    for candidate in self.board_storage[lane].values():
                        if candidate:
                            count_pulia += 1
                    if count_pulia == 1:
                        list.append(lane)

            else:
                lane = lane - roll
                if set(self.board_storage[lane][1]).color != set(PULI_COLOR_P1) and (lane > 0):
                    list.append(lane)
                elif (set(self.board_storage[lane][1]).color == set(PULI_COLOR_P1)) and (lane > 0):
                    count_pulia = 0
                    for candidate in self.board_storage[lane].values():
                        if candidate:
                            count_pulia += 1
                    if count_pulia == 1:
                        list.append(lane)

    def get_valid_lanes(self, puli, dice):
        valid_lanes = []
        lane= puli.lane

        if dice[0] == dice[1]: val_range = 4
        else: val_range = 2

        for i in range(val_range):
            if i == 0: dice = dice
            else: dice.reverse()
            one_hop = []
            for roll in dice:
                if i == 0:
                    self._criterion(one_hop, roll, lane, puli)
                else: 
                    for lane in one_hop:
                        self._criterion(valid_lanes, roll, lane, puli)
                    valid_lanes = np.unique(valid_lanes).tolist()
        
        return valid_lanes

    # def _place_pulia(self):
    #     num_pulia_up_right = 3
    #     num_lanes = 6
    #     diameter = self.puli_p1.radius*2
    #     for hor in range(num_lanes):
    #         h_offset = diameter*hor 
    #         for vert in range(0, num_pulia_up_right):
    #             v_offset = diameter*vert
    #             # top left
    #             for row in range(
    #                 self.top_left_corner+v_offset,
    #                 self.top_left_corner+diameter+v_offset
    #                 ):
    #                 for col in range(
    #                     self.top_left_corner + h_offset,
    #                     self.top_left_corner+diameter+h_offset
    #                     ):
    #                     self.board[row, col] = self.puli_p1.grid[row-(self.top_left_corner+v_offset), col-(self.top_left_corner+h_offset)]

    #             #bottom left
    #             for row in reversed(range(
    #                 self.board_height-(self.top_left_corner+diameter+(diameter*vert)),
    #                 self.board_height-(self.top_left_corner+(diameter*vert))
    #                 )):
    #                 for col in range(
    #                     self.top_left_corner + (diameter*hor),
    #                     self.top_left_corner+diameter+(diameter*hor)
    #                     ):
    #                     self.board[row, col] = self.puli_p1.grid[row-(self.board_height-(self.top_left_corner+(diameter*vert))), col-(self.top_left_corner+(diameter*hor))]
                
    #             #top right
    #             for row in range(
    #                 self.top_left_corner+(diameter*vert),
    #                 self.top_left_corner+diameter+(diameter*vert)
    #                 ):
    #                 for col in reversed(range(
    #                     self.board_width-(self.top_left_corner+diameter+(diameter*hor)),
    #                     self.board_width - (self.top_left_corner + (diameter*hor))
    #                     )):
    #                     self.board[row, col] = self.puli_p1.grid[row-(self.top_left_corner+(diameter*vert)), col-(self.board_width - (self.top_left_corner + (diameter*hor)))]
                
    #             #bottom right
    #             for row in reversed(range(
    #                 self.board_height-(self.top_left_corner+diameter+(diameter*vert)),
    #                 self.board_height-(self.top_left_corner+(diameter*vert))
    #                 )):
    #                 for col in reversed(range(
    #                     self.board_width-(self.top_left_corner+diameter+(diameter*hor)),
    #                     self.board_width - (self.top_left_corner + (diameter*hor))
    #                     )):
    #                     self.board[row, col] = self.puli_p1.grid[row-(self.board_height-(self.top_left_corner+(diameter*vert))), col-(self.board_width - (self.top_left_corner + (diameter*hor)))]


    #     # plt.imshow(self.board)
    #     # plt.show()
    #     return

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
