#!/usr/bin/python
# Sudoku board code, and Sudoku board generation code.
# TODO:
# - Sudoku Solver
# - GUI Load/Save game (DONE)
# - GUI Board Drawing (DONE)
# - GUI Board Sync (DONE)
# - GUI Board Interaction (DONE)
# - GUI End Game Mode
# - Reimplment SudokuBoard more efficently and with less complexity
import random
import time
import os
import tkinter.tix
import pickle
from tkinter import *
from tkinter.constants import *
from tkinter.tix import FileSelectBox, Tk

random.seed(time.time())


# There are probably a few bugs in this class, and it could be implemented 
# better I think.
# ReDesign Stuff:
# Don't integrate game rule error checks in set(), instead create valid()
# and is_game_complete() functions to handle this, but allow users to mess
# up the board however they like.

class Board:
    """
    Data structure representing the board of a Sudoku game.
    """


    #@property
    #def grid(self):
    #    grid = [[0 for x in range(9)] for y in range(9)]
    #    for y in range(9):
    #        for x in range(9):
    #            grid[y][x] = self.get(x, y)
    #    return grid

    def __init__(self):
        self.clear()

    def clear(self):
        """
        Empty the board.
        """
        self.board = [0 for i in range(9*9)]
        self.locked = []

    def is_valid(self, col, row):
        v = self.get(col, row)
        region = self.get_nearest_region(col, row)
        cols = self.get_cols(col)
        row_list = self.get_row(row)
        if cols.count(v) > 1 or row_list.count(v) > 1 or region.count(v) > 1:
            return False
        return True

    def valid(self):
        return False

    def is_game_over(self):
        if self.valid() and not 0 in self.board:
            return True
        return False

    def col_row_to_index(self, col, row):
        if col < 0 or col >= 9 or row < 0 or row >= 9:
            raise IndexError("Column or row out of bounds.")
        i = (row*9) + col
        return i

    def set(self, col, row, v, lock=False):
        if v < 0 or v > 9:
            raise ValueError("Value must be within range 1-9.")
        i = self.col_row_to_index(col, row)

        if i in self.locked:
            return
        else:
            self.board[i] = v

        if lock:
            self.locked.append(i)

    def get_row(self, row):
        i = self.col_row_to_index(0, row)
        return self.board[i:i+9]

    def get_cols(self, col):
        cols = []
        for row in range(9):
            i = self.col_row_to_index(col, row)
            cols.append(self.board[i])
        return cols

    def get_nearest_region(self, col, row):
        if row < 3:
            row = 0
        else:
            row = (row - (row%3))

        if col < 3:
            col = 0
        else:
            col = (col - (col%3)) // 3
        return self.get_region(row+col)

    def get_region(self, region):
        """
        region is a number between 0-8 with 0 being top-leftmost 
        region and 8 being the bottom-rightmost region.
        """
        if region < 0 or region > 8:
            raise IndexError("region out of bounds")
        (row,col) = (0,0)
        if region <= 2:
            col = region * 3
        else:
            row = (region // 3) * 3
            col = (region % 3) * 3
        region = []
        for y in range(row, row+3):
            for x in range(col, col+3):
                region.append(self.get(x, y))
        return region

    def get(self, col, row):
        return self.board[self.col_row_to_index(col, row)]

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
                board.set(random.randint(x, x+2), random.randint(y, y+2), i, lock=True)
            except ValueError:
                print("Board rule violation, this shouldn't happen!")
            added.append(i)

def rgb(red, green, blue):
    """
    Make a tkinter compatible RGB color.
    """
    return "#%02x%02x%02x" % (red, green, blue)

class GUI(Frame):
    board_generators = {"Empty":lambda b:None,
                        "SudoGen v1 (Very Easy)":sudogen_1}
    board_generator = staticmethod(sudogen_1)

    def new_game(self):
        self.board.clear()
        self.board_generator(self.board)
        self.sync_board_and_canvas()

    def make_modal_window(self, title):
        window = Toplevel()
        window.title(title)
        window.attributes('-topmost', True)
        window.grab_set()
        window.focus_force()
        return window
 
    def load_game(self):
        def _load_game(filename):
            with open(filename, 'rb') as f:
                board = pickle.load(f)
                if not isinstance(board, SudokuBoard):
                    # TODO: Report bad file
                    return
                self.board = board
            self.sync_board_and_canvas()
            window.destroy()
        window = self.make_modal_window("Load Game")
        fbox = FileSelectBox(window, command=_load_game)
        fbox.pack()
        window.mainloop()

    def save_game(self):
        def _save_game(filename):
            with open(filename, 'wb') as f:
                pickle.dump(self.board, f, protocol=2)
            window.destroy()
        window = self.make_modal_window("Save Game")
        fbox = FileSelectBox(window, command=_save_game)
        fbox.pack()
        window.mainloop()

    def query_board(self):
        window = self.make_modal_window("Set Board Algorithm")

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
        c = Canvas(self, bg=rgb(128,128,128), width='512', height='512')
        c.pack(side='top', fill='both', expand='1')

        self.rects = [[None for x in range(9)] for y in range(9)]
        self.handles = [[None for x in range(9)] for y in range(9)]
        rsize = 512/9
        guidesize = 512/3

        for y in range(9):
            for x in range(9):
                (xr, yr) = (x*guidesize, y*guidesize)
                self.rects[y][x] = c.create_rectangle(xr, yr, xr+guidesize, 
                                                      yr+guidesize, width=3)
                (xr, yr) = (x*rsize, y*rsize)
                r = c.create_rectangle(xr, yr, xr+rsize, yr+rsize)
                t = c.create_text(xr+rsize/2, yr+rsize/2, text="SUDO",
                                  font="System 15 bold")
                self.handles[y][x] = (r, t)

        self.canvas = c
        self.sync_board_and_canvas()

    def sync_board_and_canvas(self):
        for y in range(9):
            for x in range(9):
                text = ''
                color = rgb(0,0,0)
                i = self.board.get(x, y)
                if i != 0:
                    text=str(i)
                if not self.board.is_valid(x,y):
                    color = rgb(128,0,0)
                self.canvas.itemconfig(self.handles[y][x][1], text=text, fill=color)

    def canvas_click(self, event):
        self.canvas.focus_set()
        rsize = 512 // 9
        (x,y) = (0, 0)
        if event.x > rsize:
            x = event.x // rsize
        if event.y > rsize:
            y = event.y // rsize
        self.current = (x,y)

    def canvas_key(self, event):
        if event.char.isdigit() and int(event.char) > 0 and self.current:
            (x,y) = self.current
            self.board.set(x, y, int(event.char))
            self.sync_board_and_canvas()
            self.current = None

    def __init__(self, master, board):
        Frame.__init__(self, master)

        if master:
            master.title("SudokuGUI")

        self.board = board
        self.board_generator(board)
        bframe = Frame(self)

        self.ng = Button(bframe, command=self.new_game, text="New Game")
        self.ng.pack(side='left', fill='x', expand='1')

        self.sg = Button(bframe, command=self.save_game, text="Save Game")
        self.sg.pack(side='left', fill='x', expand='1')

        self.lg = Button(bframe, command=self.load_game, text="Load Game")
        self.lg.pack(side='left', fill='x', expand='1')

        self.query = Button(bframe, command=self.query_board, text="Set Board Algorithm")
        self.query.pack(side='left', fill='x', expand='1')

        bframe.pack(side='bottom', fill='x', expand='1')
        self.make_grid()
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Key>", self.canvas_key)
        self.current = None
        self.pack()

if __name__ == '__main__':
    board = Board()
    tk = Tk()
    gui = GUI(tk, board)
    gui.mainloop()
