import numpy as np
import pygame
import time
import sys


class GameOfLife():
    """
    An object oriented version of Conway's Game of Life
    """
    def __init__(self, x=50, y=50, delay=0, theme="dark", title="Bruno's Game"):
        """
        :param x: number of rows in the grid
        :param y: number of columns in the grid
        :param delay: duration in seconds between each game iteration
        :param theme: game color theme
        :param title: game title
        """
        x, y, delay = int(x), int(y), float(delay)
        assert x >= 20 and y >= 20, "Dimensions of grid are less than 20x20"
        assert delay >= 0 and delay < 10, "Delay out of the [0, 10) range"
        assert str(theme).casefold() in ["dark", "light", "dartmouth"], "Theme not available, choose 'dark', 'light', or 'Dartmouth'"
        self.__x = x
        self.__y = y
        self.__delay = delay
        self.__theme = str(theme).casefold()
        self.__title = title
        self.__size = 9


    def iterate_cells(self, grid, current):
        dying_col, alive_col, back_col = self.change_theme(self.__theme) # calling staticmethod to set the colors
        next = np.zeros(current.shape)

        for i in range(current.shape[0]):
            for j in range(current.shape[1]):
                num_alive = np.sum(current[i-1:i+2, j-1:j+2])-current[i,j] # calculates number of alive neighbors

                if (current[i, j] == 1 and (2 <= num_alive <= 3)) or (current[i, j] == 0 and num_alive == 3):  # these elements will stay alive!
                    color = alive_col
                    next[i, j] = 1 # stores in the next grid, which is returned after the close of the loop!
                if current[i, j] == 1 and (num_alive < 2 or num_alive > 3): # these elements will die!
                    color = dying_col
                if current[i, j] == 0: # these elements will stay dead!
                    color = back_col

                pygame.draw.rect(grid, color, (i*self.__size, j*self.__size, self.__size-1, self.__size-1)) # cues up the rectangle to be drawn in the grid

        time.sleep(self.__delay) # controls the delay among iterations
        return next # returns the updated cell states (dead or alive)


    def play_game(self):
        grid = pygame.display.set_mode((self.__y*self.__size, self.__x*self.__size)) # instantiates the grid object's grid
        grid.fill(self.change_theme(self.__theme)[2])
        pygame.display.set_caption(self.__title)
        cells = self.make_cells(self.__y, self.__x) # calling staticmethod to instantiate each cell's dead or alive state
        print(self)

        while True: # controls the game flow
            for event in pygame.event.get(): # pygame way to exit program when user hits the 'X' button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            cells = self.iterate_cells(grid, cells) # calling the method above to cue the grid and update the status of cells for next iteration
            pygame.display.update()  # draws the object that was cued up by pygame.draw.rect(), which is called in self.iterate_cells()


    @staticmethod
    def make_cells(n1, n2):
        cells = np.zeros((n1, n2))
        for i in range(cells.shape[0]):
            for j in range(cells.shape[1]):
                if np.random.randint(0, 2, 1) == 0: # gives each cell a 50/50 chance of being alive at instantiation
                    cells[i, j] = 1
        return cells


    @staticmethod
    def change_theme(mode):
        if mode == 'dark':
            dying_col, alive_col, back_col = (200, 200, 200), (255, 255, 255), (0, 0, 0)
        if mode == 'light':
            dying_col, alive_col, back_col = (55, 55, 55), (0, 0, 0), (255, 255, 255)
        if mode == 'dartmouth':
            dying_col, alive_col, back_col = (200, 200, 200), (255, 255, 255), (0, 105, 62)
        return dying_col, alive_col, back_col


    def __str__(self):
        return f"Welcome to {self.__title}!"


# driver code for command line
if __name__ == "__main__":
    params = {'x':'50', 'y':'50', 'delay':'0', 'theme':"dark", 'title':"Bruno's Game"} # defaults
    keys = [i for i in params.keys()]
    args = sys.argv[1:]

    # conditionality blocks
    if len(args) == 0:
        print(f"No params provided, default used: {params}")

    else:
        ins = [i.split('=') for i in args]
        last_key = 0

        for j in ins:
            if len(j) == 2: # if keyword arg provided
                params[j[0]]=j[1]
                last_key = j[0]
            if len(j) == 1: # if positional arg provided
                if last_key == 0:
                    params[keys[last_key]] = ''.join(j)
                    last_key = keys[last_key]
                else:
                    last_key = keys[keys.index(last_key)+1]
                    params[last_key] = ''.join(j)

        print(f"Custom params provided: {params}")

    # execution
    g1 = GameOfLife(*params.values())
    g1.play_game()
