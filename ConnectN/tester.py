import board
import alpha_beta_agent as aba

brd = [
    [2, 2, 1, 2, 1],
    [2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

b1 = board.Board(brd, 5, 4, 4)



agent = aba.AlphaBetaAgent("Jeffery", 5)

print(agent.calculateScore(b1))

boards = agent.get_successors(b1)

"""for b in boards:
    tier2 = agent.get_successors(b[0])
    for c in tier2:
        print(c[0].board)
        print(agent.calculateScore(c[0]))"""

# Prints a list of all the children to depth n

# It's only looking at the 1st successor of current board state, where a "1" piece is placed in col 0, so it won't ever
# detect a win in column 0. Remember this later, silly.
for b in agent.getRecursiveSuccessors(agent.get_successors(b1)[0][0], 1):
    # if agent.calculateScore(b[0]) > 1:
        print(b[0].board)

print("REGULAR GETSUCCESSORS: \n\n\n")

for b in agent.get_successors(b1):
    print(b[0].board)
# yay, they're the same.

