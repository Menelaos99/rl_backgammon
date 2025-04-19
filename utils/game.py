import pygame
from copy import deepcopy
import numpy as np
from .board import Board
from .constants import *
from .puli import calc_coor

class Game:
    def __init__(self, win):
        self.win = win
        self._init_game()
        self.p1_entered_endgame, self.p2_entered_endgame = False, False

    def update(self):
        self.board.draw(win=self.win)
        self.draw_valid_moves()
        pygame.display.update()

    def _init_game(self):
        self.selected = None
        self.board = Board()
        self.turn = PULI_COLOR_P2
        self.valid_lanes = {}
        self.count_turn = 0
        self.change = False
        self._roll()

    def reset(self):
        self._init_game()
    
    def _roll(self):
        d1 = np.random.randint(1,7, dtype=int)
        d2 = np.random.randint(1,7, dtype=int)
        d1 = d2 = 1
        self.dice = [d1, d2]
        if d1 == d2:
            self.dice.extend(self.dice)
        self.start_len=len(self.dice)
        print("Roll:", self.dice)

    def select(self, lane, vpos):
        if self.selected:
            print('enter if select')
            print('valid moves', self.valid_lanes)
            result = self._move(lane, vpos)
            if not result:
                self.selected = None
                self.select(lane, vpos)
        
        print('enter select')
        puli = self.board.get_piece(lane, vpos)
        if puli and puli.color == self.turn:
            print('entered selection')
            self.selected = puli
            if self.p1_entered_endgame or self.p2_entered_endgame:
                self.valid_lanes = self.board.get_valid_lanes(puli=puli, dice=self.dice, endgame=True)
            else:
                self.valid_lanes = self.board.get_valid_lanes(puli=puli, dice=self.dice)
                print('after selection valid', self.valid_lanes)
            print('end\n')
            return True
            
        return False

    def bring_back_in(self, puli, lane):
        puli_tmp = deepcopy(puli)
        puli_tmp.lane = lane
        self.selected = puli
        self.valid_lanes = self.board.get_valid_lanes(puli=puli_tmp, dice=self.dice)

    def change_turn(self):
        self._roll()
        self.valid_lanes = {}
        self.count_turn = 0
        if self.turn == PULI_COLOR_P1:
            self.turn = PULI_COLOR_P2
        else:
            self.turn = PULI_COLOR_P1
    
    def _move(self, lane, vpos):
        piece = self.board.get_piece(lane, vpos)

        if self.p1_entered_endgame or self.p2_entered_endgame:
            endgame = True
        else:
            endgame = False
        
        if self.selected \
            and (piece == 0 or (piece != 0 and self.board.counts[lane-1]==1)) \
            and (lane, vpos) in self.valid_lanes:
            self.count_turn += 1
            
            print('valid lanes in _move', self.valid_lanes)
            # if len(self.valid_lanes)>2:
            #     if self.selected.color == PULI_COLOR_P2:
            #         thr = max(t[0] for t in self.valid_lanes)
            #     else:
            #         thr = min(t[0] for t in self.valid_lanes)
            # else:
            #     thr = None
            
            if self.selected.color == PULI_COLOR_P2:
                if self.selected.lane == 26:
                    picked_roll = lane
                else:
                    picked_roll = lane - self.selected.lane
            elif self.selected.color == PULI_COLOR_P1:
                if self.selected.lane == 0:
                    picked_roll = lane
                else:
                    picked_roll = self.selected.lane - lane
            # print('selected', self.selected.lane)
            # print('lane', lane)
            # if ((picked_roll==sum(self.dice)) or self.count_turn==2) and self.start_len>2:
            #     self.dice = []
            #     change = True
            # elif len(self.dice)>2:
            #     print('picked_roll', picked_roll)
            #     print(self.dice[0])
            #     pop_range = int(picked_roll/self.dice[0])
            #     print('pop range', pop_range)
            #     [self.dice.pop(0) for _ in range(pop_range)] 
            #     if pop_range == 0:
            #         change = True
            #     else:
            #         change = False
            # else:
            #     roll_idx = self.dice.index(picked_roll)
            #     self.dice.pop(roll_idx)
            #     change = False
        
            # try:
            #     roll_idx = self.dice.index(picked_roll)
            #     self.dice.pop(roll_idx)
            # except:
            #     print('entered except')
            #     for _ in range(len(self.dice)):
            #         self.dice.pop(0)

            self.board.move(self.selected, lane, vpos, endgame=endgame)
            
            if self.start_len>2:
                pop_range = int(picked_roll/self.dice[0])
                [self.dice.pop(0) for _ in range(pop_range)] 
            elif picked_roll==sum(self.dice):
                self.dice = []
            elif self.start_len<=2:
                roll_idx = self.dice.index(picked_roll)
                self.dice.pop(roll_idx)
            # else:
            #     idx = self.valid_lanes.index((lane, vpos))            
            #     self.valid_lanes.pop(idx)
            print('len dice', len(self.dice))
            if not self.dice:
                self.change_turn()
            print('picked roll', picked_roll)
            print('valid lanes after', self.valid_lanes)
            # for tup in self.valid_lanes:
        else:
            return False

        return True
    
    def draw_valid_moves(self):
        for lane, vpos in self.valid_lanes:
            center = calc_coor(lane, vpos)
            pygame.draw.circle(self.win, GREEN, center, 5)
    
    def check_endgame(self):
        color = [0,0,0]
        total_counts_p1 = 0
        total_counts_p2 = 0
        total_counts_p1_endgame = 0
        total_counts_p2_endgame = 0
        for lane in range(1, 25):
            try:
                color = self.board.board_storage[lane][1].color
            except:
                continue
            if color == PULI_COLOR_P1:
                total_counts_p1 += self.board.counts[lane-1]
                if 0 < lane < 7:
                    total_counts_p1_endgame += self.board.counts[lane-1]
            elif color == PULI_COLOR_P2:
                total_counts_p2 += self.board.counts[lane-1]
                if 18 < lane < 25:
                    total_counts_p2_endgame += self.board.counts[lane-1]

        if total_counts_p1 == total_counts_p1_endgame:
            self.p1_entered_endgame = True
        if total_counts_p2 == total_counts_p2_endgame:
            self.p2_entered_endgame = True