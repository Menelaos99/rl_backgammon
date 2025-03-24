import pygame
import numpy as np
import os 

pygame.init()

os.environ["SDL_VIDEO_CENTERED"] = '1'
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

display = pygame.display.set_mode((screen_width - 10, screen_height - 50), pygame.RESIZABLE)

display = pygame.display.set_mode((350, 350), pygame.RESIZABLE)
x = np.arange(0, 350)
y = np.arange(0, 350)
X, Y = np.meshgrid(x, y)
Z = X + Y
Z = 255*Z/Z.max()
surf = pygame.surfarray.make_surface(Z)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display.blit(surf, (0, 0))
    pygame.display.update()
pygame.quit()