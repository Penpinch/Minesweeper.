import random

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
        for i in range(mine):
            x = random.randint(1, self.grid_scale) - 1
            y = random.randint(1, self.grid_scale) - 1
            if self.grid_structure[x][y].has_mine == False:
                self.mines_pos_list.append((x, y))
                self.grid_structure[x][y].has_mine = True
                total_mines += 1
            else:
                i -= 1
        self.total_safe_cells = (self.grid_scale ** 2) - total_mines

    def adjacent_cells(self, row, column):
        adjacente_cell = []
        for displac_row, displac_column in self.displacements:
            new_row, new_column = row + displac_row, column + displac_column
            # Within limits.
            if 0 <= new_row < len(self.grid_structure) and 0 <= new_column < len(self.grid_structure[0]):
                adjacente_cell.append(self.grid_structure[new_row][new_column])
        return adjacente_cell
    
    def calculate_mines(self):
        for row in range(self.grid_scale):
            for col in range(self.grid_scale):
                cells_list:list[Cell] = self.adjacent_cells(row, col)
                cont = sum(cell.has_mine for cell in cells_list)
                self.grid_structure[row][col].surrounding_mines = cont

class Cell:
    def __init__(self):
        self.has_mine = False # tiene mina.
        self.revealed = False # la Cell es visible.
        self.flag_marked = False # fue marcada.
        self.surrounding_mines = int # mians al rededor.

class GameLogic:# logic
    def __init__(self, board: Board):
        # que pasa al revelarse una Cell.
        # revelar celdas vacias automaticamente.
        self.board = board
        self.revealed_safe_mines_left = self.board.total_safe_cells
        self.game_won = False
        self.game_lost = False

    def set_mark(self): 
    #set_mark(self, x, y): for GUI imput.
        try: # Check case for (0, 0).
            x = int(input("X: ")) - 1
            y = int(input("y: ")) - 1

            if self.board.grid_structure[x][y].has_mine == False:
                self.board.grid_structure[x][y].revealed = True
                self.revealed_safe_mines_left -= 1
            else:
                self.game_lost = True
        except IndexError:
            print("Out of range.")

    def auto_reveal(self): pass # for cells adjacent without mines.

    def win_check(self):
        if self.revealed_safe_mines_left == 0:
            self.game_won = True

class Game:
    def __init__(self):
        self.dim = 10
        self.board = Board(self.dim)
        self.logic = GameLogic(self.board)

    def loop(self):
        self.temporal_show()
        while self.logic.game_won == False and self.logic.game_lost == False:
                self.logic.set_mark()
                self.temporal_show()
                self.logic.win_check()
                if self.logic.game_won == True:
                    print("Won!")
                    return
                if self.logic.game_lost == True:
                    print("Lost")
                    return

    def temporal_show(self):
        for i in range(self.dim):
            fila = []
            for j in range(self.dim):
                if self.board.grid_structure[i][j].has_mine:
                    fila.append("x")
                elif self.board.grid_structure[i][j].has_mine == False and self.board.grid_structure[i][j].revealed == True:
                    fila.append(str(self.board.grid_structure[i][j].surrounding_mines)) # revelada.
                else:
                    fila.append("▢")
            print(" ".join(fila))

game = Game()
game.loop()