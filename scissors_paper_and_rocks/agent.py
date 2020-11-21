# def copy_opponent_agent(observation, configuration):
#     if observation.step > 0:
#         return observation.lastOpponentAction
#     else:
#         return 0

import random

def copy_opponent_agent(observation, configuration):
    if observation.step > 0:
        return observation.lastOpponentAction
    else:
        return 0

def random_agent(observation, configuration):
    return int(random.randint(0,2))
