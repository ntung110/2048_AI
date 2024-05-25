# Grid Module
from constants import *
from row_ops import merge_row_left, merge_row_right

def transpose(grid):
    trans =  [*zip(*grid)]
    trans = [list(zip_itm) for zip_itm in trans]
    return trans

def identity(grid):
    return grid

MERGE_DICT = {'left' : (identity, merge_row_left),
              'right' : (identity, merge_row_right),
              'up' : (transpose, merge_row_left),
              'down' : (transpose, merge_row_right)}

def merge(grid, dir):

    # Specify operations on grid and rows based on direction
    grid_op = MERGE_DICT[dir][0]
    merge_op = MERGE_DICT[dir][1]
    
    # Perform operations on grid and row
    prep = grid_op(grid)
    transform = []
    for row in prep:
        new_row = merge_op(row)
        transform.append(new_row)
    new_grid = grid_op(transform)

    return new_grid


board = [[2,2,4,8],
         [2,4,0,0],
         [0,0,4,0],
         [2,0,8,8]]

print(merge(board, 'down'))

