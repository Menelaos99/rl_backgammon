import pygame
from copy import deepcopy
import numpy as np
from .board import Board
from .constants import *
from .puli import calc_coor, Puli

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
        self.change = False
        self._roll()

    def reset(self):
        self._init_game()
    
    def _roll(self):
        d1 = np.random.randint(1,7, dtype=int)
        d2 = np.random.randint(1,7, dtype=int)
        d1=1
        d2=1
        self.dice = [d1, d2]
        if d1 == d2:
            self.dice.extend(self.dice)
        self.start_len=len(self.dice)
        print("Roll:", self.dice)

    def select(self, lane, vpos):
        if self.selected:
            print('selected in select', self.selected.lane, self.selected.vpos)
            result = self._move(lane, vpos)
            if not result:
                self.selected = None
                self.select(lane, vpos)
        
        puli = self.board.get_piece(lane, vpos)
        if puli and puli.color == self.turn:
            self.selected = puli
            print('selected in select 1', self.selected.lane, self.selected.vpos)
            if self.p1_entered_endgame or self.p2_entered_endgame:
                self.valid_lanes = self.board.get_valid_lanes(puli=puli, dice=self.dice, endgame=True)
            else:
                self.valid_lanes = self.board.get_valid_lanes(puli=puli, dice=self.dice)
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
        
        if self.board.counts[lane-1] >= 6:
            vpos = self.board.counts[lane-1] + 1

        if self.selected \
            and (piece == 0 or (piece != 0 and self.board.counts[lane-1]==1)) or (isinstance(piece, Puli) and self.board.counts[lane-1]>=6)\
            and (lane, vpos) in self.valid_lanes:
            
            if self.selected.color == PULI_COLOR_P2:
                if self.selected.lane == 26:
                    picked_roll = lane
                else:
                    print('lane', lane)
                    print('select', self.selected.lane)
                    picked_roll = lane - self.selected.lane
            elif self.selected.color == PULI_COLOR_P1:
                if self.selected.lane == 0:
                    picked_roll = lane
                else:
                    picked_roll = self.selected.lane - lane
            
            self.board.move(self.selected, lane, vpos, endgame=endgame)
            
            if self.start_len>2:
                print('picked roll', picked_roll)
                print('dice0', self.dice[0])
                pop_range = int(picked_roll/self.dice[0])
                print('pop range', pop_range)
                [self.dice.pop(0) for _ in range(pop_range)] 
            elif picked_roll==sum(self.dice):
                self.dice = []
            elif self.start_len<=2:
                roll_idx = self.dice.index(picked_roll)
                self.dice.pop(roll_idx)
            
            if not self.dice or not self.valid_lanes:
                self.change_turn()
        else:
            return False
        print("board storage", self.board.board_storage)
        return True
    
    def draw_valid_moves(self):
        print('valid lanes', self.valid_lanes)
        for lane, vpos in self.valid_lanes:
            center = calc_coor(lane, vpos, counts=self.board.counts[lane-1])
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