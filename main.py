#!/usr/bin/env python3
"""
The module below implements a Sudoku Solver, using a stack.
Refer to the -h option the the program to get help on how to run it.
"""

__author__ = """Leo Schreuder & Pim van Helvoirt"""
__copyright__ = "None"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.7"
__maintainer__ = ""
__email__ = "leoschreuders@hotmail.com pim.van.helvoirt@home.nl"
__status__ = "Working"

import argparse
import math
import sys
import collections
import time

NUMBERS = 0
POSITIONS = 0
BLOCKS = 0

def parse_sudoku(file):
    """ parses a sudoku from a given file """

    parsed = []

    try:
        with open(file) as f:
            for line in f:
                parsed.append([item for item in parse_int(line)])
    except IOError:
        raise ValueError(""" The sudoku file is not there, please"""
                         """ give a file to read from. """)
    size = len(parsed)

    if not size:
        raise ValueError(""" The sudoku file is empty, please"""
                         """ give a file to read from. """)

    if not len(parsed) == len(parsed[0]):
        raise ValueError("""The sudoku should be square. Current size is"""
                         f""" {len(parsed)} by {len(parsed[0])}""")

    block_size = int(math.sqrt(len(parsed)))

    # store static attributes of the sudoku as globals, for more readable code.
    global NUMBERS
    global POSITIONS
    global BLOCKS

    # define the possible numbers, the positions and blocks for the sudoku.
    NUMBERS = {i for i in range(1, size + 1)}
    POSITIONS = {i for i in range(1, size)}
    BLOCKS = [tuple((j + b1, i + b2) for i in range(block_size)
                    for j in range(block_size))
              for b1 in range(0, size, block_size)
              for b2 in range(0, size, block_size)]

    return parsed


def parse_int(inputstring):
    """ returns numbers in a given string as ints """

    for i in inputstring.split():
        if i == '_':
            yield 0
        elif i.isdigit():
            yield int(i)
        else:
            raise ValueError('The input could not be parsed wrong characters.')


def solve_sudoku(sudoku, verbose, experiment):
    """ solve a given sudoku grid, returns a solved grid
        if the sudoku is unsolvable, it returns the original one"""

    possible_positions = build_possible_positions(sudoku)

    open_spots = len(possible_positions.keys())

    if verbose:
        print(f'startpoint. Open spots: {open_spots}.\n')

    if experiment:
        su2 = [row[:] for row in sudoku]

        start_time = time.time()
        solve_stack(su2, verbose, dumb=True)
        end_time = time.time()
        print("----------")
        print(f"Without optimization: {end_time - start_time} s")

    start_time = time.time()
    solved = solve_stack(sudoku, verbose)
    end_time = time.time()
    if experiment:
        print("----------")
        print(f"With optimization: {end_time - start_time} s")

    return solved


def solve_stack(sudoku, verbose=False, dumb=False):
    """ Takes a sudoku as arguments and returns a solved sudoku """

    # Make a stack with the given sudoku on top
    stack = collections.deque([sudoku])

    # While there is still a sudoku on the stack, take the top one
    while stack:
        if verbose:
            print(f"current size of stack {len(stack)}\n")

        top = stack.pop()
        open_spots, possible_positions = fill_guaranteed(top)

        if (open_spots == 0):
            return top
        else:
            if possible_positions:
                # Stop als er een oninvulbaar vakje is
                if len(possible_positions) == open_spots:

                    if dumb:
                        key = list(possible_positions.keys())[0]
                    else:
                        key = sorted(possible_positions, key=lambda k:
                                     len(possible_positions[k]))[0]

                    possibles = possible_positions[key]
                    row, col = key

                    for possible in possibles:

                        sudoku_next = [row[:] for row in top]
                        sudoku_next[row][col] = possible

                        stack.append(sudoku_next)
                else:

                    if verbose:
                        print("faulty sudoku:")
                        dirty_print_sudoku(top)
                        print("")

    return sudoku


