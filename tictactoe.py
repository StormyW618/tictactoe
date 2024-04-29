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
    

#alpha beta pruning :(
def find_value(board, player, alpha=float('-inf'),beta=float('inf'), depth=0 ):
    score = get_score(board)
    #return value at last node or score if game is finished
    if score is not None:
        return score
    # maximizing player
    if player == "max":
        maxvalue = float('-inf')
        #iterate over successors
        successors  = get_possible_moves(board, "max")
        for i in successors:
            maxvalue = max(maxvalue,find_value(i, "min", alpha, beta, depth+1))
            if maxvalue >= beta:
                return maxvalue
            alpha = max(alpha, maxvalue)
        return maxvalue
    #minimizing player
    else:
        minvalue = float('inf')
        succes  = get_possible_moves(board, "min")
        for h in succes:
            minvalue = min(minvalue,find_value(h, "max", alpha, beta, depth + 1))
            if minvalue <= alpha:
                return minvalue
            beta = min(beta, minvalue)
        return minvalue

#cheats starting about half way through the game
#very bad algorithm-> if you can call it that
def cheat(board, player):
    blank = np.array([[' ', ' ', ' '],
                        [' ', ' ', ' '],
                        [' ', ' ', ' ']])
    moves = []
    count = 0
    for (x,y) , element in np.ndenumerate(board):
        if element == 'X':
           count+= 1
    if count > 2:
        for (x,y) , element in np.ndenumerate(board):
            if element == 'X':
                new_board = np.array(board, copy=True)
                new_board[x][y] = 'X' if player is 'max' else 'O'
                moves.append(new_board)
                break
        return moves[0]
    else:
        return 0

def find_best_move(board, player):
    print("Deciding best move...")
    boards = get_possible_moves(board, player)
    # for i in boards:
    #     print(i)
    values = [find_value(board,
                        ('max' if player is 'min'
                        else 'min'))
            for board in tqdm(boards)]
    # print(values)
    # print("In best move\n")
    
    #if values has 1; cheat
    if None in values:
        raise ValueError('find_value should always return an integer.')
    
    for i in values:
        if int(i) == 1:
            # print("before test")
            print("Not Today...")
            test = cheat(board, player)
            if test != 0:
                # print("returning test")
                return test
            
    if player is "max":
        policy_vector = np.array([1 if value == np.amax(values) else 0
                                for value in values])
    else:
        policy_vector = np.array([1 if value == np.amin(values) else 0
                                for value in values])
    # Normalize Probabilities
    policy_vector = policy_vector / np.count_nonzero(policy_vector)
    return boards[np.random.choice(np.arange(len(values)),
                                1,
                                p=policy_vector)[0]]
    

# Plays a match between  a human and the bot, asking the human for their move  via console
# To select the  role of the  bot (max or min), edit  line 11

def run_demo():
    board = np.array([[' ', ' ', ' '],
                        [' ', ' ', ' '],
                        [' ', ' ', ' ']])
    score = get_score(board)
    player = "max"
    while score is None:
        if player == "min":   # Set this to max if you want the bot to go first, and min otherwise
            board = find_best_move(board, player)
        else:
            move_entered = False
            while not move_entered:
                try:
                    move = int(input('Choose a move...')) - 1
                    if not 0 <= move <= 8:
                        print("Enter an integer between 1 and 9.\n")
                        continue
                    elif not board[move//3][move%3] == ' ':
                        print("That spot is already taken.\n")
                        continue
                    else:
                        board[move//3][move%3]= 'O' if player == "min" else "X"
                        move_entered = True
                except ValueError:
                    print("Enter an integer.\n")
        score = get_score(board)
        player = "min" if player == "max" else "max"
        print(board)
    if (score == 0):
        print("Draw")
    elif (score > 0):
        print("You Win")
    else:
        print("You Lose")


run_demo()