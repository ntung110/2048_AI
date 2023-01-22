
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import math
import copy as cp


#CONSTANTS
URL = 'https://play2048.co/'
DIRECTORY = 'C:/Users/thanhtung.nguyen/OneDrive - Bodwell High School/Pictures/Screenshots/2048 Bot'


#MOVE MECHANICS
def add_zeros(row):
    #add zeros to back and return data
    for i in range(4 - len(row)):
        row.insert(0,0)
    return row

def remove_zeros(row):
    row = [i for i in row if i != 0]
    return row

def can_move(board):
    for row in board:
        if row == [0,0,0,0]:
            continue
        else:
            i = 0
            #Remove leading zeros
            while row[i] == 0:
                i += 1   
            
            first_num = row[i]
            for j in range(i + 1,len(row)):
                if row[j] == 0 or first_num == row[j]:
                    return True
                else:
                    first_num = row[j]
                
    return False

#MATRIX ROTATION

def rotate_clockwise(board):
    newboard = cp.deepcopy(board)
    rotated = list(zip(*reversed(newboard)))
    #Convert tuple to list
    rotated = [list(i) for i in rotated]
    return rotated

def rotate_counterclockwise(board):
    newboard = cp.deepcopy(board)
    rotated = reversed(list(zip(*newboard)))
    #Convert tuple to list
    rotated = [list(i) for i in rotated]
    return rotated

def reverse_board(board):
    newboard = cp.deepcopy(board)
    for i in newboard:
        i.reverse()
    return newboard

#Check for moves

def can_move_right(board):
    return can_move(board)

def can_move_down(board):
    board = rotate_counterclockwise(board)
    return can_move(board)

def can_move_left(board):
    board = reverse_board(board)
    return can_move(board)
    
def can_move_up(board):
    board = rotate_clockwise(board)
    return can_move(board)

def is_the_game_lost(board):

    if can_move_right(board):
        return False
    elif can_move_up(board):
        return False
    elif can_move_down(board):
        return False
    elif can_move_left(board):
        return False 

    return True

def available_player_moves(board):
    available_moves = []

    if can_move_right(board):
        available_moves.append("right")
    if can_move_up(board):
        available_moves.append("up")
    if can_move_down(board):
        available_moves.append("down")
    if can_move_left(board):
        available_moves.append("left")
    return available_moves

def can_tiles_be_placed(board):
    available_tiles = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return False            
    return True

def availble_bot_moves(board):
    available_tiles = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                pos1 = (2,i,j)
                pos2 = (4,i,j)
                available_tiles.append(pos1) 
                available_tiles.append(pos2)         
    return available_tiles


#MOVEMENT --------------------------------------------------

def move(board):
    
    newboard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for row in range(len(board)):
        if row == [0,0,0,0]:
            continue
        else:
            #Remove all zeros (blank spaces)
            new_row = remove_zeros(board[row])
            new_row.reverse()
            for n in range(len(new_row) - 1):
                if new_row[n] & new_row[n+1] != 0:
                    new_row[n] = new_row[n] << 1
                    new_row[n+1] = 0
            new_row.reverse()   
            new_row = remove_zeros(new_row)
            new_row = add_zeros(new_row) 
            newboard[row] = new_row
    return newboard

def move_right(board):
    return move(board)

def move_down(board):
    board = rotate_counterclockwise(board)
    board = move(board)
    return rotate_clockwise(board)

def move_left(board):
    board = reverse_board(board)
    board = move(board)
    return reverse_board(board)   

def move_up(board):
    board = rotate_clockwise(board)
    board = move(board)
    return rotate_counterclockwise(board)
    
def move_where(board, move):
    newboard = cp.deepcopy(board)
    match move:
        case "up":
            newboard = move_up(newboard)
        case "right":
            newboard = move_right(newboard)
        case "down":
            newboard = move_down(newboard)
        case "left":
            newboard = move_left(newboard)
    return newboard

def place_where(board, available_tiles):
    newboard = cp.deepcopy(board)
    newboard[available_tiles[1]][available_tiles[2]] = available_tiles[0]
    return newboard



# SCORE EVALUATION AND HEURISTICS --------------------------------------

WEIGHT_PREFERENCE  = [[1,2,3,4],
                        [11,8,8,11],
                        [22,18,18,22],
                        [35,34,33,30]
                    ]


def max_num(board):
    m = [0,0,0,0] 
    for i in range(len(board)):
        m[i] = max(board[i])
    return max(m)

    
def span(board, length):
    #arrange all element of board in decreasing order
    
    order = [[0,0,0,0]] * 4
    order = [(board[i][j],i,j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] != 0]
    order.sort(reverse = True)
    
    #Evaluate the distance between elements:

    order = order[:length]
    total_span = 0

    for n in range(len(order) - 1):

        y = order[n][1] - order[n+1][1]

        x = order[n][2] - order[n+1][2]
        
        dist = math.sqrt(x ** 2 + y ** 2)

        total_span += dist
    
    return total_span

