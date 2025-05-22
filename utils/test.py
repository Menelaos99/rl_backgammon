import sys
import pygame

from utils.constants import *
from utils.board import Board

def test(obj):
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test")

    circle_position = (200, 200) 
    circle_radius = 50

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        if obj=='puli':
            obj(
                win=screen,
                center=circle_position,
                radius=circle_radius,
                color=PULI_COLOR
            )
        elif obj=='board':
            Board(
                win=screen,
            )
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()