import numpy as np 
from kaggle_environments import make, evaluate

env = make('rps', configuration = {"episodeSteps":1000}, debug = 'True')
env.reset()
env.run(["agent.py", "statistical"])
env.render(mode = 'ipython')
print(evaluate('rps',["agent.py", "statistical"],configuration = {"episodeSteps":1000}, num_episodes = 10))
