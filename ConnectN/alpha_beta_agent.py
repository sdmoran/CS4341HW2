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

        """Search for the best move (choice of column for the token)"""
        # Selects best move for agent to make based on calculateScore() function.
        #return self.alphaBeta(brd, self.max_depth, float('-inf'), float('inf'), brd.player, -1, -1, -1)
        return self.decision(brd)[1]

    def calculateScore(self, brd):
        """Heuristic:
            - If the game can be won, do so immediately.
            - Otherwise, look for n - 1s in a row, n - 2s in a row, etc, scoring proportionally"""

        if brd.get_outcome() == 1:
            return -1000000
        elif brd .get_outcome() == 2:
            return 1000000

        val = 0
        for col in range(0, brd.w):
            for row in range(0, brd.h):
                if brd.board[row][col] != 0:
                    if self.is_any_short_line_at(brd, col, row):  # check for n-1 in a row WITH BLANK SPACE AT END
                        if brd.player == 2:
                            val += 1000
                        else:
                            val -= 2000
        return val

    def get_best_col(self, brd, n):
        board_tuples = self.get_successors(brd)
        maxcol = 0
        maxval = 0

        for t in board_tuples:
            val = self.alphaBeta(t[0], n, float('-inf'), float('inf'), 1, -1, -1, -1)
            if  val > maxval:
                maxval = val
                maxcol = t[1]
        print("Max value: " + str(maxval))
        print("Max col: " + str(maxcol))
        if maxval == 0:
            return random.randint(0, brd.w - 1)
        return maxcol

    def minimize(self, brd, n, alpha, beta):
        currentScore = self.calculateScore(brd)
        if n == 0 or currentScore >= abs(100000):
            return (None, currentScore)
        (minChild, minUtil) = (None, float('inf'))
        for b in self.get_successors(brd):
            (x, util) = self.maximize(b[0], n - 1, alpha, beta) #here, x is useless, just holds place of tuple elt
            if util < minUtil:
                (minChild, minUtil) = (b, util)
            if minUtil <= alpha:
                break
            if minUtil <= beta:
                beta = minUtil
        return (minChild, minUtil)

    def maximize(self, brd, n, alpha, beta):
        currentScore = self.calculateScore(brd)
        if n == 0 or currentScore >= abs(100000):
            return (None, currentScore)
        (maxChild, maxUtil) = (None, float('-inf'))
        for b in self.get_successors(brd):
            (x, util) = self.minimize(b[0], n - 1, alpha, beta)  # here, x is useless, just holds place of tuple elt
            if util > maxUtil:
                (maxChild, maxUtil) = (b, util)
            if maxUtil >= beta:
                break
            if maxUtil >= alpha:
                alpha = maxUtil
        return (maxChild, maxUtil)

    def decision(self, brd):
        (child, state) = self.maximize(brd, self.max_depth, float('-inf'), float('inf'))
        return child





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
        if brd.board[y + (brd.n - 1) * dy][x + (brd.n - 1) * dx] != 0: # We ONLY care if there is a blank space at the end
            return False

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