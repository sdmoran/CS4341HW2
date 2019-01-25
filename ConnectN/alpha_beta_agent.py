import math
import agent
import random

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        levels = 4

        """Search for the best move (choice of column for the token)"""
        # Selects best move for agent to make based on calculateScore() function.
        return self.get_best_col(brd, levels)



        # return cols[max(boards)]

    def calculateScore(self, brd):
        """Heuristic:
            - If the game can be won, do so immediately.
            - Otherwise, look for n - 1s in a row, n - 2s in a row, etc, scoring proportionally"""
        val = 0 # this should depend on whether we are looking for max or min
        for col in range(0, brd.w):
            for row in range(0, brd.h):
                if brd.board[row][col] != 0:
                    if brd.is_any_line_at(col, row): # check for win
                        return 100000
                    if self.is_any_short_line_at(brd, col, row): # check for n-1 in a row
                        val += 1000
        if brd.player == 1:
            return val
        else:
            return val * -1

    # Return the list of the n-th level successors of the given board.
    # PARAM brd: a Board to recursively get successors for
    # PARAM n: the level to go til
    # RETURN tuple of [list of Board.board]
    def getRecursiveSuccessors(self, brd, n):
        children = []
        #print("LEVEL: " + str(n))
        if n <= 1:
            #print(self.get_successors(brd))
            return(self.get_successors(brd))
        else:
            for b in self.get_successors(brd):
                for c in self.getRecursiveSuccessors(b[0], n - 1):
                    children.append(c)
        return children


    def get_best_col(self, brd, n):
        board_tuples = self.get_successors(brd)
        maxcol = 0
        maxval = 0

        for t in board_tuples:
            val = self.alphaBeta(t[0], n, float('-inf'), float('inf'), 1)
            if  val > maxval:
                maxval = val
                maxcol = t[1]
        print("Max value: " + str(maxval))
        print("Max col: " + str(maxcol))
        if maxval == 0:
            return random.randint(0, brd.w - 1)
        return maxcol



    def alphaBeta(self, brd, n, alpha, beta, player):
        # todo find more elegant solution fo checking if we won
        currentScore = self.calculateScore(brd)
        if n == 0 or currentScore >= 10000:
            return currentScore
        # We don't want to return the actual value, we want to return
        # the column number at the top level that results in highest value
        # So if it's the top level....
        # - We get successors of initial board state
        # - Then run alphaBeta on THOSE
        # - Get max
        # - Return index of max
        # - Probably a job for another method!
        if player == 1:
            maxval = float('-inf')
            for b in self.get_successors(brd):
                maxval = max(maxval, self.alphaBeta(b[0], n - 1, alpha, beta, 2))
                alpha = max(alpha, maxval)
                if alpha > beta:
                    break
            return maxval
        else:
            minval = float('inf')
            for b in self.get_successors(brd):
                minval = min(minval, self.alphaBeta(b[0], n - 1, alpha, beta, 1))
                beta = min(beta, minval)
                if alpha > beta:
                    break
            return minval

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

    def is_short_line_at(self, brd, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (brd.n - 1) * dx >= brd.w) or
            (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)):
            return False
        # Get token at (x,y)
        t = brd.board[y][x]
        # Go through elements
        for i in range(1, brd.n - 1):
            if brd.board[y + i * dy][x + i * dx] != t:
                return False
        return True

    # Check if a line of identical tokens exists starting at (x,y) in any direction
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_any_short_line_at(self, brd, x, y):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        return (self.is_short_line_at(brd, x, y, 1, 0) or  # Horizontal
                self.is_short_line_at(brd, x, y, 0, 1) or  # Vertical
                self.is_short_line_at(brd, x, y, 1, 1) or  # Diagonal up
                self.is_short_line_at(brd, x, y, 1, -1)) # Diagonal down

    # Calculate the game outcome.
    #
    # RETURN [int]: 1 for Player 1, 2 for Player 2, and 0 for no winner
    def get_outcome(self):
        """Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner"""
        for x in range(self.w):
            for y in range(self.h):
                if (self.board[y][x] != 0) and self.is_any_short_line_at(x,y):
                    return self.board[y][x]
        return 0