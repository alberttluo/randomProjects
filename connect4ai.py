import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

EMPTY_PIECE = 0
PLAYER_PIECE = 1
AI_PIECE = 2

COL_COUNT = 7
ROW_COUNT = 6

def printBoard(board):
    print(np.flip(board, 0))

def createBoard():
    return np.zeros((6, 7))

def dropPiece(board, row, col, piece):
    board[row][col] = piece

def isValidLocation(board, col):
    return board[ROW_COUNT-1][col] == 0

def getValidLocations(board):
    valid_locations = []
    for col in range (COL_COUNT):
        if isValidLocation(board, col):
            valid_locations.append(col)
    return valid_locations

def getNextOpen(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


def isColumnFull(board, column):
    for i in range(ROW_COUNT):
        if board[ROW_COUNT - 1 - i, column] == 0:
            return False
    return True    

def checkWin(board, piece):
    # Check horizontal locations for win
	for c in range(COL_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COL_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COL_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def drawBoard(board):
    for col in range(COL_COUNT):
        for row in range (ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col*SQSIZE, row*SQSIZE+SQSIZE, SQSIZE, SQSIZE))
            pygame.draw.circle(screen, WHITE, (col*SQSIZE+SQSIZE/2, row*SQSIZE+SQSIZE+SQSIZE/2), RADIUS)

    
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(col*SQSIZE+SQSIZE/2), height-int(row*SQSIZE+SQSIZE/2)), RADIUS)
            elif board[row][col] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(col*SQSIZE+SQSIZE/2), height-int(row*SQSIZE+SQSIZE/2)), RADIUS)
    pygame.display.update()

#probably useless unless depth is 0
def evaluateWindow(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score += 5
    elif window.count(piece == 2) and window.count(EMPTY_PIECE) == 2:
        score += 2
    
    if window.count(opp_piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score -= 4

    return score

def scorePosition(board, piece):
    score = 0

    #center column
    center_array = [int(i) for i in list(board[:, COL_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    #horizontals
    for row in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[row ,:])]
        for col in range(COL_COUNT - 3):
            window = row_array[col:col+4]
            score += evaluateWindow(window, piece)
    
    #verticals
    for col in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(ROW_COUNT - 3):
            window = col_array[row:row + 4]
            score += evaluateWindow(window, piece)
    
    #positive diagonals
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row+i][col+i] for i in range(4)]
            score += evaluateWindow(window, piece)

    #negative diagonals
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row+3-i][col+i]for i in range(4)]
            score += evaluateWindow(window, piece)

    return score

def bestMove(board, piece):
    bestScore = 0
    valid_locations = getValidLocations(board)
    bestCol = random.choice(valid_locations)
    for col in valid_locations:
        row = getNextOpen(board, col)
        copyBoard = board.copy()
        dropPiece(copyBoard, row, col, piece)
        score = scorePosition(copyBoard, piece)
        if score > bestScore:
            bestScore = score
            bestCol = col

    return bestCol

def isTerminalNode(board):
    return checkWin(board, AI_PIECE) or checkWin(board, PLAYER_PIECE) or len(getValidLocations(board)) == 0

transposition_table = {}

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = getValidLocations(board)
    terminalNode = isTerminalNode(board)

    if str(board) in transposition_table:
        return transposition_table[str(board)]
    
    if depth == 0 or terminalNode:
        if terminalNode:
            if checkWin(board, AI_PIECE):
                return (None, 10000000000000)
            elif checkWin(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: #game is over -- no valid moves
                return (None, 0)
        else: #depth is 0
            return None, scorePosition(board, AI_PIECE)
    
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextOpen(board, col)
            bcopy = board.copy()
            dropPiece(bcopy, row, col, AI_PIECE)
            new_score = minimax(bcopy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        
        transposition_table[str(board)] = (column, value)
        return column, value
        
    else: #minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextOpen(board, col)
            bcopy = board.copy()
            dropPiece(bcopy, row, col, PLAYER_PIECE)
            new_score = minimax(bcopy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break

        transposition_table[str(board)] = (column, value)
        
        return column, value
    

board = createBoard()
printBoard(board)
gameOver = False

pygame.init()

SQSIZE = 100
RADIUS = int(SQSIZE/2 - 5)

width = COL_COUNT * SQSIZE
height = (ROW_COUNT + 1) * SQSIZE

size = (width, height)

screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQSIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQSIZE/2)), RADIUS)
            
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQSIZE))

            if turn == PLAYER:
                posx = event.pos[0]
                column = int(math.floor(posx/SQSIZE))

                if isValidLocation(board, column):
                    row = getNextOpen(board, column)
                    dropPiece(board, row, column, PLAYER_PIECE)

                    if checkWin(board, PLAYER_PIECE):
                        label = myfont.render(f"Player {PLAYER_PIECE} wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        gameOver = True

                    turn += 1
                    turn = turn % 2

                    printBoard(board)
                    print("\n")
                    drawBoard(board)

    if turn == AI and gameOver == False:
        
        column, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if isValidLocation(board, column):
            row = getNextOpen(board, column)
            dropPiece(board, row, column, AI_PIECE)

            if checkWin(board, AI_PIECE):
                label = myfont.render(f"Player {AI_PIECE} wins!", 1, YELLOW)
                screen.blit(label, (40, 10))
                gameOver = True
            
            printBoard(board)
            print("\n")
            drawBoard(board)

            turn += 1
            turn = turn % 2

    if gameOver:
        pygame.time.wait(1000)
        transposition_table.clear()