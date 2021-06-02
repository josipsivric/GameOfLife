#!/usr/bin/env python
import copy
import tkinter as tk
from tkinter import messagebox

from GameOfLife.Logic import board_generation

ALIVE = 1
DEAD = 0
number_columns = 50
number_rows = 50


# TODO
# - Should use sparse matrix instead of 2D list - more efficient
# - Update single element instead whole board
# - Add more functionality etc.

class GameOfLife:
    board_states = []

    def __init__(self):
        self.root = tk.Tk()

        self.gen = tk.StringVar()
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.control_frame = tk.LabelFrame(self.root, text="Controls")
        self.control_frame.grid(row=0, column=0, padx=10, pady=5, sticky="N")
        self.canvas_frame = tk.LabelFrame(self.root, text="Board")
        self.canvas_frame.grid(row=0, column=2, padx=5, pady=5, sticky="N")

        self.board = [[DEAD] * number_rows for _ in range(number_columns)]
        self.remember_state(self.board)

        self.canvas = tk.Canvas(self.canvas_frame, width=len(self.board) * 12, height=len(self.board[0]) * 12)
        self.draw(self.board)

        self.empty_button = tk.Button(self.control_frame, text="Empty board",
                                      width=18, command=lambda: self.clear_board(self.board))
        self.empty_button.grid(row=0, column=0, padx=5, pady=5)

        self.full_button = tk.Button(self.control_frame, text="Full board",
                                     width=18, command=lambda: self.fill_board(self.board))
        self.full_button.grid(row=0, column=1, padx=5, pady=5)

        self.percent = 0
        self.percentage_var = tk.StringVar()
        self.percentage_var.trace_add("write", self.limit_input_per)
        self.enter_percent = tk.Entry(self.control_frame, width=3, textvariable=self.percentage_var)
        self.enter_percent.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.label_percent = tk.Label(self.control_frame, text="% chance to be alive")
        self.label_percent.grid(row=1, column=0, padx=(27, 0), sticky="W")

        self.random_percent_button = tk.Button(self.control_frame, text="Randomize", width=18,
                                               command=self.randomize_chance_call)
        self.random_percent_button.grid(row=2, column=0, padx=5, pady=5)

        self.number = 0
        self.number_var = tk.StringVar()
        self.number_var.trace_add("write", self.limit_input_num)
        self.enter_number = tk.Entry(self.control_frame, width=5, textvariable=self.number_var)
        self.enter_number.grid(row=1, column=1, padx=5, pady=5, sticky="W")
        self.label_number = tk.Label(self.control_frame, text="cells alive")
        self.label_number.grid(row=1, column=1, padx=(43, 0), sticky="W")

        self.random_num_button = tk.Button(self.control_frame, text="Randomize", width=18,
                                           command=self.randomize_fixed_call)
        self.random_num_button.grid(row=2, column=1, padx=5, pady=5)

        self.play_button = tk.Button(self.control_frame, text="Start", width=39, command=self.play)
        self.play_button.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

        self.gen_label = tk.Label(self.control_frame, textvariable=self.gen)
        self.gen_label.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        self.root.mainloop()

    def remember_state(self, board):
        """ Adds current state of the board to the list for later use. List accepts 50 boards.
        In case of more, delete the oldest and save.

        :param board: board to be saved
        :return: None
        """
        if len(self.board_states) > 50:
            self.board_states.pop(0)
            self.board_states.append(copy.deepcopy(board))
        else:
            self.board_states.append(copy.deepcopy(board))

    def limit_input_per(self, *args):
        """ Verify input of percent field.

        :param args:
        :return: None
        """
        value = self.percentage_var.get()
        if len(value) > 0:
            try:
                value_int = int(value)
                if 0 < int(value) > 100:
                    messagebox.showwarning("Invalid input", "Percentage must be a number between 0 and 100!")
                    self.percentage_var.set("0")
                else:
                    self.percent = value_int
            except ValueError:
                messagebox.showwarning("Invalid input", "Percentage must be a number between 0 and 100!")
                self.percentage_var.set("0")

    def limit_input_num(self, *args):
        value = self.number_var.get()
        if len(value) > 0:
            try:
                value_int = int(value)
                if 0 < int(value) > 100000:
                    messagebox.showwarning("Invalid input", "Number must be between 0 and 100000!")
                    self.number_var.set("0")
                else:
                    self.number = value_int
            except ValueError:
                messagebox.showwarning("Invalid input", "Number must be between 0 and 100000!")
                self.number_var.set("0")

    def randomize_board_select(self, board, select, num):
        if select == 0:
            new_b = board_generation.randomize_board_chance(board, num)
            return new_b
        else:
            new_b = board_generation.randomize_board_fixed(board, num)
            return new_b

    def randomize_chance_call(self):
        new_b = self.randomize_board_select(self.board, 0, self.percent)
        self.remember_state(new_b)
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.canvas.delete("all")
        self.canvas.update()
        self.canvas.after(1, self.draw(new_b))
        return new_b

    def randomize_fixed_call(self):
        new_b = self.randomize_board_select(self.board, 1, self.number)
        self.remember_state(new_b)
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.canvas.delete("all")
        self.canvas.update()
        self.canvas.after(1, self.draw(new_b))
        return new_b

    def clear_board(self, board):
        new_b = board_generation.empty_board(board)
        self.remember_state(new_b)
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.canvas.delete("all")
        self.canvas.update()
        self.canvas.after(1, self.draw(new_b))

    def fill_board(self, board):
        new_b = board_generation.full_board(board)
        self.remember_state(new_b)
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.canvas.delete("all")
        self.canvas.update()
        self.canvas.after(1, self.draw(new_b))

    def draw(self, board):
        self.canvas.delete("all")
        self.canvas.update()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == ALIVE:
                    self.cell_alive(i, j)
                else:
                    self.cell_dead(i, j)

    def cell_alive(self, row, column):
        self.canvas.create_rectangle(1 + (column * 12), 1 + (row * 12), 11 + (column * 12), 11 + (row * 12),
                                     fill="black", width=0)
        self.canvas.grid(padx=(8, 5), pady=5)

    def cell_dead(self, row, column):
        self.canvas.create_rectangle(1 + (column * 12), 1 + (row * 12), 11 + (column * 12), 11 + (row * 12),
                                     fill=None, width=0)
        self.canvas.grid(padx=(8, 5), pady=5)

    def play(self):
        new_b = board_generation.next_board(self.board_states[len(self.board_states) - 1])
        self.remember_state(new_b)
        self.generation += 1
        self.gen.set("Generation: " + str(self.generation))
        self.draw(new_b)


if __name__ == '__main__':
    app = GameOfLife()
