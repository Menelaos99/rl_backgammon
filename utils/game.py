import pygame
from .board import Board
from .constants import *

class Game:
    def __init__(self, win):
        self.win = win
        self._init_game()

    def update(self):
        self.board.draw(win=self.win)
        # self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init_game(self):
        self.selected = None
        self.board = Board()
        self.turn = PULI_COLOR_P1
        self.valid_lanes = {}

    def reset(self):
        self._init_game()
    
    def select(self, lane, vpos):
        if self.selected:
            result = self._move(lane, vpos)
            if not result:
                self.selected = None
                self.select(lane, vpos)
        
        puli = self.board.get_piece(lane, vpos)
        if puli and puli.color == self.turn:
            self.selected = puli
            self.valid_lanes = self.board.get_valid_lanes(puli)
            return True
            
        return False

    def change_turn(self):
        self.valid_lanes = {}
        if self.turn == PULI_COLOR_P1:
            self.turn = PULI_COLOR_P2
        else:
            self.turn = PULI_COLOR_P1