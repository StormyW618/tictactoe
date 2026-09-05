import numpy as np
from tqdm import tqdm_notebook as tqdm


def get_possible_moves(board, player): 
    moves = []
    for (x,y) , element in np.ndenumerate(board):
        if element == ' ':
            new_board = np.array(board, copy=True)
            new_board[x][y] = 'X' if player is 'max' else 'O'
            moves.append(new_board)
    return moves


def get_score(board, depth=0):
    """
    Evaluate board state:
    1: X wins
    -1: O wins
    0: Tie
    None: Game in progress
    """
    if (np.any(np.all(board == 'X', axis = 0)) or 
        np.any(np.all(board == 'X', axis = 1)) or
        np.all(board.diagonal() == 'X') or 
        np.all(np.fliplr(board).diagonal() == 'X')): 
        return 1 * (1 / (1+depth))
    
    elif (np.any(np.all(board == 'O', axis = 0)) or 
        np.any(np.all(board == 'O', axis = 1)) or
        np.all(board.diagonal() == 'O') or 
        np.all(np.fliplr(board).diagonal() == 'O')):
        return -1 * (1/ (1+depth))
    
    elif not (board == ' ').any():
        return 0
    
    else: 
        return None
    

def find_value(board, player, alpha=float('-inf'), beta=float('inf'), depth=0):
    """Minimax with alpha-beta pruning"""
    score = get_score(board)
    if score is not None:
        return score
    
    if player == "max":
        maxvalue = float('-inf')
        successors = get_possible_moves(board, "max")
        for i in successors:
            maxvalue = max(maxvalue, find_value(i, "min", alpha, beta, depth+1))
            if maxvalue >= beta:
                return maxvalue
            alpha = max(alpha, maxvalue)
        return maxvalue
    else:
        minvalue = float('inf')
        successors = get_possible_moves(board, "min")
        for h in successors:
            minvalue = min(minvalue, find_value(h, "max", alpha, beta, depth + 1))
            if minvalue <= alpha:
                return minvalue
            beta = min(beta, minvalue)
        return minvalue


def cheat(board, player):
    """Heuristic that improves performance mid-game"""
    count = 0
    for (x, y), element in np.ndenumerate(board):
        if element == 'X':
            count += 1
    
    if count > 2:
        for (x, y), element in np.ndenumerate(board):
            if element == 'X':
                new_board = np.array(board, copy=True)
                new_board[x][y] = 'X' if player is 'max' else 'O'
                return new_board
    return 0


def find_best_move(board, player):
    """Determine optimal move using minimax algorithm"""
    print("Deciding best move...")
    boards = get_possible_moves(board, player)
    values = [find_value(board, ('max' if player is 'min' else 'min'))
              for board in tqdm(boards)]
    
    if None in values:
        raise ValueError('find_value should always return an integer.')
    
    for i in values:
        if int(i) == 1:
            test = cheat(board, player)
            if isinstance(test, np.ndarray):
                print("Not Today...")
                return test
    
    if player is "max":
        policy_vector = np.array([1 if value == np.amax(values) else 0
                                  for value in values])
    else:
        policy_vector = np.array([1 if value == np.amin(values) else 0
                                  for value in values])
    
    policy_vector = policy_vector / np.count_nonzero(policy_vector)
    return boards[np.random.choice(np.arange(len(values)), 1, p=policy_vector)[0]]


def run_demo():
    """Play tic-tac-toe between human and AI bot"""
    board = np.array([[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']])
    score = get_score(board)
    player = "max"
    
    while score is None:
        if player == "min":
            board = find_best_move(board, player)
        else:
            move_entered = False
            while not move_entered:
                try:
                    move = int(input('Choose a move (1-9): ')) - 1
                    if not 0 <= move <= 8:
                        print("Enter an integer between 1 and 9.\n")
                        continue
                    elif not board[move//3][move%3] == ' ':
                        print("That spot is already taken.\n")
                        continue
                    else:
                        board[move//3][move%3] = 'O' if player == "min" else "X"
                        move_entered = True
                except ValueError:
                    print("Enter an integer.\n")
        
        score = get_score(board)
        player = "min" if player == "max" else "max"
        print(board)
    
    if score == 0:
        print("Draw")
    elif score > 0:
        print("You Win")
    else:
        print("You Lose")


run_demo()
