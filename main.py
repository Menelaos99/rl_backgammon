import os 
import pygame
import numpy as np
from utils.board import Board
from utils.game import Game
from utils.constants import *

def get_row_col_from_mouse(pos):
    x, y = pos
    
    active_width = ACTIVE_WIDTH - PULI_DIAMETER
    # 6 = line width * 2
    if y < ACTIVE_HEIGHT//2:
        if x > int(WIDTH//2):
            lane = int(int((x + ACTIVE_WIDTH - DEAD_AREA - PULI_DIAMETER - 6))//PULI_DIAMETER) - 1
        else:
            lane = int(int((x + ACTIVE_WIDTH - DEAD_AREA ))//PULI_DIAMETER) - 1
        vpos = ((y - DEAD_AREA)//PULI_DIAMETER) + 1
    else: 
        vpos_list = [i for i in range(1, 7)]
        vpos_list.reverse()
        vpos = (y - ACTIVE_HEIGHT//2)//PULI_DIAMETER
        vpos = vpos_list[vpos-1]
        
        lanes = [i for i in range(1, 13)]
        lanes.reverse()
        print("lanes", lanes)
        if x > int(WIDTH//2):
            tmp_lane = int(int(x - DEAD_AREA - PULI_DIAMETER- 6)//PULI_DIAMETER)
        else: 
            tmp_lane = int(int(x - DEAD_AREA)//PULI_DIAMETER)
        print('tmp lane', tmp_lane)
        lane = lanes[tmp_lane]
    print('lane', lane)
    print('pos', vpos)
    return lane, vpos

def main():
    pygame.init()
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    info = pygame.display.Info()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    
    game = Game(win=screen)

    clock = pygame.time.Clock()
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

            game.update()

            pygame.display.flip()  # or pygame.display.update()
            clock.tick(60)
    pygame.quit()
        

if __name__=="__main__":
    main()