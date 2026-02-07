import random

class Grid:
    def __init__(self, grid):
        self.grid_scale = grid
        self.general_grid = [[0 for i in range(self.grid_scale)] for j in range(self.grid_scale)]
    
    def set_mines(self, mines_coords, mine_mark):
        for inx, coord in enumerate(mines_coords):
            x, y = coord[0], coord[1]
            
            self.general_grid[x][y] = mine_mark

    def temporal_show(self):
        for i in range(len(self.general_grid)):
            print(self.general_grid[i])

class Mines:
    def __init__(self):
        self.mines_mark = 2
        self.mines_proportion = 0.20 #Entre 12 y 21% en un juego calsico

    def weepers_positions(self, grid_scale, grid: list[list[int]]):
        mine = round((grid_scale ** 2) * self.mines_proportion)
        mines_pos_list = []
        for i in range(mine):
            x = random.randint(1, grid_scale) - 1
            y = random.randint(1, grid_scale) - 1
            if grid[x][y] == 0:
                mines_pos_list.append((x, y))
            else:
                i -= 1
        return mines_pos_list

class Game:
    def __init__(self):
        pass

dim = 10

grid = Grid(dim)
mines = Mines()
mines_coordinates = mines.weepers_positions(dim, grid.general_grid)
grid.set_mines(mines_coordinates, mines.mines_mark)
grid.temporal_show()