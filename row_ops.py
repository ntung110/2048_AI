# Move Mechanics

from constants import *
from collections import deque

def remove_zeros(row) -> list[int]:
    return [itm for itm in row if itm != 0]

def merge_row_right(row) -> list[int]:
    # Remove all zeros from row
    non_zero = remove_zeros(row)
    merged = [0] * len(row)
    cnt = len(row) - 1

    # Begin merging to the right
    while non_zero:
        itm = non_zero.pop()
        if non_zero and (itm == non_zero[-1]):
            merged[cnt] = itm * 2
            non_zero.pop()
        else:
            merged[cnt] = itm
        cnt -= 1

    return merged

def merge_row_left(row) -> list[int]:
    deq = deque(remove_zeros(row))
    merged = [0] * len(row)
    cnt = 0

    while deq:
        itm = deq.popleft()
        if deq and (itm == deq[0]):
            merged[cnt] = itm * 2
            deq.popleft()
        else:
            merged[cnt] = itm
        cnt += 1

    return merged

def can_merge_right(row) -> bool:
    # Check if zero exist in row
    non_zero = remove_zeros(row)
    while non_zero:
        itm = non_zero.pop()

    return False
    

# def can_merge_left(row) -> bool: