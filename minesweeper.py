import random

class Board:
    def __init__(self, grid_scale):
        self.grid_scale = grid_scale # dimensiones.
        self.grid_structure = [[Cell() for i in range(self.grid_scale)] for j in range(self.grid_scale)] # martiz de objetos Cell.
        self.adj_mines_coords = [] # Adjacent mines.
        self.mines_proportion = 0.20
        self.mines_pos_list = [] # Position of all the mines.
        self.set_mines()

    def set_mines(self):
        mine = round((self.grid_scale ** 2) * self.mines_proportion)
        for i in range(mine):
            x = random.randint(1, self.grid_scale) - 1
            y = random.randint(1, self.grid_scale) - 1
            if self.grid_structure[x][y].has_mine == False:
                self.mines_pos_list.append((x, y))
                self.grid_structure[x][y].has_mine = True
            else:
                i -= 1

    def adjacent_cells(self):
        row, column = 5, 5
        displacements = [ # Displacements to the 8 adjacent Cell.
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        adjacente_cell_coords = []
        for displac_row, displac_column in displacements:
            new_row, new_column = row + displac_row, column + displac_column
            # Within limits.
            if 0 <= new_row < len(self.grid_structure) and 0 <= new_column < len(self.grid_structure[0]):
                adjacente_cell_coords.append((new_row, new_column))

        return adjacente_cell_coords
    
    def calculate_adjacent_mines(self): # obtiene coordenadas de Cell alrededos. --method
        pass

    def temporal_show(self):
        for i in range(self.grid_scale):
            fila = []
            for j in range(self.grid_scale):
                if self.grid_structure[i][j].has_mine:
                    fila.append("2")
                else:
                    fila.append("0")
            print(" ".join(fila))

class Cell:
    def __init__(self):
        self.has_mine = False # tiene mina.
        self.revealed_mine = False # la mina es visible.

        self.marked_mine = False # fue marcada.
        self.surounding_mines = int # mians al rededor.

class Winner:
    def victory_conditions(self):
        # condiciones victoria.
        # condiciones derrota.
        pass

class GameLogic:# logic
    def __init__(self, grid: list[list[bool]], mark: int):
        # q pasa al revelarse una Cell.
        # revelar celdas vacias automaticamente.
        # decide cuando se gana.
        # decide cuando se pierde.

        self.grid = grid
        self.mark = mark

    def set_mark(self):
        try:
            mark_x = int(input("X: ")) - 1
            mark_y = int(input("y: ")) - 1 
            
            if self.grid[mark_x][mark_y] == False:
                self.grid[mark_x][mark_y] = True
                return 1
        except IndexError:
            print("Out of range bitch.")

class Game:
    def __init__(self):
        # llama eventos: logic, winner.
        # estado del juego.
        pass
dim = 10

grid = Board(dim)
grid.temporal_show()
grid.adjacent_cells()
#game = GameLogic(grid, 1)
#game.loop()