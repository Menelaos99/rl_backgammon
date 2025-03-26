import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from skimage import draw

#TODO: add identifies sta poulia (is it a good idea?)

class isosceles():
    def __init__(
            self,
            width: int,
            height: int,
            reverse: bool
        ):
        
        self.grid = np.zeros((height, width, 3), dtype=np.uint8)
        self.grid[:, :] = [161, 102, 47]
        start_color=False
        if reverse:
            rr, cc = draw.line(0, 0, height-1, int(width/2))
            self.grid[rr, cc] = [180, 133, 89]
            rr, cc = draw.line(0, width-1, height-1, int(width/2))
            self.grid[rr, cc] = [180, 133, 89]

            for x in range(width):
                for y in reversed(range(height)):
                    if np.array_equal(self.grid[y, x], [180, 133, 89]):
                        self.grid[y:y+2, x] = [0, 0, 0]
                        start_color=True
                    if start_color:
                        self.grid[y, x]= [180, 133, 89]
                    if y == 0:
                        start_color=False
        else:
            rr, cc = draw.line(height-1, 0, 0, int(width/2))
            self.grid[rr, cc] = [180, 133, 89]
            rr, cc = draw.line(height-1, width-1, 0, int(width/2))
            self.grid[rr, cc] = [180, 133, 89]
        
            for x in range(width):
                for y in range(height):
                    if np.array_equal(self.grid[y, x], [180, 133, 89]):
                        self.grid[y-2:y, x] = [0, 0, 0]
                        # self.grid[y-2, x] = [0, 0, 0]
                        start_color=True
                    if start_color:
                        self.grid[y, x]= [180, 133, 89]
                    if y == self.grid.shape[0]-1:
                        start_color=False

        # plt.imshow(self.grid)
        # plt.show()
        # print(self.grid)

class Pouli():
    def __init__(
            self,
            radius: int=20,
            color: np.array=[255, 0, 0]
        ):
        self.radius = radius
        self.color = color
        self.grid=self._create()
        
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

class Diamond():
    def __init__(self):
        pass

