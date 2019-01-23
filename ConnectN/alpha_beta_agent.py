import math
import agent

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
        # Your code here

        # (boards, cols) = self.get_successors(brd)

        # return cols[max(boards)]
        return 2

    def calculateScore(self, brd):
        """Heuristic:
            - If the game can be won, do so immediately.
            - Otherwise, look for n - 1s in a row, n - 2s in a row, etc, scoring proportionally"""
        for col in range(0, brd.w):
            for row in range(0, brd.h):
                if brd.board[row][col] != 0:
                    if brd.is_any_line_at(col, row):
                        return 10000

        # Next, need to check for n-1 in a row.

        return 0

    # Return the a list of the n-th level successors of the given board.
    # PARAM brd: a board to recursively get succesors for
    # PARAM n: the level to go til
    # RETURN list of (board.Board)
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
                #print(b[0].board)
                #print("\n")






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