def corner(board):
    m = max_num(board)
    value = 0
    if m == board[0][0] or m == board[0][3] or m == board[3][0] or m == board[3][3]:
        value = 50
    elif m == board[1][1] or m == board[1][2] or m == board[2][1] or m == board[2][2]:
        value = 0
    value = 25
    return value

def monotonicity(board):
    rot_board = rotate_clockwise(board)
    mono = 0
    for i in range(4):
        for j in range(4):
            array = rot_board[j][: 4-i] + board[i][j:]
            if array == sorted(array, reverse = True): 
                mono += 1
    return mono


def evaluate(board):
    #For one board
    sum = 0
    occupied_tiles = 0
    for i in range(len(board)):
        for j in range (len(board)):
            if board[i][j] != 0: 
                occupied_tiles += 1
                sum += int(board[i][j]) * WEIGHT_PREFERENCE[i][j]  

    return ((sum) + monotonicity(board) + corner(board) - span(board, 8)) / occupied_tiles                        
    #return ((sum * 20) - (span(board, 8) * 2) + (corner(board) * 10) + (monotonicity(board) * 1.5)) / occupied_tiles      

#MINIMAX ALGORITHM ------------------------------------------------

def maximize(board, alpha, beta, depth):
    if depth == 0 or is_the_game_lost(board):
        return None, evaluate(board)

    max_position, max_score = None, float('-inf')
    for move in available_player_moves(board):
        child = move_where(board, move) 
        (_ , score) = minimize(child, alpha, beta, depth - 1)

        if max_score <= score:
            (max_position, max_score) = (child, score)

        alpha = max(alpha, score)
        if beta <= alpha:
            break
    
    return max_position, max_score




def minimize(board, alpha, beta, depth):
    if depth == 0 or is_the_game_lost(board):
        return None, evaluate(board)

    min_position, min_score = None, float('inf')
    for move in availble_bot_moves(board):
        
        child = place_where(board, move)
        ( _ , score) = maximize(child, alpha, beta, depth - 1)

        if min_score >= score:
            (min_position, min_score) = child, score
            min_position = child

        beta = min(beta, score)
        if beta <= alpha:
            break

    return min_position, min_score



def register_move(board, position):
    if move_up(board) == position:
        return 'up'
    elif move_left(board) == position:
        return 'left'
    elif move_right(board) == position:
        return 'right'
    elif move_down(board) == position:
        return 'down'


def what_is_best_move(board, depth):
    (best_move , _ ) = maximize(board, float('-inf'), float('inf'), depth)
    return register_move(board, best_move)




#PROCESS DATA ---------------------------------------------------------

#Update gameboard on browser
def find_elements(find):
    matrix = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
            ]
    
    #Read the gameboard for elements and return gameboard at 2D array
    tiles = find.findAll('div', {'class' : 'tile'})
    for string in tiles:
        string = str(string)[12:]
        f = string.split(" ")
        pos = f[2][14:].split("-")
        pos[0] = pos[0][0]
        pos[1] = pos[1][0]
        num = f[1][5:]
        matrix[int(pos[1]) - 1][int(pos[0]) - 1] = int(num)

    return matrix

def move_on_web(find, input, moves):
    find.send_keys(input[moves])
    time.sleep(0.05)
    

#MAINLOOP--------------------------------------------------------

def main():
    #Retrieve and process data
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('log-level=3')
    options.add_experimental_option('detach', True)
    launcher = webdriver.Chrome(options = options)
    launcher.get(URL)

    #Initialize all variables
    input = launcher.find_element(By.TAG_NAME, 'body')
    html = launcher.page_source
    find = BeautifulSoup(html, 'html.parser')
    available_inputs = {
        "up" : Keys.ARROW_UP,
        "down" : Keys.ARROW_DOWN,
        "left" : Keys.ARROW_LEFT, 
        "right" : Keys.ARROW_RIGHT
        }

    count = 0

    #GAMELOOP
    while True:

        #Find elements from html source
        html = launcher.page_source
        find = BeautifulSoup(html, 'html.parser')
        gameboard = find_elements(find)

        #Game Logic
        if is_the_game_lost(gameboard):
            print("I lost the game after {} moves".format(count))
            print("The highest block achieved is {}".format(max_num(gameboard)))
            break
        elif find.findAll('div', {'class' : 'game-message game-won'}) != []:
            print("WE WIN :)")
            break
        
        move = what_is_best_move(gameboard,5)
        move_on_web(input, available_inputs, move)

        count += 1
        print("Move #{}: {}".format(count, move))
              


main()