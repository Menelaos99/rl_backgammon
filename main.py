import os 
import pygame
from utils.objects import *

def main():
    pygame.init()
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    board = Board(pouli_radius=20)
    
    img_array_t = np.transpose(board.board_grid, (1, 0, 2))

    screen = pygame.display.set_mode((img_array_t.shape[0], img_array_t.shape[1]), pygame.RESIZABLE)
    surface = pygame.surfarray.make_surface(img_array_t)
    clock = pygame.time.Clock()
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
    
            screen.blit(surface, (0, 0))
            pygame.display.flip()  # or pygame.display.update()

            clock.tick(60)
        
        

if __name__=="__main__":
    main()