import random
from panda3d.core import loadPrcFileData
from panda3d.core import LineSegs, NodePath
from direct.showbase.ShowBase import ShowBase

loadPrcFileData("", "win-size 1000 1000")
loadPrcFileData("", "window-title Minesweeper")

class Board:
    def __init__(self, grid_scale):
        self.grid_scale = grid_scale # dimensiones.
        self.grid_structure = [[Cell() for i in range(self.grid_scale)] for j in range(self.grid_scale)] # martiz de objetos Cell.
        self.mines_proportion = 0.20
        self.mines_pos_list = [] # Position of all the mines.
        self.total_safe_cells = int
        self.displacements = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] # Displacements to the 8 adjacent Cell.
        self.set_mines()
        self.calculate_mines()

    def set_mines(self):
        mine = round((self.grid_scale ** 2) * self.mines_proportion)
        total_mines = 0

        while total_mines < mine:
            x = random.randint(0, self.grid_scale - 1)
            y = random.randint(0, self.grid_scale - 1)
            if not self.grid_structure[x][y].has_mine:
                self.mines_pos_list.append((x, y))
                self.grid_structure[x][y].has_mine = True
                total_mines += 1
        self.total_safe_cells = (self.grid_scale ** 2) - total_mines

    def adjacent_cells(self, row, column):
        adjacente_cell = []
        adjacent_cells_coords = []
        for displac_row, displac_column in self.displacements:
            new_row, new_column = row + displac_row, column + displac_column
            # Within limits.
            if 0 <= new_row < len(self.grid_structure) and 0 <= new_column < len(self.grid_structure[0]):
                adjacente_cell.append(self.grid_structure[new_row][new_column])
                adjacent_cells_coords.append((new_row, new_column))
        return adjacente_cell, adjacent_cells_coords
    
    def calculate_mines(self):
        for row in range(self.grid_scale):
            for col in range(self.grid_scale):
                cells_list, cell_coords = self.adjacent_cells(row, col)
                cont = sum(cell.has_mine for cell in cells_list)
                self.grid_structure[row][col].surrounding_mines = cont

class Cell:
    def __init__(self):
        self.has_mine = False # Has mine.
        self.revealed = False # Cell is visible.
        self.flag_marked = False # Was marked.
        self.surrounding_mines = int # Number of djacent mines.

class GameLogic:# :ogic.
    def __init__(self, board: Board):
        self.board = board
        self.revealed_safe_mines_left = self.board.total_safe_cells
        self.game_won = False
        self.game_lost = False

    def set_mark(self): 
    #set_mark(self, x, y): for GUI imput.
        try: # Check case for (0, 0).
            x = int(input("X: ")) - 1
            y = int(input("y: ")) - 1
            return self.board.grid_structure[x][y], (x, y)
        except (IndexError, ValueError):
            print("Invalid input or out of range.")
            return None, None

    def auto_reveal(self, cell: Cell, coord): # Until a Cell have at least one adjacent mine.
        if cell is None or coord is None:
            return
        row, col = coord

        if cell.has_mine:
            self.game_lost = True
            return

        if not cell.revealed:
            cell.revealed = True
            if not cell.has_mine:
                self.revealed_safe_mines_left -= 1

            if cell.surrounding_mines == 0:
                cells_list, coords_list = self.board.adjacent_cells(row, col)
                for nei_cell, nei_coord in zip(cells_list, coords_list):
                    self.auto_reveal(nei_cell, nei_coord)

    def win_check(self):
        if self.revealed_safe_mines_left == 0:
            self.game_won = True

class Game_:
    def __init__(self):
        self.dim = 7
        self.board = Board(self.dim)
        self.logic = GameLogic(self.board)

    def loop(self):
        self.temporal_show()
        while not self.logic.game_won and not self.logic.game_lost:
                cell, coord = self.logic.set_mark()
                self.logic.auto_reveal(cell, coord)
                print("\033c", end = "")
                self.logic.win_check()
                self.temporal_show()
                if self.logic.game_won:
                    print("Won!")
                    return
                if self.logic.game_lost:
                    print("Lost")
                    return

    def temporal_show(self):
        for i in range(self.dim):
            fila = []
            for j in range(self.dim):
                if self.board.grid_structure[i][j].has_mine:
                    fila.append("▢")
                elif not self.board.grid_structure[i][j].has_mine and self.board.grid_structure[i][j].revealed:
                    fila.append(str(self.board.grid_structure[i][j].surrounding_mines)) # revelada.
                else:
                    fila.append("▢")
            print(" ".join(fila))

class Game(ShowBase):
    def __init__(self):
        super().__init__()

        self.dim = 15
        self.margin = 0.1
        self.board = Board(self.dim)
        self.logic = GameLogic(self.board)

        self.grid = self.create_grid(self.dim, self.margin)
        self.grid.reparentTo(self.render2d)
        self.accept("s", self.userExit)

    def create_grid(self, divisions, margin):
        lines = LineSegs()
        lines.setThickness(1.5)
        lines.setColor(0, 0, 0, 1)

        aspect = self.getAspectRatio()

        left = -aspect
        right = aspect
        bottom = -1
        top = 1

        width = right - left
        height = top - bottom

        left += width * margin
        right -= width * margin
        bottom += height * margin
        top -= height * margin

        step_x = (right - left) / divisions
        step_z = (top - bottom) / divisions

        # líneas verticales
        for i in range(divisions + 1):
            x = left + i * step_x
            lines.moveTo(x, 0, bottom)
            lines.drawTo(x, 0, top)

        # líneas horizontales
        for i in range(divisions + 1):
            z = bottom + i * step_z
            lines.moveTo(left, 0, z)
            lines.drawTo(right, 0, z)

        node = lines.create()
        return NodePath(node)
        
game = Game()
game.run()