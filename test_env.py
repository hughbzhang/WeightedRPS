import gym
import numpy as np
import WeightedRPS
from IPython import embed
import random

env = gym.make('weightedrps-v1')
lookup = ["Rock", "Paper", "Scissors"]

for a in range(3):

    action_reward = 0.
    for _ in range(10000):
        _, reward, _, _ = env.step(a)
        action_reward += reward

    action_reward /= 10000
    print("Reward for action {} is {}".format(lookup[a], action_reward))

