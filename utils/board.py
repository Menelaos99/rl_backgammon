import sys
import os.path as osp 
import numpy as np
import matplotlib.pyplot as plt
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
        # +2 out lanes, +2 end game lanes
        self.board_storage = {i: {j: 0 for j in range(1, 16)} for i in range(1, 29)}
        self._init_pulia_on_board()
        self.counts = [0 for _ in range(28)]
        self._get_counts()

    def _get_counts(self):
        #24th -> P1 & 25th -> P2 index are for puli that are forced out of the game
        for i in range(28):
            el = list(self.board_storage[i+1].values())
            count = np.count_nonzero(el)
            self.counts[i] = count

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

            pygame.draw.line(win, [0, 0, 0], (DEAD_AREA + PULI_DIAMETER*6, DEAD_AREA), (DEAD_AREA + PULI_DIAMETER*6, HEIGHT-(DEAD_AREA+1)), width=OUTLINE_THICKNESS)
            pygame.draw.line(win, [0, 0, 0], (DEAD_AREA + PULI_DIAMETER*7, DEAD_AREA), (DEAD_AREA + PULI_DIAMETER*7, HEIGHT-(DEAD_AREA+1)), width=OUTLINE_THICKNESS)

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
        # init_pos = [(1, 5, 'p1'), (2,5,'p1'), (3,5,'p1'), (24,5,'p2'), (23,5,'p2'), (22,5,'p2')]
        for tup in init_pos:
            lane = tup[0]
            assert (lane< 25 and tup[1] < 7)
            for vpos in range(1, tup[1]+1):
                if tup[2] == 'p1':
                    color=PULI_COLOR_P1
                else:
                    color=PULI_COLOR_P2
                
                self.board_storage[lane][vpos] = \
                    Puli(
                        color=color,
                        lane=lane,
                        vpos=vpos
                    )
                
    def move(
            self,
            puli: Puli,
            lane: int,
            vpos: int,
            endgame: bool = False
        ):
        assert isinstance(lane, int)
        assert isinstance(vpos, int)
        
        out_lane = 0
        print('counts', self.counts)
        if self.counts[lane-1]==1 and puli.color != self.board_storage[lane][1].color:
            out_puli = self.board_storage[lane][vpos]
            if self.board_storage[lane][1].color == PULI_COLOR_P1:
                self.counts[24] += 1
                out_vpos = self.counts[24]
                out_lane = 25
            else:
                self.counts[25] += 1
                out_vpos = self.counts[25]
                out_lane = 26
            self.board_storage[lane][vpos] = self.board_storage[puli.lane][puli.vpos]
            self.board_storage[puli.lane][puli.vpos] = self.board_storage[lane][vpos+1]

            self.board_storage[out_lane][out_vpos] = out_puli
        elif endgame:
            print('enter end move')
            if puli.color == PULI_COLOR_P1:
                vpos = self.counts[26]
                self.board_storage[27][vpos+1] = self.board_storage[puli.lane][puli.vpos]
                print('lane', puli.lane)
                print('vpos', puli.vpos)
                self.board_storage[puli.lane][puli.vpos]  = 0
            else:
                vpos = self.counts[27]
                self.board_storage[28][vpos+1] = self.board_storage[puli.lane][puli.vpos]
                self.board_storage[puli.lane][puli.vpos] = 0
        else:
            self.board_storage[puli.lane][puli.vpos], self.board_storage[lane][vpos] = self.board_storage[lane][vpos], self.board_storage[puli.lane][puli.vpos]
        print('board_storage', self.board_storage)
        puli.move(lane=lane, vpos=vpos)
        if out_lane:
            out_puli.move(lane=out_lane, vpos=out_vpos)

        self._get_counts()
        print('counts', self.counts)
    
    def draw(
        self,
        win
    ):
        self._draw_board(win=win)
        # +5 lanes because we have +2 out, +2 endgame lanes, i.e. 25, 26 (starting  from 1)
        for lane in range(1, LANES+5):
            if lane > 26:
                counts = self.counts[lane-1]
            else:
                counts = 0
            for vpos in range(1, VPOS+1):
                puli = self.board_storage[lane][vpos]
                if puli:
                    puli.draw(win, counts)

    def get_piece(self, lane, vpos):
        return self.board_storage[lane][vpos]
    
    def _criterion(self, list, roll, puli):
        print('roll', roll)
        print('len list', len(list))
        if len(self.dice)>2:
            if len(list)>0:
                print('if')
                lane = list[-1][0]
            else:
                print('else')
                lane = puli.lane
        else:
            if len(list)>2:
                lane = list[-1][0]
            else:
                lane = puli.lane
        
        print('lane', lane)
        if puli.color == PULI_COLOR_P2:
            lane = lane + roll
            count_pulia = 0
            if lane<25:
                for candidate in self.board_storage[lane].values():
                    # since empty positions have the value 0, if statement filters these values
                    if candidate:
                        count_pulia += 1
                # check if lane has puli or is empty 
                if not isinstance(self.board_storage[lane][1], int): 
                    # same color as player 
                    if (self.board_storage[lane][1].color == PULI_COLOR_P2) and (lane <= LANES):    
                        list.append((lane, count_pulia+1))
                    # different color from player
                    elif (self.board_storage[lane][1].color == PULI_COLOR_P1) and (lane <= LANES):
                        if count_pulia == 1:
                            list.append((lane, count_pulia))
                else:
                    # lane is empty, vpos=1 
                    list.append((lane, 1))
            # except:
            #     list.append(pre_lane)

        else:
            lane = lane - roll
            count_pulia = 0
            if lane>0:
                for candidate in self.board_storage[lane].values():
                    if candidate:
                        count_pulia += 1
                if not isinstance(self.board_storage[lane][1], int): 
                    if self.board_storage[lane][1].color != PULI_COLOR_P2 and (lane > 0):
                        list.append((lane, count_pulia+1))
                    elif (self.board_storage[lane][1].color == PULI_COLOR_P2) and (lane > 0):

                        if count_pulia == 1:
                            list.append((lane, count_pulia))
                else:
                    list.append((lane, 1))
            # except:
            #     list.append(pre_lane)
        print('lane1', lane)
        print('list', list)

    def get_valid_lanes(self, puli, dice: list, endgame=False):
        self.dice = dice
        valid_lanes = []

        print('len dice', len(dice))

        if len(dice) > 2 or len(dice)==1:
            val_range = 1
        else:
            val_range = 2

        print('val range', val_range)
        for i in range(val_range):
            print('i', i)
            if i > 0: 
                dice.reverse()
            # one_hop = []
            for j, roll in enumerate(dice):
                self._criterion(valid_lanes, roll, puli)
                # if j == 0:
                #     print('entered crit')
                #     self._criterion(one_hop, roll, lane, puli)
                # else: 
                #     for lane in one_hop:
                #         #TODO: Check if tuple is necessary
                #         valid_lanes.append(lane)
                #         self._criterion(valid_lanes, roll, lane, puli)
        # if len(dice)==1:
        #     valid_lanes=one_hop

        if endgame and puli.color == PULI_COLOR_P1:
            # vpos = self.counts[26] + 1
            valid_lanes.append((27, 6))
        elif endgame and puli.color == PULI_COLOR_P2:
            # vpos = self.counts[27] + 1
            valid_lanes.append((28, 6))
        
        valid_lanes = list(set(valid_lanes))
        return valid_lanes

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
