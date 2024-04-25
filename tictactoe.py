import numpy as np


def get_possible_moves(board, player): 
    moves = []
    for (x,y) , element in np.ndenumerate(board):
        if element == ' ':
            new_board = np.array(board, copy=True)
            new_board[x][y] = 'X' if player is 'max' else 'O'
            moves.append(new_board)
    return moves

#final score of board
# 1: game ends with a win for X
# -1: game ends with a win for O
# O: Tie game

def get_score(board, depth=0):
    if (np.any(np.all(board == 'X', axis = 0)) or 
        np.any(np.all(board == 'X', axis = 1)) or
        np.all(board.diagonal() == 'X') or 
        np.all(np.fliplr(board).diagonal() == 'X')): 
        
        #MAX victory
        return 1 * (1 / (1+depth))
    
    elif (np.any(np.all(board == 'O', axis = 0)) or 
        np.any(np.all(board == 'O', axis = 1)) or
        np.all(board.diagonal() == 'O') or 
        np.all(np.fliplr(board).diagonal() == 'O')):
        
        #min victory
        return -1 * (1/ (1+depth))
    
    elif not (board == ' ').any():
        #Draw
        return 0
    
    else: 
        return None
    

    