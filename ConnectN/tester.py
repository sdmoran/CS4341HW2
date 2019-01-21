import board
import alpba_beta_agent

brd= [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1]
]

b1 = board.Board(brd, 5, 4, 5)

print(alpha_beta_agent.go(board))
