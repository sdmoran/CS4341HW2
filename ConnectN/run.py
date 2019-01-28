import random
import game
import agent
import alpha_beta_agent as aba

# Set random seed for reproducibility
for i in range (0, 1000):
    seed = random.randint(1, 100000001)
    print("Random seed: " + str(seed))
    random.seed(seed)

#
# Random vs. Random
#
#g = game.Game(7, # width
#              6, # height
#              4, # tokens in a row to win
#              agent.RandomAgent("random1"),       # player 1
#              agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
# Random vs. AlphaBeta
#
g = game.Game(7, # width
              6, # height
              4, # tokens in a row to win
              agent.RandomAgent("random2"),
              aba.AlphaBetaAgent("alphabeta", 4)
              )
# player 2

#
# Human vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

# Execute the game
outcome = g.go()
