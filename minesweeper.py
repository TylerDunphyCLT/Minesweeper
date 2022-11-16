import pygame
import random

# Initialize Settings

boxSize = 32 # factors of 2 load in the cleanest
cols = 30
rows = 16
run = True
numMines = 99
game = "init"

if numMines >= cols * rows:
    numMines = cols*rows -1

pygame.init()
surface = pygame.display.set_mode((cols*boxSize,rows*boxSize))
pygame.display.set_caption("Minesweeper")

# Load in images
mineDraw = pygame.transform.scale(pygame.image.load('mine.png'), (boxSize-1,boxSize-1))
one = pygame.transform.scale(pygame.image.load('one.png'), (boxSize-1,boxSize-1))
two = pygame.transform.scale(pygame.image.load('two.png'), (boxSize-1,boxSize-1))
three = pygame.transform.scale(pygame.image.load('three.png'), (boxSize-1,boxSize-1))
four = pygame.transform.scale(pygame.image.load('four.png'), (boxSize-1,boxSize-1))
five = pygame.transform.scale(pygame.image.load('five.png'), (boxSize-1,boxSize-1))
six = pygame.transform.scale(pygame.image.load('six.png'), (boxSize-1,boxSize-1))
seven = pygame.transform.scale(pygame.image.load('seven.png'), (boxSize-1,boxSize-1))
eight = pygame.transform.scale(pygame.image.load('eight.png'), (boxSize-1,boxSize-1))
flag = pygame.transform.scale(pygame.image.load('flag.png'), (boxSize-1,boxSize-1))

numbers = [one, two, three, four, five, six, seven, eight]

# Class Tile, has a number 0-8 or -1 if it is a mine. It also stores if it is covered

class Tile(object):
    def __init__(self,x,y,num,cover, flag):
        self.x = x
        self.y = y
        self.num = num
        self.cover = cover
        self.flag = flag

board = [[] for i in range(cols)]

for i in range(0,cols,1):
    for j in range(0,rows,1):
        board[i].append(Tile(i,j,0,True, False))
        
# Randomize Mines
def randomizeMines(x,y,board_):
    for i in range(0,numMines,1):
        # Picks random index in board
        randX = random.randint(0,cols-1)
        randY = random.randint(0,rows-1)
        # Checks to make sure that the spot picked is not a mine, nor is it where the first click is
        while(board_[randX][randY].num == -1 or (randX == (int)(x) and randY == (int)(y))):
            randX = random.randint(0,cols-1)
            randY = random.randint(0,rows-1)
        board_[randX][randY].num = -1

# Checks neighboring tiles for mines
def checkMines(x,y,board_):
    total = 0
    for i in range(x-1,x+2,1):
        for j in range(y-1,y+2,1):
            # Do not attempt to check a tile outside of the bounds, or itself
            if not (i < 0 or i > cols-1 or j < 0 or j > rows-1 or (i == x and j == y)):
                if board_[i][j].num == -1:
                    total += 1
    return total

# Runs all necessary checks to initialize numbers  
def setNumbers(board_):
    for i in range(0,cols,1):
        for j in range(0,rows,1):
            if board_[i][j].num != -1:
                board_[i][j].num = checkMines(i,j,board_)

# Calculates losing the game
def loseGame(board_):
    for i in range(0,cols,1):
        for j in range(0,rows,1):
            board_[i][j].cover = False
    game = "lose"

# Calculates if the game is done
def calcWin(board_):
    numCover = 0
    for i in range(0,cols,1):
        for j in range(0,rows,1):
            if board_[i][j].cover == True:
                numCover += 1
    return numCover == numMines
                
def placeFlag(x,y,board_):
    board_[x][y].flag = not board_[x][y].flag


# Handles tile clearing
def clearTile(x,y,board_):
    if board_[x][y].num == 0 and board_[x][y].flag == False:
        board_[x][y].cover = False
        # Clears surrounding tiles as a convenience feature
        for i in range(x-1,x+2,1):
            for j in range(y-1,y+2,1):
                # Do not attempt to clear a tile outside of the bounds, or itself
                if not (i < 0 or i > cols-1 or j < 0 or j > rows-1 or (i == x and j == y)):
                    if board_[i][j].cover == True and board_[i][j].flag == False:
                        clearTile(i,j,board_)
    elif board_[x][y].num == -1 and board_[x][y].flag == False:
        loseGame(board_)
    elif board_[x][y].flag == False:
        board_[x][y].cover = False
    
# Displays Board
def displayBoard(board_):
    if game == "win":
        surface.fill((200,255,200))
    else:
        surface.fill((255,255,255))
    
    for i in range(0,cols,1):
        for j in range(0,rows,1):

            pygame.draw.rect(surface, (0,0,0), pygame.Rect(i*boxSize,j*boxSize,boxSize,boxSize), 1)

            num_ = board_[i][j].num
            cover_ = board_[i][j].cover
            flag_ = board_[i][j].flag

            if num_ == -1:
                surface.blit(mineDraw, (i*boxSize, j*boxSize))
            elif num_ > 0:
                surface.blit(numbers[num_-1], (i*boxSize, j*boxSize))

            if cover_:
                pygame.draw.rect(surface, (180,180,180), pygame.Rect(i*boxSize+1,j*boxSize+1,boxSize-2,boxSize-2))
                if flag_:
                    surface.blit(flag, (i*boxSize, j*boxSize))

    pygame.display.update()

# GAME

displayBoard(board)

while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            run = False

        if game == "init":

            if event.type == pygame.MOUSEBUTTONUP:

                pos = pygame.mouse.get_pos()

                if pos[0] > 0 and pos[0] < boxSize*cols and pos[1] > 0 and pos[1] < boxSize*rows:
                    randomizeMines((int)(pos[0]/boxSize),(int)(pos[1]/boxSize),board)
                    setNumbers(board)
                    clearTile((int)(pos[0]/boxSize),(int)(pos[1]/boxSize),board)
                    game = "play"

        if game == "play":

            if event.type == pygame.MOUSEBUTTONUP:

                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    clearTile((int)(pos[0]/boxSize),(int)(pos[1]/boxSize),board)
                else:
                    placeFlag((int)(pos[0]/boxSize),(int)(pos[1]/boxSize),board)
                displayBoard(board)
                if calcWin(board):
                    game = "win"

        if game == "win" or game == "lose":

            displayBoard(board)

        

    


