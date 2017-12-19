
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diagonal_units = [[rows[i] + cols[i] for i in range(len(rows))],
                  [rows[-(i+1)] + cols[i] for i in range(len(rows))]]
unitlist = unitlist + diagonal_units 

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(dictionary):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    # find all boxes with two values
    for unit in unitlist:
        pairs = [box for box in unit if len(dictionary[box]) == 2]
        if len(pairs) > 1:
            twin_dict = {} # pair_value as a key, list of pair as a value
            for pair in pairs:
                pair_value = dictionary[pair]
                if pair_value in twin_dict:
                    twin_dict[pair_value].append(pair)
                else:
                    twin_dict[pair_value] = [pair]
            # remove key with the number of pairs != 2
            naked_twins = {k: v for k, v in twin_dict.items() if len(v) == 2}
            # if there is naked twins, get all values of naked twins
            if naked_twins:
                naked_twins_values = ''
                for v in naked_twins:
                    naked_twins_values = naked_twins_values + v
                # eliminate the values of the naked twins from non-twins values
                for box in unit:
                    if len(dictionary[box])>2:
                        for digit in dictionary[box]:
                            if digit in naked_twins_values:
                                dictionary[box] = dictionary[box].replace(digit,'')
    return dictionary


def eliminate(dictionary):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    solved_values = [box for box in dictionary.keys() if len(dictionary[box]) == 1]
    for box in solved_values:
        digit = dictionary[box]
        for peer in peers[box]:
            dictionary[peer] = dictionary[peer].replace(digit,'')
    return dictionary


def only_choice(dictionary):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in dictionary[box]]
            if len(dplaces) == 1:
                dictionary[dplaces[0]] = digit
    return dictionary


def reduce_puzzle(dictionary):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in dictionary.keys() if len(dictionary[box]) == 1])
        # Use the Eliminate Strategy
        dictionary = eliminate(dictionary)
        # Use the Only Choice Strategy
        dictionary = only_choice(dictionary)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in dictionary.keys() if len(dictionary[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in dictionary.keys() if len(dictionary[box]) == 0]):
            return False
    return dictionary


def search(dictionary):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    
    # First, Iterate eliminate() and only_choice() using the previous procedure
    dictionary = reduce_puzzle(dictionary)
    if dictionary is False:
        return False ## Failed earlier
    if all(len(dictionary[s]) == 1 for s in boxes): 
        return dictionary ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(dictionary[s]), s) for s in boxes if len(dictionary[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, 
    # and if one returns a value (not False), return that answer!
    for value in dictionary[s]:
        new_sudoku = dictionary.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
