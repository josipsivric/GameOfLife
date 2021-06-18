import random
from time import time

ALIVE = 1
DEAD = 0


def empty_board(board):
    """ Fill entire board with live cells.

    :param board: pass original board
    :return: new_b: new emptied board
    """
    new_b = board.copy()

    for i in range(len(new_b)):
        for j in range(len(new_b[i])):
            new_b[i][j] = DEAD
    return new_b


def full_board(board):
    """ Fill entire board with live cells.

    :param board: pass original board
    :return: new_b: new filled board
    """
    new_b = board.copy()

    for i in range(len(new_b)):
        for j in range(len(new_b[i])):
            new_b[i][j] = ALIVE
    return new_b


def randomize_board_chance(board, chance):
    """Randomize board according to chance given by user.

    :param board: pass original board
    :param chance: chance that each cell is alive
    :return: new_b: new randomized board
    """
    random.seed(time())
    new_b = board.copy()

    for i in range(len(new_b)):
        for j in range(len(new_b[i])):
            number = random.randint(1, 100)
            if chance >= number and chance != 0:
                new_b[i][j] = ALIVE
            else:
                new_b[i][j] = DEAD
    return new_b


def randomize_board_fixed(board, number_of_alive):
    """ Randomize board according to number of alive cells set by user.

    :param board: pass original board
    :param number_of_alive: number of live cells on entire board
    :return: new_b: new randomized board
    """
    new_b = [[DEAD] * len(board) for _ in range(len(board[0]))]

    while number_of_alive > 0:
        i = random.randrange(0, len(new_b))
        j = random.randrange(0, len(new_b[0]))
        if new_b[i][j] == DEAD:
            new_b[i][j] = ALIVE
            number_of_alive -= 1
    return new_b


def next_board(board):
    """ Calculate entire new board according to the rules.

    :param board: pass original board
    :return: new_b: new board calculated according to rules
    """

    side_length = len(board)
    new_board = [[DEAD] * side_length for _ in range(side_length)]

    for i in range(side_length):
        for j in range(side_length):
            sum_of_cells_around = board[(i - 1) % side_length][(j - 1) % side_length] + \
                                  board[(i - 1) % side_length][j % side_length] + \
                                  board[(i - 1) % side_length][(j + 1) % side_length] + \
                                  board[i % side_length][(j - 1) % side_length] + \
                                  board[i % side_length][(j + 1) % side_length] + \
                                  board[(i + 1) % side_length][(j - 1) % side_length] + \
                                  board[(i + 1) % side_length][j % side_length] + \
                                  board[(i + 1) % side_length][(j + 1) % side_length]
            if board[i][j] == ALIVE:
                if sum_of_cells_around < 2 or sum_of_cells_around > 3:
                    new_board[i][j] = DEAD
                else:
                    new_board[i][j] = ALIVE
            else:
                if sum_of_cells_around == 3:
                    new_board[i][j] = ALIVE
                else:
                    new_board[i][j] = DEAD
    return new_board