def fill_guaranteed(sudoku, verbose=False):
    """ fills in guaranteed values in a sudoku,
        until no longer possible """

    filling_guarenteed = True

    while(filling_guarenteed):

        filling_guarenteed = False

        possible_positions = build_possible_positions(sudoku)
        open_spots_current = len(possible_positions.keys())

        # walk over the keys in the possible positions dictionary
        for key in sorted(possible_positions,
                          key=lambda k: len(possible_positions[k]),
                          reverse=True):

            # drop filled in positions from the dictionary
            if not possible_positions[key]:
                possible_positions.pop(key)

            # if there is only one possible value, fill it in.
            elif len(possible_positions[key]) == 1:

                # flip bool to true to retry filling in a value.
                filling_guarenteed = True

                val = possible_positions[key].pop()

                # unpack key and fill in value.
                row, col = key
                sudoku[row][col] = val

                if verbose:
                    print(f'filled in {key} with {val}.')

                break
    if verbose:
        print('\ncurrent open spots:', open_spots_current)

    return open_spots_current, possible_positions


def build_possible_positions(sudoku):
    """ build a dict with (col, row): possible values from a given sudoku """
    possibles = {}

    for row, _ in enumerate(sudoku):
        for col, item in enumerate(_):
            if item == 0:
                possibles[(row, col)] = possible_per_spot(sudoku, row, col)

    return possibles


def possible_per_spot(su, row, col):
    """ return the possible values for a spot in the sudoku """

    possible = {i for i in NUMBERS if i not in get_column(su, col) and
                i not in get_row(su, row) and
                i not in get_block(su, row, col)}

    return possible


def get_row(su, i):
    """ get the ith row of the sudoku """
    return su[i]


def get_column(su, i):
    """ get the ith column of the sudoku """

    return [su[j][i] for j in range(len(su))]


def get_block(m, row, col):
    """ get the values in the block in which the col and row fall. """
    block_i = 0

    for block in BLOCKS:

        if not tuple((row, col)) in block:
            block_i += 1
        else:
            break

    block = [m[j][i] for (j, i) in BLOCKS[block_i]]

    return block


def is_valid(sudoku):
    """ check whether a given sudoku is a valid sudoku """

    for i in range(len(sudoku)):
        for j in range(len(sudoku)):

            if not (sorted(get_row(sudoku, i)) ==
                    sorted(get_column(sudoku, j)) ==
                    sorted(get_block(sudoku, i, j)) ==
                    sorted(NUMBERS)):
                return False
    return True


def dirty_print_sudoku(sudoku):
    """ print only the numbers """
    for item_list in sudoku:
        for item in item_list:
            print(f'{item} ', end='')
        print('')


def pretty_print_sudoku(sudoku):
    """ print some additional stuff next to only numbers """
    add_lines = 0

    if len(sudoku) == 16:
        add_lines = 1

    print('\nSolution!')
    for item_list in sudoku:
        print('-' * len(sudoku) * (4 + add_lines))
        for item in item_list:
            out = f'| {item} '
            if item < 9 and add_lines:
                out += ' '
            print(out, end="")
        print('|')
    print('-' * len(sudoku) * (4 + add_lines), '\n')


def main():
    # define an argument parser
    # consult -h for help
    parser = argparse.ArgumentParser()
    parser.add_argument('sudoku_string', action="store",
                        help='sudoku string to be parsed.')
    parser.add_argument('-verbose', action="store_true",
                        help='boolean for verbose output',
                        default=False)
    parser.add_argument('-prettyprint', action="store_true",
                        help='boolean to pretty print.',
                        default=False)
    parser.add_argument('-experiment', action="store_true",
                        help='boolean to run an optimization experiment.',
                        default=False)

    # parse arguments
    args = parser.parse_args()
    su, pretty, verbose, experiment = (args.sudoku_string, args.prettyprint,
                                       args.verbose, args.experiment)

    su = parse_sudoku(su)

    solved = solve_sudoku(su, verbose, experiment)

    if not is_valid(solved):
        raise ValueError("""The sudoku provided as input is not valid.""")
        sys.exit()

    if pretty:
        pretty_print_sudoku(solved)
    else:
        dirty_print_sudoku(solved)

    return 0


if __name__ == "__main__":
    main()
