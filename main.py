import tkinter as tk
from tkinter import *
from tkinter import ttk
import random

class Program:
    def __init__(self, root) -> None:
        self.root = root

        width = 20
        height = 20
        num_of_mines = 10

        minefield = MineField(width, height, num_of_mines, root)

class Field:
    """
    The parent class of the clickable buttons on the screen.
    """

    def __init__(self, where, r, c) -> None:
        self.flaged = False
        self.revealed = False

        self.tk_button = Button(where, bg="grey")
        self.tk_button.config(command = lambda: self.onClick())

        # note: there is probably a better way to do this
        def flag(event) -> None:
            if not self.revealed:
                if (self.flaged):
                    self.flaged = False
                    self.tk_button.config(background="grey")
                else:
                    self.flaged = True
                    self.tk_button.config(background="green")

        self.tk_button.bind('<Button-3>', flag)

        self.tk_button.grid(row = r, column= c, sticky = "NSEW")

    def onClick(self) -> None:
        pass

class EmptyField(Field):
    """
    The field, which borders no mines.
    """

    def onClick(self) -> None:
        self.revealed = True
        if not self.flaged:
            self.tk_button.config(background="white", disabledforeground="black")

class Mine(Field):
    """
    The field containing a mine.
    """

    def onClick(self) -> None:
        self.revealed = True
        if not self.flaged:
            self.tk_button.config(background="black", disabledforeground="black")
        
class NumberField(Field):
    """
    The field containing the number of mines it borders.
    """    

    def __init__(self, where, r, c, num_of_mines) -> None:
        self.num_of_mines = num_of_mines
        self.flaged = False
        self.revealed = False

        self.tk_button = Button(where, bg="grey")
        self.tk_button.config(command = lambda: self.onClick())

        # note: there is probably a better way to do this
        def flag(event) -> None:
            if not self.revealed:
                if (self.flaged):
                    self.flaged = False
                else:
                    self.flaged = True
                self.tk_button.config(background="green")

        self.tk_button.bind('<Button-3>', flag)

        self.tk_button.grid(row = r, column= c, sticky = "NSEW")


    def onClick(self) -> None:
        self.revealed = True
        if not self.flaged:
            self.tk_button.config(background="white", text = str(self.num_of_mines), disabledforeground="black")


class MineField:
    """
    The "minefield" containing the buttons of the game.
    """

    def __init__(self, width, height, num_of_mines, root) -> None:
        self.width: int = width
        self.height: int = height
        self.num_of_mines: int = num_of_mines

        self.minefield = [list() for row in range(0, height)]

        for row in range(0, height):
            for column in range(0, width):
                self.minefield[row].append(0)

        self.lay_down_mines()
        self.config_widgets(root)

    def lay_down_mines(self) -> None:
        # put the mines in random positions

        for iter in range(0, self.num_of_mines):
            x: int = random.randint(0, self.width - 1)
            y: int = random.randint(0, self.height - 1)

            while (self.minefield[x][y] == -1):
                x: int = random.randint(0, self.width - 1)
                y: int = random.randint(0, self.height - 1)

            self.minefield[x][y] = -1

        def mine_there(row, column) -> int:
            if (self.minefield[row][column] == -1):
                return 1
            return 0
        

        # mark the other fields with numbers
        for x in range(0, self.height):
            for y in range(0, self.width):
                if (self.minefield[x][y] != -1):
                    num_of_bordering_mines = 0

                    # x x x
                    # o c o
                    # o o o
                    # x: inspected fields, o: other fields, c: current field
                    if (x > 0):
                        num_of_bordering_mines += mine_there(x - 1, y)

                        if (y > 0):
                            num_of_bordering_mines += mine_there(x - 1, y - 1)

                        if (y < self.width - 1):
                            num_of_bordering_mines += mine_there(x - 1, y + 1)

                    # o o o
                    # o c o
                    # x x x
                    if (x < self.height - 1):
                        num_of_bordering_mines += mine_there(x + 1, y)

                        if (y > 0):
                            num_of_bordering_mines += mine_there(x + 1, y - 1)

                        if (y < self.width - 1):
                            num_of_bordering_mines += mine_there(x + 1, y + 1)

                    # o o o
                    # x c x
                    # o o o
                    if (y > 0):
                        num_of_bordering_mines += mine_there(x, y - 1)

                    if (y < self.width - 1):
                        num_of_bordering_mines += mine_there(x, y + 1)

                    self.minefield[x][y] = num_of_bordering_mines

        for x in range(0, self.height):
            for y in range(0, self.width):
                print(self.minefield[x][y], end="")
            print()

    def config_widgets(self, root) -> None:
        self.frame = Frame(root, height= self.width * 20, width = self.height * 20)

        self.frame.grid(padx = 0, pady = 0)
        self.frame.columnconfigure(0, weight = 1)
        self.frame.rowconfigure(0, weight = 1)
        self.frame.grid_propagate(False)

        for x in range(0, self.height):
            for y in range(0, self.width):
                self.frame.columnconfigure(x, weight = 1)
                self.frame.rowconfigure(y, weight = 1)

                if (self.minefield[x][y] == -1):
                    Mine(self.frame, x, y)
                elif (self.minefield[x][y] == 0):
                    EmptyField(self.frame, x, y)
                else:
                    NumberField(self.frame, x, y, self.minefield[x][y])



if __name__ == '__main__':
    root = Tk()
    root.geometry("500x500")
    root.title("Minesweeper")
    root.resizable(False, False)
    game = Program(root)
    root.mainloop()