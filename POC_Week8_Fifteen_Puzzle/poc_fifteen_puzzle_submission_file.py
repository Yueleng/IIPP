"""
http://www.codeskulptor.org/#user44_HMPPybg6AX_15.py

Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self._grid[target_row][target_col] != 0:
            return False
        for col in range(target_col + 1, self.get_width()):
            if self._grid[target_row][col] !=  col + self._width * target_row:
                return False
        for row in range(target_row + 1, self.get_height()):
            for col in range(self.get_width):
                if self._grid[row][col] !=  col + self._width * row:
                    return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        row, col = self.current_position(target_row, target_col)
        if row == target_row  - 1:
            if col == target_col: 
                move_string += "uld"
                return move_string
            elif col > target_col:
                move_string += "u" + "r" * (col - target_col)
                move_string += "ulldr" * (col - target_col - 1)
                move_string += "ullddru"
                move_string += "ld"
                return move_string
            elif col < target_col:
                move_string += "u" + "l" * (target_col - col)
                move_string += "urrdl" * (target_col - col - 1)
                move_string += "druld"
                return move_string
            
        if row == target_row:
            if target_col - col == 1:
                move_string += "l"
                return move_string
            else:
                move_string += "l" * (target_col - col)
                move_string += "urrdl" * (target_col - col - 1)
                return move_string
            
        if target_row - row > 1:
            if target_col == col:
                move_string += "u" * (target_row - row)
                move_string += "lddru" * (target_row - row - 1)
                move_string += "ld"
                return move_string
            elif target_col > col:
                #left
                move_string += "u" * (target_row - row) + "l" * (target_col - col)
                move_string += "drrul" * (target_col - col - 1)
                move_string += "druld" * (target_row - row)
                return move_string
            elif target_col < col:
                #right
                move_string += "u" * (target_row - row) + "r" * (col - target_col)
                move_string += "dllur" * (col - target_col - 1)
                move_string += "dlu"
                move_string += "lddru" * (target_row - row - 1)
                move_string += "ld"
                return move_string
            

        

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        target_col = 0
        move_string = ""
        row, col = self.current_position(target_row, target_col)
        if row == target_row  - 1:
            if col == target_col: 
                move_string += "u" 
                move_string += "r" * (self._width - 1)
                return move_string
            elif col - target_col == 1:
                move_string += "u"
                move_string += "ruldrdlurdluurddlu"
                move_string += "r" * (self._width - 1)
                return move_string
            elif col - target_col >= 2:
                move_string += "u" + "r" * (col - target_col)
                move_string += "ulldr" * (col - target_col - 2)
                move_string += "ulld"
                move_string += "ruldrdlurdluurddlu"
                move_string += "r" * (self._width - 1)
                return move_string
        if target_row - row >= 2:
            if col == target_col:
                move_string += "u" * (target_row - row) + "rdl"
                move_string += "druld" * (target_row - row - 2)
                move_string += "ruldrdlurdluurddlu"
                move_string += "r" * (self._width - 1)
                return move_string
                
            if col - target_col == 1:
                move_string += "u" * (target_row - row)
                move_string += "druld" * (target_row - row - 1)
                move_string += "ruldrdlurdluurddlu"
                move_string += "r" * (self._width - 1)
                return move_string
            if col - target_col >= 2:
                move_string += "u" * (target_row - row) + "r" * (col - target_col)
                move_string += "dllur" * (col - target_col - 2)
                move_string += "dllu"
                move_string += "druld" * (target_row - row - 1)
                move_string += "ruldrdlurdluurddlu"
                move_string += "r" * (self._width - 1)
                return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        start_row, start_col = self.current_position(0, 0)
        # move_string = self.solve_interior_tile(start_row, start_col)
        move_string = self.solve_col0_tile(start_row)
        return move_string 

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(5, 5))


