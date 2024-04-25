import numpy as np

example_board = np.array([['X','O','X'],
                          [' ', ' ', ' '],
                          [' ', 'O', ' ']])


def get_possible_moves(board, player): 
    moves = []
    for (x,y) , element in np.ndenumerate(board):
        if element == ' ':
            new_board = np.array(board, copy=True)
            new_board[x][y] = 'X' if player is 'max' else 'O'
            moves.append(new_board)
    return moves

example_moves = get_possible_moves(example_board, 'max')
for b in example_moves:
    print(b)