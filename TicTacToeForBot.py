import random


def makeMove(board, letter, move):
     board[move] = letter

        
def isWinner(bo, le):
     return ((bo[7] == bo[8] == bo[9] == le) or #Top line
        (bo[4] == bo[5] == bo[6] == le) or #Middle line
        (bo[1] == bo[2] == bo[3] == le) or #Bottom line
        (bo[7] == bo[4] == bo[1] == le) or #Left vertical line
        (bo[8] == bo[5] == bo[2] == le) or #Central vertical line
        (bo[9] == bo[6] == bo[3] == le) or #Right vertical line
        (bo[7] == bo[5] == bo[3] == le) or #3-7 Diagonal
        (bo[9] == bo[5] == bo[1] == le))   #1-9 Diagonal

    
def getBoardCopy(board):
     #Makes a copy of the board and returns it
    dupe_Board = []
 
    for i in board:
         dupe_Board.append(i)

    return dupe_Board
 
    
def isSpaceFree(board, move):
    #Returns True if the move is possive
    return board[move] == ' '

 
def chooseRandomMoveFromList(board, moves_List):
     #Returns a random possible move
     #Returns None if no move is possible
    possible_Moves = []
    for i in moves_List:
        if isSpaceFree(board, i):
            possible_Moves.append(i)
 
    if len(possible_Moves) != 0:
        return random.choice(possible_Moves)
    else:
        return None

    
def getComputerMove(board, computer_Letter):
    if computer_Letter == 'Х':
         player_Letter = 'О'
    else:
        player_Letter = 'Х'
 
    #Here starts AI for playing Tic-Tac-Toe
    #Checks if bot can win by the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computer_Letter, i)
            if isWinner(copy, computer_Letter):
                return i

    #Checks if player can win by the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, player_Letter, i)
            if isWinner(copy, player_Letter):
                return i
 
    #Trying to occupy one of the corners
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move
 
    #Trying to occupy the center
    if isSpaceFree(board, 5):
        return 5
 
    #Occupying what is left
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isBoardFull(board):
    #Returns True if the board is full
    #Returns False otherwise
    for i in range(1, 10):
         if isSpaceFree(board, i):
            return False
    return True
