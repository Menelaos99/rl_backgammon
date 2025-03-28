import numpy as np
import pygame
from constants import *
from skimage import draw

class Pouli():
    def __init__(
            self,
            win: pygame.surface.Surface=None,
            radius: int=20,
            center: tuple=(20, 20),
            color: np.array=[255, 0, 0]
        ):
        self.center = center
        self.radius = radius
        self.color = color
        self._draw(win)
        # self.grid=self._create()
        
    def _create(self):
        inner_radius = int(self.radius/2)
        
        temp = np.ones((int(self.radius*2), int(self.radius*2), 3))
        # temp[:, :] = [161, 102, 47]
        temp[:, :] = [161, 102, 47] 
        
        center = (int(temp.shape[0]/2), int(temp.shape[1]/2))
        
        rr, cc = draw.disk(center, self.radius, shape=temp.shape)
        temp[rr, cc] = [0, 0, 0] 

        rr, cc = draw.disk(center, self.radius-2, shape=temp.shape)
        temp[rr, cc] = self.color

        rr, cc = draw.disk(center, inner_radius, shape=temp.shape)
        temp[rr, cc] = [0, 0, 0] 

        rr, cc = draw.disk(center, inner_radius-2, shape=temp.shape)
        temp[rr, cc] = self.color 

        # plt.imshow(temp)
        # plt.show()
        return temp
    
    def _draw(self, win):
        pygame.draw.circle(win, BLACK, self.center, self.radius)
        pygame.draw.circle(win, self.color, self.center, self.radius-3)
        pygame.draw.circle(win, BLACK, self.center, int(self.radius/2))
        pygame.draw.circle(win, self.color, self.center, int(self.radius/2)-6)

def test():
    pygame.init()

    screen = pygame.display.set_mode((400, 400))
    print(type(screen))
    pygame.display.set_caption("Circle Drawing Test")

    circle_position = (200, 200)  # Center of the window
    circle_radius = 50

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a white background
        screen.fill((255, 255, 255))
        
        Pouli(
            win=screen,
            center=circle_position,
            radius=circle_radius,
            color=RED
        )
        
        # Update the display
        pygame.display.flip()

    # Clean up
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    test()    

