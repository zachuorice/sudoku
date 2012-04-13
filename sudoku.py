# Sudoku board code, and Sudoku board generation code.
import random
import time

random.seed(time.time())


class SudokuBoard:


    def __init__(self):
        self.clear()

    def clear(self):
        self.grid = [[0 for x in range(9)] for y in range(9)]

    def get_row(self, row):
        return self.grid[row]

    def get_cols(self, col):
        return [y[col] for y in self.grid]

    def get_nearest_region(self, col, row):
        """
        Regions are 3x3 sections of the grid
        """
        def make_index(v):
            if v <= 2:
                return 0
            elif v <= 5:
                return 3
            else:
                return 6
        return [y[make_index(col):make_index(col)+3] for y in 
                self.grid[make_index(row):make_index(row)+3]]

    def set(self, col, row, v):
        if v == self.grid[row][col]:
            return
        for v2 in self.get_row(row):
            if v == v2:
                raise ValueError()
        for v2 in self.get_cols(col):
            if v == v2:
                raise ValueError()
        for y in self.get_nearest_region(col, row):
            for x in y:
                if v == x:
                    raise ValueError()
        self.grid[row][col] = v

    def get(self, col, row):
        return self.grid[row][col]

    def __str__(self):
        strings = []
        newline_counter = 0
        for y in self.grid:
                strings.append("%d%d%d %d%d%d %d%d%d" % tuple(y))
                newline_counter += 1
                if newline_counter == 3:
                    strings.append('')
                    newline_counter = 0
        return '\n'.join(strings)

def sudogen_1(board):
    """
    Algorithm:
        Add a random number between 1-9 to each subgrid in the 
        board, do not add duplicate random numbers.
    """
    board.clear()
    added = [0]
    for y in range(0, 9, 3):
        for x in range(0, 9, 3):
            if len(added) == 10:
                return
            i = 0
            while i in added:
                i = random.randint(1, 9)
            try:
                board.set(random.randint(x, x+2), random.randint(y, y+2), i)
            except ValueError:
                print("Board rule violation, this shouldn't happen!")
            added.append(i)

if __name__ == '__main__':
    def wrapped_print(*args, **kwargs):
        print("-----------------------")
        print(*args, **kwargs)
        print("-----------------------")

    board = SudokuBoard()
    wrapped_print(board)

    sudogen_1(board)
    wrapped_print(board)
