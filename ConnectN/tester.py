import board
import alpha_beta_agent as aba

brd = [
    [1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

empty = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

wbrd = [
    [2, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

b1 = board.Board(brd, 5, 4, 4)

win = board.Board(wbrd, 5, 4, 4)

blank = board.Board(empty, 5, 4, 4)


agent = aba.AlphaBetaAgent("Jeffery", 5)

# If game is already won, then method to calculate which column to move next will return 0, because
# any move results in "win" state, meaning children[0] is a win so column 0 is the move. Yay!
# print("Win score: ")
# print(agent.calculateScore(win))
# print("Column: ")
# print(agent.go(brd))


"""for b in boards:
    tier2 = agent.get_successors(b[0])
    for c in tier2:
        print(c[0].board)
        print(agent.calculateScore(c[0]))"""

# Prints a list of all the children to depth n

# It's only looking at the 1st successor of current board state, where a "1" piece is placed in col 0, so it won't ever
# detect a win in column 0. Remember this later, silly.
for b in agent.getRecursiveSuccessors(b1, 2):
    # if agent.calculateScore(b[0]) > 1:
        for n in range(0, 4):
            print(b[0].board[n])
        print("==== ====")
# yay, they're the same.

print(agent.go(b1))

print(agent.get_best_col(b1, 4))

print(agent.alphaBeta(win, 10, float('-inf'), float('inf'), 1))


