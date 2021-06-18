#!/usr/bin/env python
import copy
import tkinter as tk
from tkinter import messagebox

from Logic import board_generation

ALIVE = 1
DEAD = 0
number_columns = 50
number_rows = 50


class GameOfLife:
    boards_back_stack = []
    boards_forward_stack = []
    _stop = 0
    board = [[DEAD] * number_rows for _ in range(number_columns)]

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Of Life")
        self.root.resizable(False, False)

        self.control_frame = tk.LabelFrame(self.root, text="Controls")
        self.control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="N")
        self.canvas_frame = tk.LabelFrame(self.root, text="Board")
        self.canvas_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="NE")

        self.canvas = tk.Canvas(self.canvas_frame, width=len(self.board) * 12, height=len(self.board[0]) * 12,
                                highlightthickness=0, borderwidth=0)

        self.push_to_back_stack(self.board)
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

        self.back_button = tk.Button(self.control_frame, text="<<", command=self.back)
        self.back_button.grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.play_button = tk.Button(self.control_frame, text="Start", width=28, command=self.start)
        self.play_button.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.forward_button = tk.Button(self.control_frame, text=">>", command=self.forward)
        self.forward_button.grid(row=3, column=1, padx=5, pady=5, sticky="E")

        self.gen = tk.StringVar()
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.gen_label = tk.Label(self.control_frame, textvariable=self.gen)
        self.gen_label.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        self.root.mainloop()

    def push_to_back_stack(self, board):
        """ Adds current state of the board to the list for later use. List accepts 50 boards.
        In case of more, delete the oldest and save.

        :param board: board to be saved
        :return: None
        """
        if len(self.boards_back_stack) > 50:
            self.boards_back_stack.pop(0)
            self.boards_back_stack.append(copy.deepcopy(board))
        else:
            self.boards_back_stack.append(copy.deepcopy(board))

    def push_to_forward_stack(self, board):
        """ Adds current state of the board to the list for later use.

        :param board: board to be saved
        :return: None
        """
        self.boards_forward_stack.append(copy.deepcopy(board))

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
        """ Verify input of fixed number of alive cells field.

        :param args:
        :return: None
        """
        value = self.number_var.get()
        if len(value) > 0:
            try:
                value_int = int(value)
                if 0 < int(value) > number_columns * number_rows:
                    messagebox.showwarning("Invalid input", "Number must be between 0 and " +
                                           str(number_columns * number_rows) + "!")
                    self.number_var.set("0")
                else:
                    self.number = value_int
            except ValueError:
                messagebox.showwarning("Invalid input", "Number must be between 0 and 100000!")
                self.number_var.set("0")

    def randomize_board_select(self, board, select, num):
        """ Randomize entire board according to selection made.

        :param board: Current board
        :param select: Select randomization mode
        :param num: Percentage or fixed number of live cells
        :return: New randomized board
        """
        if select == 0:
            new_b = board_generation.randomize_board_chance(board, num)
            return new_b
        else:
            new_b = board_generation.randomize_board_fixed(board, num)
            return new_b

    def randomize_chance_call(self):
        """ Method for calling percentage randomization.

        :return: New randomized board
        """
        new_b = self.randomize_board_select(self.board, 0, self.percent)
        self.push_to_back_stack(new_b)
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        self.canvas.after(1, self.draw, new_b)
        return new_b

    def randomize_fixed_call(self):
        """ Method for calling fixed number randomization.

        :return: New randomized board
        """
        new_b = self.randomize_board_select(self.board, 1, self.number)
        self.push_to_back_stack(new_b)
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        self.canvas.after(1, self.draw, new_b)
        return new_b

    def clear_board(self, board):
        """ Sets all cells to dead.

        :param board: Current board
        :return: None
        """
        new_b = board_generation.empty_board(board)
        self.push_to_back_stack(new_b)
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        self.draw(new_b)

    def fill_board(self, board):
        """ Sets all cells to alive.

        :param board: Current board
        :return: None
        """
        new_b = board_generation.full_board(board)
        self.push_to_back_stack(new_b)
        self.generation = 0
        self.gen.set("Generation: " + str(self.generation))
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        self.draw(new_b)

    def cell_alive(self, row, column):
        """ Create black rectangle at target location to create visual representation of live cell.

        :param row: Row of live cell
        :param column: Column of live cell
        :return: None
        """
        self.canvas.create_rectangle(column * 12, row * 12, 11 + column * 12, 11 + row * 12, fill="black", width=0)
        self.canvas.grid(padx=5, pady=5)

    def cell_dead(self, row, column):
        """ Create empty rectangle at target location to create visual representation of dead cell.

        :param row: Row of dead cell
        :param column: Column of dead cell
        :return: None
        """
        self.canvas.create_rectangle(column * 12, row * 12, 11 + column * 12, 11 + row * 12, fill=None, width=0)
        self.canvas.grid(padx=5, pady=5)

    def draw(self, board):
        """ Redraw entire board at once.

        :param board: Current board for drawing
        :return: None
        """
        self.canvas.delete("all")
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == ALIVE:
                    self.cell_alive(i, j)
                else:
                    self.cell_dead(i, j)
        self.canvas.update_idletasks()

    def play(self):
        """ Generate next board according to rules.

        :return: None
        """
        new_b = board_generation.next_board(self.boards_back_stack[len(self.boards_back_stack) - 1])
        self.push_to_back_stack(new_b)
        self.generation += 1
        self.gen.set("Generation: " + str(self.generation))
        self.draw(new_b)
        if self._stop == 0:
            self.canvas.after(1, self.play)
        else:
            self.play_button.configure(text="Start", command=self.start)
            self._stop = 0

    def start(self):
        """ Start continuous calculation of boards.

        :return: None
        """
        self.play_button.configure(text="Stop", command=self.stop)
        self.play()

    def stop(self):
        """ Stop continuous calculation of boards.

        :return: None
        """
        self._stop = 1
        # low-tech way to start-stop, but after_cancel has some problems when running too fast
        # and i don't feel like debugging internal library. Maybe sometime later (probably not :D)

    def back(self):
        """ Go one step back.

        :return: None
        """
        if len(self.boards_back_stack) > 1:
            self.push_to_forward_stack(self.boards_back_stack.pop())
            self.draw(self.boards_back_stack[-1])

    def forward(self):
        """ Go one step forward.

        :return: None
        """
        if len(self.boards_forward_stack) > 1:
            self.push_to_back_stack(self.boards_forward_stack.pop())
            self.draw(self.boards_back_stack[-1])


if __name__ == '__main__':
    app = GameOfLife()
