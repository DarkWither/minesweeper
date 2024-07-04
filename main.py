# Minesweeper
# Beta version
# Made by Attila Ladányi
# 2024.07.

import tkinter as tk
from tkinter import *
import random

class Program:
    def __init__(self, root) -> None:
        self.root = root

        width = 20
        height = 20
        num_of_mines = 10

        root.geometry(f"{width * 20}x{height * 20}")
        root.title("Minesweeper")
        root.resizable(False, False)
        root.iconbitmap('logo.ico')

        canvas = Canvas(self.root, width = width * 20, height = height * 20, bg="red")
        canvas.pack()

        minefield = MineField(width, height, num_of_mines, canvas)

        def click(event) -> None:
            minefield.onClick(event.x, event.y)
            
            if minefield.lost:
                self.lose()

            if minefield.won_game():
                self.win()


        def rightClick(event) -> None:
            minefield.flag(event.x, event.y)

        canvas.bind('<Button-1>', click)
        canvas.bind('<Button-3>', rightClick)

    def win(self) -> None:
        print("You won!")

    def lose(self):
        print("You lost!")

class MineField:
    """
    The minefield containing the "buttons" of the game.
    """

    def __init__(self, width, height, num_of_mines, canvas) -> None:
        self.width: int = width
        self.height: int = height
        self.num_of_mines: int = num_of_mines

        self.canvas = canvas

        self.lost = False

        self.minefield = [list() for row in range(0, height)]
        self.revealed_fields = [list() for row in range(0, height)]
        self.flaged_fields = [list() for row in range(0, height)]

        for row in range(0, height):
            for column in range(0, width):
                self.minefield[row].append(0)
                self.revealed_fields[row].append(False)
                self.flaged_fields[row].append(False)

        self.lay_down_mines()
        self.draw_minefield(root)

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
                    self.minefield[x][y] = self.num_of_bordering_mines(x, y)


    def num_of_bordering_mines(self, row, column) -> int:
        num = 0
        
        for i in range(max(0, row - 1), min(self.height, row + 2)):
            for j in range(max(0, column - 1), min(self.width, column + 2)):
                
                if (i == row and j == column):
                    continue
                
                if self.minefield[i][j] == -1:
                    num += 1
                    
        return num

    def draw_minefield(self, root) -> None:
        for x in range(self.width):
            for y in range(self.height):
                h_x, h_y = x * 20, y * 20
                self.canvas.create_rectangle(h_x , h_y, h_x + 20, h_y + 20, fill = "grey", outline="black")

    def reveal_field(self, row, column) -> None:
        self.revealed_fields[row][column] = True

        if (self.minefield[row][column] == -1):
            self.canvas.create_rectangle(row * 20, column * 20, row * 20 + 20, column * 20 + 20, fill="black", outline="black")
        elif (self.minefield[row][column] == 0):
            self.canvas.create_rectangle(row * 20, column * 20, row * 20 + 20, column * 20 + 20, fill="white", outline="black")
        else:
            self.canvas.create_rectangle(row * 20, column * 20, row * 20 + 20, column * 20 + 20, fill="white", outline="black")
            self.canvas.create_text((row * 20) + 10, column * 20 + 10, text=f"{self.minefield[row][column]}", fill="black")

    def reveal_all(self) -> None:
        for x in range(0, self.height):
            for y in range(0, self.width):
                self.reveal_field(y, x)                

    def reveal_neighbours(self, row, column) -> None:
        for x in range(max(0, row-1), min(self.width, row+2)):
            for y in range(max(0, column-1), min(self.height, column+2)):
                if (x == row and y == column):
                    continue
                else:
                    if not (self.revealed_fields[x][y]):
                        self.reveal_field(x, y)
                        if self.minefield[x][y] == 0:
                            # recursion
                            self.reveal_neighbours(x, y)

    def onClick(self, x, y) -> None:
            row = x // 20
            column = y // 20

            if not self.flaged_fields[row][column]:
                # if clicked on mine:
                if (self.minefield[row][column] == -1):
                    self.reveal_all()
                    self.lost = True
                elif (self.minefield[row][column] == 0):
                    self.reveal_neighbours(row, column)
                else:
                    self.reveal_field(row, column)

    def flag(self, x: int, y: int) -> None:
        row: int = (x // 20)
        column: int = (y // 20)

        if not self.revealed_fields[row][column]:
            if self.flaged_fields[row][column]:
                self.flaged_fields[row][column] = False
                self.canvas.create_rectangle(row * 20, column * 20, row * 20 + 20, column * 20 + 20, fill = "grey", outline="black")
            else:
                self.flaged_fields[row][column] = True
                self.canvas.create_rectangle(row * 20, column * 20, row * 20 + 20, column * 20 + 20, fill = "green", outline="black")

    def won_game(self) -> bool:
        num_of_revealed = 0

        for row in self.revealed_fields:
            for bool in row:
                if bool:
                    num_of_revealed += 1

        if (self.width * self.height - self.num_of_mines == num_of_revealed):
            return True
        
        return False

if __name__ == '__main__':
    root = Tk()
    game = Program(root)
    root.mainloop()