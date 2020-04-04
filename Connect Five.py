import random, sys, pygame, time, copy
from pygame.locals import *

FPS = 10 # frames per second to update the screen
WINDOWWIDTH = 1200 # width of the program's window, in pixels
WINDOWHEIGHT = 675 # height in pixels
SPACESIZE = 32 # width & height of each space on the board, in pixels
BOARDWIDTH = 19 # how many columns of lines on the game board
BOARDHEIGHT = 19 # how many rows of lines on the game board
WHITE_TILE = 'WHITE_TILE' # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE' # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value

# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
TAN        = (227, 195, 122)
GREEN      = (  0, 155,   0)

GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
bgColor = TAN
TEXTBGCOLOR = GREEN

def main():

    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Connect Five')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    while True:
        runGame()

def runGame():
    mainBoard = getNewBoard()
    turn = 'black'

    # Make the Surface and Rect objects for the "New Game" button
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)

    drawBoard(mainBoard)
    drawTurn(mainBoard, turn)
    DISPLAYSURF.blit(newGameSurf, newGameRect)
    pygame.display.update()

    while True:
        movexy = None
        while movexy == None:
            # Keep looping until the player clicks on a valid space.

            checkForQuit()
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONUP:
                    # Handle mouse click events
                    mousex, mousey = event.pos
                    if newGameRect.collidepoint( (mousex, mousey) ):
                        # Start a new game
                        return
                    # movexy is set to a two-item tuple XY coordinate, or None value
                    movexy = getSpaceClicked(mousex, mousey)
                    if movexy != None and not isValidMove(mainBoard, movexy[0], movexy[1]):
                        movexy = None

        # Make the move and end the turn.
        if turn == 'black':
            mainBoard[movexy[0]][movexy[1]] = BLACK_TILE
            turn = 'white'
        else:
            mainBoard[movexy[0]][movexy[1]] = WHITE_TILE
            turn = 'black'

        drawBoard(mainBoard)
        drawTurn(mainBoard, turn)
        DISPLAYSURF.blit(newGameSurf, newGameRect)
        pygame.display.update()

        # Check for a winner.
        winner = isWinner(mainBoard)
        if winner:
            showGameOver(winner)
            break

def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE, YMARGIN + y * SPACESIZE

def drawBoard(board):
    # Draw background of board.
    DISPLAYSURF.fill(bgColor)

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + ((BOARDHEIGHT - 1) * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + ((BOARDWIDTH - 1) * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    # Draw the small circles on the go board.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if x % 6 == 3 and y % 6 == 3:
                centerx, centery = translateBoardToPixelCoord(x, y)
                pygame.draw.circle(DISPLAYSURF, GRIDLINECOLOR, (centerx, centery), 5, 0)

    # Draw the black & white tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                else:
                    tileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)

def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > (x - 0.5) * SPACESIZE + XMARGIN and \
               mousex < (x + 0.5) * SPACESIZE + XMARGIN and \
               mousey > (y - 0.5) * SPACESIZE + YMARGIN and \
               mousey < (y + 0.5) * SPACESIZE + YMARGIN:
                return (x, y)
    return None

def drawTurn(board, turn):
    # Draws whose turn it is at the bottom of the screen.
    turnSurf = FONT.render("%s's Turn" % (turn.title()), True, TEXTCOLOR)
    turnRect = turnSurf.get_rect()
    turnRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(turnSurf, turnRect)

def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board

def isValidMove(board, xstart, ystart):
    # Returns False iff the player's move is invalid.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False
    return True

def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT

def showGameOver(winner):
    if winner == 'white':
        color = WHITE
    elif winner == 'black':
        color = BLACK
    text = '%s Wins'%winner.title()
    textSurf = BIGFONT.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.topright = (WINDOWWIDTH - 8, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(textSurf, textRect)

    # Make the Surface and Rect objects for the "New Game" button
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)
    DISPLAYSURF.blit(newGameSurf, newGameRect)
    pygame.display.update()

    while True:
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                # Handle mouse click events
                mousex, mousey = event.pos
                if newGameRect.collidepoint( (mousex, mousey) ):
                    # Start a new game
                    return

def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

def isWinner(board):
    # check horizontal spaces
    for x in range(BOARDWIDTH - 4):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLACK_TILE and board[x+1][y] == BLACK_TILE and board[x+2][y] == BLACK_TILE and\
                board[x+3][y] == BLACK_TILE and board[x+4][y] == BLACK_TILE:
                    return 'black'
            if board[x][y] == WHITE_TILE and board[x+1][y] == WHITE_TILE and board[x+2][y] == WHITE_TILE and\
                board[x+3][y] == WHITE_TILE and board[x+4][y] == WHITE_TILE:
                    return 'white'
    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 4):
            if board[x][y] == BLACK_TILE and board[x][y+1] == BLACK_TILE and board[x][y+2] == BLACK_TILE and\
                board[x][y+3] == BLACK_TILE and board[x][y+4] == BLACK_TILE:
                return 'black'
            if board[x][y] == WHITE_TILE and board[x][y+1] == WHITE_TILE and board[x][y+2] == WHITE_TILE and\
                board[x][y+3] == WHITE_TILE and board[x][y+4] == WHITE_TILE:
                return 'white'
    # check / diagonal spaces
    for x in range(BOARDWIDTH - 4):
        for y in range(4, BOARDHEIGHT):
            if board[x][y] == BLACK_TILE and board[x+1][y-1] == BLACK_TILE and board[x+2][y-2] == BLACK_TILE and\
                board[x+3][y-3] == BLACK_TILE and board[x+4][y-4] == BLACK_TILE:
                return 'black'
            if board[x][y] == WHITE_TILE and board[x+1][y-1] == WHITE_TILE and board[x+2][y-2] == WHITE_TILE and\
                board[x+3][y-3] == WHITE_TILE and board[x+4][y-4] == WHITE_TILE:
                return 'white'
    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 4):
        for y in range(BOARDHEIGHT - 4):
            if board[x][y] == BLACK_TILE and board[x+1][y+1] == BLACK_TILE and board[x+2][y+2] == BLACK_TILE and\
                board[x+3][y+3] == BLACK_TILE and board[x+4][y+4] == BLACK_TILE:
                return 'black'
            if board[x][y] == WHITE_TILE and board[x+1][y+1] == WHITE_TILE and board[x+2][y+2] == WHITE_TILE and\
                board[x+3][y+3] == WHITE_TILE and board[x+4][y+4] == WHITE_TILE:
                return 'white'
    return None

if __name__ == '__main__':
    main()