import board
import agent
import run
import game
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
    [2, 2, 2, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

wbrd2 = [
    [1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

whynowin = [
    [2, 1, 2, 1, 0, 1, 1],
    [1, 2, 1, 1, 0, 0, 1],
    [2, 2, 2, 0, 0, 0, 1],
    [2, 1, 2, 0, 0, 0, 0],
    [2, 2, 1, 0, 0, 0, 0],
    [1, 2, 0, 0, 0, 0, 0]
]

b1 = board.Board(brd, 5, 4, 4)

win = board.Board(wbrd, 5, 4, 4)

win2 = board.Board(wbrd2, 5, 4, 4)

why = board.Board(whynowin, 7, 6, 4)

blank = board.Board(empty, 5, 4, 4)

win.player = 2
win2.player = 2  # Interestingly, WIN2 only detects properly when current player is 1? Wacky.

def printBoard(brd):
    for r in brd.board:
        print(r)
    print(" =====///=====")

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

alpha = aba.AlphaBetaAgent("Jimbo", 3)

print("Scores for children::")
for c in alpha.get_successors(why):
    print("Move: " + str(c[1]))
    print("Score: " + str(alpha.calculateScore(c[0])))
print(alpha.calculateScore(why))

print("Suggested move::")
print(alpha.go(why))


print(alpha.calculateScore(win))
printBoard(win)
win.add_token(alpha.go(win))
printBoard(win)

print("WIN2:")
print(alpha.calculateScore(win2))
printBoard(win2)
win2.add_token(alpha.go(win2))
printBoard(win2)

# Not properly states of poor outcome for some reason.
"""win.add_token(alpha.go(win))

print(win.board)

win.add_token(0)
print(alpha.calculateScore(win))

win.add_token(0)
print(alpha.calculateScore(win))

print("Player number: " + str(win.player))
print("Column picked: ")
print(alpha.go(win))
print(alpha.go(win))
print(alpha.go(win))
win.add_token(alpha.go(win))

print("Player number: " + str(win.player))
print("Column picked: ")
print(alpha.go(win))"""

#boards = alpha.get_successors(brd)

#print(alpha.decision(win)[0].board)

#g = game.Game(5, # width
 #             4, # height
  #            4, # tokens in a row to win
   #           agent.RandomAgent("random"),        # player 1
    #          aba.AlphaBetaAgent("alphabeta", 4)) # player 2

