import os 
import pygame
import numpy as np
from utils.board import Board
from utils.game import Game
from utils.constants import *

def get_row_col_from_mouse(pos):
    x, y = pos
    
    mid_left = PULI_DIAMETER*6 + DEAD_AREA + OUTLINE_THICKNESS
    mid_right = mid_left + PULI_DIAMETER + OUTLINE_THICKNESS

    mid_height = DEAD_AREA + OUTLINE_THICKNESS + 6*PULI_DIAMETER

    # 6 = line width * 2
    if y < mid_height:
        if mid_left<x<mid_right:
            lane = 28
        elif x > mid_right:
            lane = int(int((x + ACTIVE_WIDTH - DEAD_AREA - PULI_DIAMETER - 6))//PULI_DIAMETER) - 1
        elif x < mid_left:
            lane = int(int((x + ACTIVE_WIDTH - DEAD_AREA ))//PULI_DIAMETER) - 1
        vpos = ((y - DEAD_AREA)//PULI_DIAMETER) + 1
    else: 
        vpos_list = [i for i in range(1, 7)]
        vpos_list.reverse()
        vpos = (y - ACTIVE_HEIGHT//2)//PULI_DIAMETER
        vpos = vpos_list[vpos]
        
        lanes = [i for i in range(1, 13)]
        lanes.reverse()
        if mid_left<x<mid_right:
            lane = 27
        elif x > mid_right:
            tmp_lane = int(int(x - DEAD_AREA - PULI_DIAMETER- 6)//PULI_DIAMETER)
            lane = lanes[tmp_lane]
        elif x < mid_left: 
            tmp_lane = int(int(x - DEAD_AREA)//PULI_DIAMETER)
            lane = lanes[tmp_lane]
    return lane, vpos

def main():
    pygame.init()
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    info = pygame.display.Info()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    
    game = Game(win=screen)

    clock = pygame.time.Clock()
    reenter = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.check_endgame()
                pos = pygame.mouse.get_pos()
                lane, vpos = get_row_col_from_mouse(pos)
                
                if reenter:
                    game.select(lane, vpos)
                    reenter = False
                elif (game.turn == PULI_COLOR_P1) and game.board.board_storage[25][1]:
                    reenter = True
                    puli_idx = max(np.nonzero(list(game.board.board_storage[25].values()))[0].tolist())
                    puli = game.board.board_storage[25][puli_idx+1]
                    game.bring_back_in(puli, lane=25)
                elif  (game.turn == PULI_COLOR_P2) and game.board.board_storage[26][1]:
                    reenter = True
                    puli_idx = max(np.nonzero(list(game.board.board_storage[26].values()))[0].tolist())
                    puli = game.board.board_storage[26][puli_idx+1]
                    game.bring_back_in(puli, lane=0)
                else:
                    game.select(lane, vpos)

            game.update()

            pygame.display.flip()  
            clock.tick(60)
    pygame.quit()
        

if __name__=="__main__":
    main()