class Board():
    def __init__(
            self,
            pouli_radius:int=20,
            wood_set:int=24
        ):
        self.pouli_radius = 20
        self.p_diameter = self.pouli_radius*2

        self.triangle = isosceles(
            height=pouli_radius*2*5,
            width=pouli_radius*2,
            reverse=True
        )
        self.reversed_triangle = isosceles(
            height=pouli_radius*2*5,
            width=pouli_radius*2,
            reverse=False
        )
        
        self.height=(pouli_radius*12*2)+wood_set*2
        self.width=(pouli_radius*13*2)+wood_set*2
        
        self.black_offset = wood_set-4
        self.wood_set = wood_set
        self.board_grid = self._create_board()
        
        # self.pouli_p1 = Pouli(radius=pouli_radius, color=[255, 0, 0])
        # self.pouli_p2 = Pouli(radius=pouli_radius, color=[0, 0, 255])
        # self._place_poulia()

    def _create_board(
            self,
        ):
        board = np.ones((self.height, self.width, 3), dtype=np.uint8)
        board[:, :] = [161, 102, 47] 

        rr, cc = draw.rectangle((self.black_offset, self.black_offset), end=(board.shape[0]-self.black_offset, board.shape[1]-self.black_offset), shape=board.shape)
        board[rr, cc] = [0, 0, 0]

        rr, cc = draw.rectangle((self.wood_set, self.wood_set), end=(board.shape[0]-self.wood_set, board.shape[1]-self.wood_set), shape=board.shape)
        board[rr, cc] = [161, 102, 47]

        for hor in range(6):
            offset = hor*self.p_diameter
            #top left
            for col in range(
                self.wood_set + offset,
                self.wood_set+self.p_diameter + offset
                ):
                for row in range(
                    self.wood_set, 
                    self.wood_set + self.p_diameter*5
                ):
                    board[row, col] = self.triangle.grid[row-self.wood_set, col-(self.wood_set+offset)]
            
            #top right
            for col in reversed(range(
                self.width-(self.wood_set + self.p_diameter + self.p_diameter*hor),
                self.width - (self.wood_set + (self.p_diameter*hor))
            )):
                for row in range(
                    self.wood_set,
                    self.wood_set + self.p_diameter*5
                ):
                    board[row, col] = self.triangle.grid[row-self.wood_set, col-(self.width - (self.wood_set + (self.p_diameter*hor)))]
            
            #bottom left
            for col in range(
                self.wood_set + (self.p_diameter*hor),
                self.wood_set + self.p_diameter + (self.p_diameter*hor)
                ):
                for row in reversed(range(
                    self.height-(self.wood_set+self.p_diameter*5),
                    self.height-(self.wood_set)
                )):
                    board[row, col] = self.reversed_triangle.grid[row-(self.height-(self.wood_set)), col-(self.wood_set+(self.p_diameter*hor))]

            #bottom right
            for row in reversed(range(
                self.height-(self.wood_set+self.p_diameter*5),
                self.height-(self.wood_set)
                )):
                for col in reversed(range(
                    self.width-(self.wood_set+self.p_diameter+(self.p_diameter*hor)),
                    self.width - (self.wood_set + (self.p_diameter*hor))
                    )):
                    board[row, col] = self.reversed_triangle.grid[row-(self.height-(self.wood_set)), col-(self.width - (self.wood_set + (self.p_diameter*hor)))]
        plt.imshow(board)
        plt.show()
        # xs = np.arange(0, window_size)
        # ys = np.arange(0, window_size)
        # X, Y = np.meshgrid(xs, ys)
        # Z = np.zeros((window_size, window_size, 3), dtype=np.uint8)
        # Z = np.zeros((3,))
        
        # for y in range(20, board.shape[0]-20):
        #     for x in range(20, board.shape[1]-20):

        # sigma = 1
        # mu = - sigma * stats.norm.ppf(1/3)
        # for y in range(board.shape[0]):
        #     for x in range(board.shape[1]):
        #         if y<20 or y>(window_size-20) or x<20 or x>(window_size-20):#or i>(window_size-20) or j<20 or j>(window_size-20)
        #             # Z[y, x, :] = [161, 102, 47]
        #             board[y, x, :] = [161, 102, 47]

        #             sample = np.random.normal(mu, sigma)
        #             if sample > 0:
        #                 # Z[y, x, :] = [161, 102, 47] + np.random.rand(3,) * 10
        #                 # noise = (np.random.rand(3,) * 10).astype(np.uint8)
        #                 board[y, x, :] = [161, 102, 47] + (np.random.rand(3,) * 10)
        return board
    
    def _place_poulia(self):
        num_poulia_up_right = 3
        num_lanes = 6
        diameter = self.pouli_p1.radius*2
        for hor in range(num_lanes):
            h_offset = diameter*hor 
            for vert in range(0, num_poulia_up_right):
                v_offset = diameter*vert
                # top left
                for row in range(
                    self.wood_set+v_offset,
                    self.wood_set+diameter+v_offset
                    ):
                    for col in range(
                        self.wood_set + h_offset,
                        self.wood_set+diameter+h_offset
                        ):
                        self.board[row, col] = self.pouli_p1.grid[row-(self.wood_set+v_offset), col-(self.wood_set+h_offset)]

                #bottom left
                for row in reversed(range(
                    self.height-(self.wood_set+diameter+(diameter*vert)),
                    self.height-(self.wood_set+(diameter*vert))
                    )):
                    for col in range(
                        self.wood_set + (diameter*hor),
                        self.wood_set+diameter+(diameter*hor)
                        ):
                        self.board[row, col] = self.pouli_p1.grid[row-(self.height-(self.wood_set+(diameter*vert))), col-(self.wood_set+(diameter*hor))]
                
                #top right
                for row in range(
                    self.wood_set+(diameter*vert),
                    self.wood_set+diameter+(diameter*vert)
                    ):
                    for col in reversed(range(
                        self.width-(self.wood_set+diameter+(diameter*hor)),
                        self.width - (self.wood_set + (diameter*hor))
                        )):
                        self.board[row, col] = self.pouli_p1.grid[row-(self.wood_set+(diameter*vert)), col-(self.width - (self.wood_set + (diameter*hor)))]
                
                #bottom right
                for row in reversed(range(
                    self.height-(self.wood_set+diameter+(diameter*vert)),
                    self.height-(self.wood_set+(diameter*vert))
                    )):
                    for col in reversed(range(
                        self.width-(self.wood_set+diameter+(diameter*hor)),
                        self.width - (self.wood_set + (diameter*hor))
                        )):
                        self.board[row, col] = self.pouli_p1.grid[row-(self.height-(self.wood_set+(diameter*vert))), col-(self.width - (self.wood_set + (diameter*hor)))]


        plt.imshow(self.board)
        plt.show()
        return
                    


#Test
def test():
    pouli_radius = 20
    # isosceles(
    #     height=pouli_radius*2*5,
    #     width=pouli_radius*2,
    #     reverse=True
    # )
    Board(pouli_radius=pouli_radius)
    # pouli(20)
    # x = np.array([[[1, 1, 1],
    #            [255, 255, 255]],
    #           [[  1, 255, 255],
    #            [255, 255, 255]],
    #           [[255, 255, 255],
    #            [255,   6, 255]]], dtype=np.uint8)
    # print(x.shape)
    # mask = np.all(x == 255, axis=2, keepdims=True)
    # print(mask.shape)

    # # broadcast the mask against the array to make the dimensions the same
    # x, mask = np.broadcast_arrays(x, mask)

    # # construct a masked array
    # mx = np.ma.masked_array(x, mask)

    # plt.imshow(mx)
    # plt.show()

if __name__ == "__main__":
    test()
