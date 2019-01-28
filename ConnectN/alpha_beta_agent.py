import math
import agent
import random
import time

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
        return self.decision(brd)

    # Calculates score for given board state.
    #
    # PARAM [board] brd: the current board state
    # PARAM [int] player: the player to score the board state for
    # RETURN [int]: the numerical score of the board state
    def calculateScore(self, brd, player):
        """Heuristic:
            - If the game can be won, return an incredibly large value
            - Otherwise, look for n - 1s in a row, returning a value corresponding to the number
                - If the n - 1 line has a blank at both ends, it is weighted far more favorably
                - If it has only one blank space at one end, it is weighted less
                - If it has no blank at the end, it is ignored because it cannot result in a win
            - Preventing opponent from winning is prioritized higher than actually winning"""

        # check if we are player1 or player2 so we can play to maximize score appropriately
        if player == 1:
            p = 1
            o = 2
        else:
            p = 2
            o = 1

        # return immediately if the board is a winning state
        if brd.get_outcome() == p:
            return 10000000
        elif brd.get_outcome() == o:
            return -20000000

        val = 0
        for col in range(0, brd.w):
            for row in range(0, brd.h):
                if brd.board[row][col] != 0:
                    short_line = self.is_any_short_line_at(brd, col, row)
                    if short_line:  # We don't care if there is no n-1 line
                        space_before = self.is_any_space_before(brd, col, row)
                        if space_before and short_line:  # Assigns significantly higher score if space before and after
                            multiplier = 5
                        else:
                            multiplier = 1
                        if brd.board[row][col] == p:  # Checks appropriate token based on player
                            val += 1000 * multiplier
                        else:
                            val -= 2000 * multiplier
        return val

    def minimize(self, brd, n, alpha, beta, player):
        if n == 0:
            return (None, self.calculateScore(brd, player))
        (minChild, minUtil) = (None, float('inf'))
        for b in self.get_successors(brd):
            (x, util) = self.maximize(b[0], n - 1, alpha, beta, player)  # here, x is useless, just holds place of tuple
            if util < minUtil:
                (minChild, minUtil) = (b, util)
            if minUtil <= alpha:
                break
            if minUtil <= beta:
                beta = minUtil
        return (minChild, minUtil)

    def maximize(self, brd, n, alpha, beta, player):
        #  This should ONLY stop if n is terminal
        if n == 0:
            return (None, self.calculateScore(brd, player))
        (maxChild, maxUtil) = ((0, None), float('-inf'))
        for b in self.get_successors(brd):
            (x, util) = self.minimize(b[0], n - 1, alpha, beta, player)  # here, x is useless, just holds place of tuple
            if util > maxUtil:
                (maxChild, maxUtil) = (b, util)
            if maxUtil >= beta:
                break
            if maxUtil >= alpha:
                alpha = maxUtil
        return (maxChild, maxUtil)

    def decision(self, brd):
        start_time = time.time()
        global bestmove
        global bestscore
        bestmove = 0
        bestscore = 0
        # Iterative deepening
        for i in range(1, self.max_depth + 1):
            (child, state) = self.maximize(brd, i, float('-inf'), float('inf'), brd.player)
            if state <= -20000000:
                return child[1]
            if state >= 10000000:
                return child[1]
            if state > bestscore:
                bestscore = state
                bestmove = child
            else:
                bestmove = child
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:
                break
        return bestmove[1]

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

    #  todo: assign values to lines? maybe return 1 for 1 space, 2 for 2, 0 for 0
    def is_short_line_at(self, brd, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (brd.n - 1) * dx >= brd.w) or
            (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)):
            return False
        # Get token at (x,y)
        t = brd.board[y][x]
        if t == 0:
            return False
        # Go through elements

        if not self.check_space_after:  # We ONLY care if there is a blank space at end
            return False
        # todo: check space before line for openness and fix above function%^^^^ maybe write helpers?
        # if y - dy >= 0 and x - abs(dx): #ch
        #   if brd.board[y - dy][x - dx] != 0:
        #       return False

        split = False

        for i in range(1, brd.n):
            symbol = brd.board[y + i * dy][x + i * dx]
            if symbol != t:
                if symbol == 0:
                    if split:
                        return False
                    if not split:
                        split = True
                else:
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
                self.is_short_line_at(brd, x, y, 1, -1))  # Diagonal down

    def check_space_before(self, brd, x, y, dx, dy):
        # Horizontal:
        if dx == 1 and dy == 0:
            if x >= 1:
                return brd.board[y][x - 1] == 0
            return False
        # If vertical, we don't have to check; because of how connect4 is played, there will never be a token
        # with an open space directly+ below it.
        if dx == 0 and dy == 1:
            return False
        # Diagonal up
        if dx == 1 and dy == 1:
            if y >= 1 and x >= 1:
                return brd.board[y - 1][x - 1] == 0
            return False
        # Diagonal up
        if dx == 1 and dy == -1:
            if y < brd.h - 1 and x >= 1:
                return brd.board[y + 1][x - 1] == 0
            return False
        # in case anything REALLY wacky happens
        return False

    def check_space_after(self, brd, x, y, dx, dy):
        # Horizontal:
        if dx == 1 and dy == 0:
            if x + brd.n < brd.w:
                return brd.board[y][x + brd.n] == 0
            return False
        if dx == 0 and dy == 1:
            if y + brd.n < brd.h:
                return brd.board[y + brd.n][x]
            return False
        # Diagonal up
        if dx == 1 and dy == 1:
            if y + brd.n < brd.h and x + brd.n < brd.h:
                return brd.board[y + brd.n][x + brd.n] == 0
            return False
        # Diagonal up
        if dx == 1 and dy == -1:
            if y - brd.n < brd.h and x + brd.n < brd.h:
                return brd.board[y - brd.n][x + brd.n] == 0
            return False
        # in case anything REALLY wacky happens
        return False

    # Check if there is a blank space before line of characters in any direction
    #
    # PARAM [int] x: the x coordinate of the starting cell
    # PARAM [int] y: the y coordinate of the starting cell
    # RETURN [Bool]: True if space exists before given coordinates, False otherwise

    def is_any_space_before(self, brd, x, y):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        return (self.check_space_before(brd, x, y, 1, 0) or  # Horizontal
                self.check_space_before(brd, x, y, 0, 1) or  # Vertical
                self.check_space_before(brd, x, y, 1, 1) or  # Diagonal up
                self.check_space_before(brd, x, y, 1, -1))  # Diagonal down

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