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

        val = 0
        # ==== This appears to be the final piece. AlphaBeta now consistently wins at depth >= 4! ====
        # Checks if the opponent has won and it is now the AI player's turn, meaning it WAS the opponent's turn
        # previously, and it was allowed to win.
        if brd.get_outcome() == o and brd.player == p:
            val -= 20000000
        # Checks if the player we want to win has won and it is now the opponent's turn, meaning it WAS the AI's turn
        # in the previous turn, allowing it to win immediately.
        elif brd.get_outcome() == p and brd.player == o:
            val += 10000000

        for col in range(0, brd.w):
            for row in range(0, brd.h):
                symbol = brd.board[row][col]
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

    # Calculate minimum score from current board state.
    #
    # PARAM [board] brd: the current board state
    # PARAM [int] n: the depth to search to
    # PARAM [int] alpha: the alpha value
    # PARAM [int] beta: the beta value
    # PARAM [int] player: the current player
    # RETURN [tuple] (minChild, minUtil): the current child with the minimum heuristic value
    def minimize(self, brd, n, alpha, beta, player):
        if n == 0:
            return (None, self.calculateScore(brd, player))
        (minChild, minUtil) = (None, float('inf'))
        for b in self.get_successors(brd):
            # Need to flip player in maximize!
            (x, util) = self.maximize(b[0], n - 1, alpha, beta, player)  # here, x is useless, just holds place of tuple
            if util < minUtil:
                (minChild, minUtil) = (b, util)
            if minUtil <= alpha:
                break
            if minUtil <= beta:
                beta = minUtil
        return (minChild, minUtil)

    # Calculate maximum score from current board state.
    #
    # PARAM [board] brd: the current board state
    # PARAM [int] n: the depth to search to
    # PARAM [int] alpha: the alpha value
    # PARAM [int] beta: the beta value
    # PARAM [int] player: the current player
    # RETURN [tuple] (maxChild, maxUtil): the current child with the maximum heuristic value
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

    # Decide which move to make from current board state.
    #
    # PARAM [board] brd: the current board state
    # RETURN [int]: which column to place the next piece in
    def decision(self, brd):
        start_time = time.time()
        global bestmove
        global bestscore
        bestmove = 0
        bestscore = 0
        # Iterative deepening
        for i in range(0, self.max_depth + 1):
            (child, state) = self.maximize(brd, i, float('-inf'), float('inf'), brd.player)
            # if state <= -2000000:
            #     return child[1]
            # if state >= 1000000:
            #     return child[1]
            if state > bestscore:
                bestscore = state
                bestmove = child
            else:
                bestmove = child
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:  # This could be as high as 15, technically, but we use 10 just in case
                break
        if bestmove[1] is not None:
            return bestmove[1]
        # If we DON'T find a best move, select one randomly from the list of legal columns. This is quite a corner case,
        # essentially should only occur if board is nearly/completely full.
        else:
            return random.choice(brd.free_cols())

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

    # Determines if a line of length n - 1 exists at coordinates (x, y) in direction (dx, dy).
    #
    # PARAM [board] brd: the current board state
    # PARAM [int] x: the x coordinate to start from
    # PARAM [int] y: the y coordinate to start from
    # PARAM [int] dx: the x direction to check
    # PARAM [int] dy: the y direction to check
    # RETURN [bool]: True if line exists, otherwise False
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

        # Accounts for lines that are split in the middle, like 1 1 0 1
        split = False

        # Special check for horizontal: we don't care if there is 1 1 0 1 if the column below 0 is empty

        for i in range(1, brd.n):
            symbol = brd.board[y + i * dy][x + i * dx]
            if symbol != t:
                if symbol == 0:
                    if y >= 1:
                        if dx == 1 and dy == 0:  # We don't care if this split line is unplayable, checks that
                            if brd.board[y - 1][x + i] == 0:
                                return False
                    if split:
                        return False
                    if not split:
                        split = True
                else:
                    return False
        return True

    # Check if a line of identical tokens of length n - 1 exists starting at (x,y) in any direction
    #
    # PARAM [board] brd: the current board state
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # RETURN [Bool]: True if n - 1 tokens of the same type have been found with space at end, False otherwise
    def is_any_short_line_at(self, brd, x, y):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        return (self.is_short_line_at(brd, x, y, 1, 0) or  # Horizontal
                self.is_short_line_at(brd, x, y, 0, 1) or  # Vertical
                self.is_short_line_at(brd, x, y, 1, 1) or  # Diagonal up
                self.is_short_line_at(brd, x, y, 1, -1))  # Diagonal down

    # Check if a blank space exists before the start of the line that begins at given coordinates in given direction
    #
    # PARAM [board] brd: the current board state
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the x direction
    # PARAM [int] dy: the y direction
    # RETURN [Bool]: True if space exists, False otherwise
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

    # Check if a blank space exists after the end of the line that begins at given coordinates in given direction
    #
    # PARAM [board] brd: the current board state
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the x direction
    # PARAM [int] dy: the y direction
    # RETURN [Bool]: True if space exists, False otherwise
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
        return ((self.is_short_line_at(brd, x, y, 1, 0) and
                self.check_space_before(brd, x, y, 1, 0)) or  # Horizontal
                (self.is_short_line_at(brd, x, y, 0, 1) and
                self.check_space_before(brd, x, y, 0, 1)) or  # Vertical
                (self.is_short_line_at(brd, x, y, 1, 1) and
                self.check_space_before(brd, x, y, 1, 1)) or
                (self.is_short_line_at(brd, x, y, 1, -1) and# Diagonal up
                self.check_space_before(brd, x, y, 1, -1)))  # Diagonal down

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

THE_AGENT = AlphaBetaAgent("MoranSamuel", 2)