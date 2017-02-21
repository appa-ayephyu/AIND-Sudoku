assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows= "ABCDEFGHI"
cols = "123456789"

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units1 = [['A1','B2','C3','D4','E5','F6','G7','H8','I9']]
diagonal_units2 = [['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
unitlist = row_units + column_units + square_units + diagonal_units1 + diagonal_units2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    for unit in unitlist:
        nakedTwins ={}
        for box in unit:
            if len(values[box]) == 2:
                for peer in unit:
                    if peer != box and values[peer]==values[box]:
                        nakedTwins[0] = box
                        nakedTwins[1] = peer
        if len(nakedTwins)==2 and values[nakedTwins[0]]==values[nakedTwins[1]]:
            for box in unit:
                if box!=nakedTwins[0] and box!=nakedTwins[1]:
                    assign_value(values, box, values[box].replace(values[nakedTwins[0]][0],''))
                    assign_value(values, box, values[box].replace(values[nakedTwins[0]][1],''))

    return values


    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    result = {}
    count = 0
    for box in boxes:
        if grid[count] == '.':
            result[box] = '123456789'
        else:
            result[box] = grid[count]
        count = count +1
    return result

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for key,val in values.items():
        if len(val) == 1:
            for peer in peers[key]:
                assign_value(values,peer,values[peer].replace(val,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for i in '123456789':
            count =0
            tmp = ''
            for box in unit:
                if i in values[box]:
                    tmp = box
                    count = count + 1
            if count == 1:
                assign_value(values,tmp,i)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values= eliminate(values)


        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        #Use Naked Twins Strategy
        value = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    
    if values is False:
        return False
    
    completed = True
    for key,val in values.items():
        if len(val) >1:
            completed = False
            break
    if completed:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    square = ''
    for key, value in values.items():
        for i in range (2,10):
            if len(value) == i:
                square = key
                break
            
    
    #if square == '':
    #    return values
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for i in range(len(values[square])):
        tmp = values.copy()
        tmp[square] = tmp[square][i]
        returnValue = search(tmp)
        if returnValue is not False:
            return returnValue

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
