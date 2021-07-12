# OpenAI Gym was designed (obviously) for single-agent RL, and so implementing multi-agent RL requires a bit of finesse. The way we do this is we define a WeightedRPSOuter which runs an agent *inside the env.step* function which represents the learning of the other agent.

from IPython import embed
import gym
import random
import uuid
from gym import spaces

class WeightedRPSStandard(gym.Env):
  # If you win with scissors you get +2 and paper gets -2
  rewards = [[0, -1, 1], #R
             [1, 0, -2], #P
             [-1, 2, 0]] #S

  def __init__(self):
    super(WeightedRPSStandard, self).__init__()
    self.action_space = spaces.Discrete(3)
    self.observation_space = spaces.Discrete(1)
    self.id = uuid.uuid1()

  def step(self, action):
      if random.random() < 0.5:
          reward = self.rewards[action][0]
      else:
          reward = self.rewards[action][1]

      return 0, reward, True, {}
    
  def reset(self):
      return 0


class WeightedRPSInner(WeightedRPSStandard):
  
  def __init__(self):
    super(WeightedRPSInner, self).__init__()
    self.other_action = None
    self.last_played_action = None

  def set_other_action(self, action):
      self.other_action = action

  def step(self, action):
      #print("Inner step with other action {}".format(self.other_action))
      assert self.other_action is not None, "Opponent not set correctly"

      reward = self.rewards[action][self.other_action]
      self.last_played_action = action
      return 0, reward, True, {}

  def reset(self):
      return 0

class WeightedRPSOuter(WeightedRPSStandard):

  def __init__(self, agent, full_step):
    super(WeightedRPSOuter, self).__init__()
    self.agent = agent
    self.inner_env = self.agent.env.envs[0]
    self.full_step = full_step
    self.update_number = 1

    assert agent and full_step, "Inner agent not specified"

  def step(self, action):
    #print("Outer step with action {}".format(action))
    #print(self.inner_env.id)
    self.inner_env.set_other_action(action)
    self.full_step(self.update_number)
    #self.inner_env.set_other_action(None)
    self.update_number += 1

    inner_agent_action = self.inner_env.last_played_action
    reward = self.rewards[action][inner_agent_action]


    return 0, reward, True, {}

  def reset(self):
      return 0
