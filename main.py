#!/usr/bin/env python3
import argparse
import numpy as np
import sys

NUMBERS = {i for i in range(1, 10) }
POSITIONS = {i for i in range(0, 8) }
BLOCKS = [tuple((i + b1, j + b2) for i in range(3) for j in range(3))
          for b1 in range(0,8,3) for b2 in range(0, 8, 3)]

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('sudoku_string', action="store",
    #                     help='sudoku string to be parsed')
    parser.add_argument('-verbose', action="store_true",
                        help='boolean for verbose output',
                        default=False)

    args = parser.parse_args()
    sudoku = sys.stdin
    matrix = check_sudoku(sudoku)
    solution = solve_sudoku(matrix, args.verbose)
    print_sudoku(matrix)

def check_sudoku(input):
    if not input:
        raise ValueError(""" The sudoku is not valid. """)

    input_l = []
    for line in input:
        input_l.append([item for item in parse_int(line)])

    matrix = np.asarray(input_l)

    return matrix

def parse_int(inputstring):
    for i in inputstring:
        if i == '_':
            yield 0
        elif i.isdigit():
            yield int(i)
        else:
            continue

def solve_sudoku(sudoku, verbose):

    possible_positions = build_possible_positions(sudoku)
    open_spots = len(possible_positions.keys())
    print(f'startpoint. Open spots: {open_spots}.\n')

    open_spots_current = fill_guaranteed(sudoku, possible_positions,
                                         open_spots, verbose)

    if open_spots_current < open_spots:
        print(f'\nCurrent open spots: {open_spots_current}')
        open_spots = open_spots_current

    return sudoku

def fill_guaranteed(sudoku, possible_positions, open_spots, verbose=False):

    filling_guarenteed = True

    while(filling_guarenteed):

        filling_guarenteed = False
        possible_positions = build_possible_positions(sudoku)

        for key in sorted(possible_positions,
                          key=lambda k: len(possible_positions[k]),
                          reverse=True):
            if len(possible_positions[key]) == 1:
                filling_guarenteed = True
                val = possible_positions[key].pop()
                sudoku[key] = val

                if verbose:
                    print(f'filled in {key} with {val}.')
                break

        open_spots_current = len(possible_positions.keys())

    return open_spots_current

def build_possible_positions(sudoku):
    possibles = {tuple((col,row)) : {} for col in POSITIONS for row in POSITIONS
                 if sudoku[row][col] == 0}

    for col, item_list in enumerate(sudoku):
        for row, item in enumerate(item_list):
            if item == 0:
                possibles[(col, row)] = possible_per_spot(sudoku, col, row)

    return possibles

def possible_per_spot(m, col, row):
    block_i = 0

    for block in BLOCKS:

        if tuple((col, row)) in block:
            break

        block_i += 1

    block = [m[b] for b in BLOCKS[block_i]]
    possible = {i for i in NUMBERS if not i in m[col, :] and
                                      not i in m[:, row] and
                                      not i in block}

    return possible

def print_sudoku(sudoku):
    print('\nSolution!')
    for item_list in sudoku:
        print("-" * 37)
        for item in item_list:
            print(f"| {item} ", end="")
        print("|")
    print("-" * 37,'\n')

if __name__ == "__main__":
    main()
