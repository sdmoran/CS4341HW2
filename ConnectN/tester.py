import board
import alpha_beta_agent as aba

brd = [
    [2, 2, 2, 0, 2],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

b1 = board.Board(brd, 5, 4, 4)


agent = aba.AlphaBetaAgent("Jeffery", 5)


boards = agent.get_successors(b1)

for b in boards:
    tier2 = agent.get_successors(b[0])
    for c in tier2:
        print(c[0].board)
        print(agent.calculateScore(c[0]))


print(agent.calculateScore(b1))
