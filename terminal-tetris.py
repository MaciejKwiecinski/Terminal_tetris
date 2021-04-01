import random
from copy import deepcopy
import os

BOARD = 20
BOARD_WITH_FRAME = BOARD+2

PIECES = [
    [[1], [1], [1], [1]],

    [[1, 1],
     [1, 1]],

    [[1, 0],
     [1, 0],
     [1, 1]],

    [[0, 1],
     [0, 1],
     [1, 1]],

    [[1, 0],
     [1, 1],
     [0, 1]],
]

random.seed()


def create_board(piece, location):
    board = [[0 for x in range(BOARD_WITH_FRAME)] for y in range(BOARD_WITH_FRAME)]
    for i in range(BOARD_WITH_FRAME):
        board[i][0] = 2
        board[BOARD_WITH_FRAME-1][i] = 2
        board[i][BOARD_WITH_FRAME-1] = 2
    merge_board_piece(board, piece, location)
    return board


def show_board(board, error_message):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("")
    for i in range(BOARD_WITH_FRAME):
        for j in range(BOARD_WITH_FRAME):
            if board[i][j] == 1:
                print('*', end='')
            elif board[i][j] == 2:
                print('*', end='')
            else:
                print(' ', end='')
        print("")

    print("Quick play instructions:\n")
    print(" - a (return): move piece left")
    print(" - d (return): move piece right")
    print(" - w (return): rotate piece counter clockwise")
    print(" - s (return): rotate piece clockwise")
    print(" - e (return): just move the piece downwards as is")
    print(" - q (return): to quit the game anytime")
    print(error_message)


def merge_board_piece(board, piece, location):
    piece_size_x = len(piece)
    piece_size_y = len(piece[0])
    for i in range(piece_size_x):
        for j in range(piece_size_y):
            if (piece[i][j] != 0 and board[location[0]+i][location[1]+j] == 0):
                board[location[0]+i][location[1]+j] = piece[i][j]
    return board


def clear_board(board):
    new_row = [0] * BOARD
    new_row.insert(0, 2)
    new_row.insert(BOARD_WITH_FRAME, 2)
    for i in range(BOARD_WITH_FRAME):
        for j in range(BOARD_WITH_FRAME):
            if board[i][j] == 1:
                board[i][j] = 0
    x = check_and_delete_full_layers(board)
    if x != 0:
        for i in range(x):
            board.insert(0, new_row)
    return board


def create_static(board):
    for i in range(BOARD_WITH_FRAME):
        for j in range(BOARD_WITH_FRAME):
            if board[i][j] == 1:
                board[i][j] = 2
    return board


def take_pieces():
    return PIECES[random.randint(0, 4)]


def take_first_position():
    return [0, random.randint(1, BOARD-1)]


def move_down(board, piece, location):
    board = clear_board(board)
    location[0] += 1
    return board


def move_left(board, piece, location):
    board = clear_board(board)
    location[1] -= 1
    return board


def move_right(board, piece, location):
    board = clear_board(board)
    location[1] += 1
    return board


def rotate_clockwise(piece):
    elem = list(zip(*piece[::-1]))
    rotate_piece = [list(e) for e in elem]
    return rotate_piece


def rotate_counter_clockwise(piece):
    for i in range(3):
        piece = rotate_clockwise(piece)
    return piece


def is_valid(board, piece, location):
    piece_size_x = len(piece)
    piece_size_y = len(piece[0])
    for i in range(piece_size_x):
        for j in range(piece_size_y):
            if board[location[0]+i][location[1]+j] == 2 and piece[i][j] == 1:
                return False
    return True


def can_be_moved_down(board, piece, location):
    copy_location = deepcopy(location)
    copy_location[0] += 1
    return is_valid(board, piece, copy_location)


def can_be_moved_left(board, piece, location):
    copy_location = deepcopy(location)
    copy_location[1] -=1
    return is_valid(board, piece, copy_location)


def can_be_moved_right(board, piece, location):
    copy_location = deepcopy(location)
    copy_location[1] += 1
    return is_valid(board, piece, copy_location)


def can_be_rotate_clockwise(board, piece, location):
    copy_location = deepcopy(location)
    new_piece = rotate_clockwise(piece)
    return is_valid(board, new_piece, copy_location)


def can_be_rotate_counter_clockwise(board, piece, location):
    copy_location = deepcopy(location)
    new_piece = rotate_counter_clockwise(piece)
    return is_valid(board, new_piece, copy_location)


def game_is_over(board, piece, location):
    if location[0] == 0 and not can_be_moved_down(board, piece, location):
        return True
    return False


def check_and_delete_full_layers(board):
    x = 0
    full_layer = [2]*BOARD_WITH_FRAME
    for i in range(BOARD_WITH_FRAME-1):
        if board[i] == full_layer:
            board.pop(i)
            x += 1
    return x


def play_game():
    piece = take_pieces()
    location = take_first_position()
    board = create_board(piece, location)
    merge_board_piece(board, piece, location)
    show_board(board, '')
    x = input()
    while x != 'q' or game_is_over(board, piece, location) == False:
        if can_be_moved_down(board, piece, location):
            if x == 'e':
                if can_be_moved_down(board, piece, location):
                    board = move_down(board, piece, location)
                    error_message = "Your move:"
                else:
                    error_message = "Invalid move"
            elif x == 'a':
                if can_be_moved_left(board, piece, location):
                    board = move_left(board, piece, location)
                    board = move_down(board, piece, location)
                    error_message = "Your move:"
                else:
                    error_message = "Invalid move"
            elif x == 'd':
                if can_be_moved_right(board, piece, location):
                    board = move_right(board, piece, location)
                    board = move_down(board, piece, location)
                    error_message = "Your move:"
                else:
                    error_message = "Invalid move"
            elif x == 'w':
                if can_be_rotate_clockwise(board, piece, location):
                    piece = rotate_clockwise(piece)
                    board = move_down(board, piece, location)
                    error_message = "Your move:"
                else:
                    error_message = "Invalid move"
            elif x == 's':
                if can_be_rotate_counter_clockwise(board, piece, location):
                    piece = rotate_counter_clockwise(piece)
                    board = move_down(board, piece, location)
                    error_message = "Your move:"
                else:
                    error_message = "Invalid move"
            board = merge_board_piece(board, piece, location)
        else:
            error_message = "Your move:"
            board = create_static(board)
            piece = take_pieces()
            location = take_first_position()
            merge_board_piece(board, piece, location)
        show_board(board, error_message)
        x = input()

if __name__ == "__main__":
    play_game()
