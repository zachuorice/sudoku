# Sudoku board code, and Sudoku board generation code.
import random
import time
from tkinter import *
from tkinter.constants import *

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

def rgb(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class SudokuGUI(Frame):
    board_generators = {"SudoGen v1 (Very Easy)":sudogen_1}
    board_generator = sudogen_1

    def new_game(self):
        self.ng.pack_forget()

    def load_game(self):
        self.lg.pack_forget()

    def save_game(self):
        self.sg.pack_forget()

    def query_board(self):
        self.setting = False
        window = Toplevel()
        window.title("Choose Board Algorithm")

        scroll = Scrollbar(window)
        scroll.pack(side='right', fill='y')

        listbox = Listbox(window, yscrollcommand=scroll.set) 

        scroll.config(command=listbox.yview)

        bframe = Frame(window)

        for s in self.board_generators.keys():
            listbox.insert(-1, s)

        def do_ok():
            self.board_generator = self.board_generators[listbox.get(ACTIVE)]
            window.destroy()

        def do_cancel():
            window.destroy()


        cancel = Button(bframe, command=do_cancel, text="Cancel")
        cancel.pack(side='right', fill='x')

        ok = Button(bframe, command=do_ok, text="Ok")
        ok.pack(side='right', fill='x')

        listbox.pack(side='top', fill='both', expand='1')
        bframe.pack(side='top', fill='x', expand='1')

        window.mainloop()

    def make_grid(self):
        c = Canvas(self, bg=rgb(255,255,255), width='512', height='512')
        c.pack(side='top', fill='both', expand='1')
        # TODO
        self.canvas = c

    def __init__(self, master, board):
        Frame.__init__(self, master)

        if master:
            master.title("SudokuGUI")

        self.board = board

        bframe = Frame(self)

        self.ng = Button(bframe, command=self.new_game, text="New Game")
        self.ng.pack(side='left', fill='x')

        self.lg = Button(bframe, command=self.load_game, text="Load Game")
        self.lg.pack(side='left', fill='x')

        self.sg = Button(bframe, command=self.save_game, text="Save Game")
        self.sg.pack(side='left', fill='x')

        self.query = Button(bframe, command=self.query_board, text="Set Board Algorithm")
        self.query.pack(side='left', fill='x')

        bframe.pack(side='bottom', fill='x', expand='1')

        self.make_grid()

        self.pack()

if __name__ == '__main__':
    board = SudokuBoard()
    tk = Tk()
    gui = SudokuGUI(tk, board)
    gui.mainloop()
