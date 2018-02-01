import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """
    
    def __init__(self, puzzle_height, puzzle_width, initial_grid = None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row] for col in range(self._width)
                     for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representation for puzzle
        Return a string
        """
        ans = ""
        for row in range(self._height):
            ans += str[self.grid[row]]
            ans += "\n"
        return ans

    #######################################################
    # GUI methods

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_number(self, row, col):
        return self._grid[row][col]

    def set_number(self, row, col, value):
        self._grid[row][col] = value
    
    def clone(self):
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ################################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        """
        solved_value = (solved_col + solved_row * self._width)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Update the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0,0)
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
                zero_col +=1 

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

    #####################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        


