import numpy as np
import gym

from scipy.signal import lfilter
from gym import spaces

from stable_baselines3.common.buffers import BaseBuffer
from stable_baselines3.common.vec_env import VecEnv
from stable_baselines3.common.env_util import unwrap_wrapper

class EpisodicBuffer(BaseBuffer):
  def __init__(
      self,
      env,
      gamma=0.99
  ):
    if not isinstance(env, VecEnv):
      raise ValueError("environment must be instance of VecEnv")
    
    max_steps = unwrap_wrapper(env.envs[0], gym.wrappers.TimeLimit)._max_episode_steps

    if max_steps is None:
      raise ValueError("environment must have a time limit")

    super(EpisodicBuffer, self).__init__(
        max_steps,
        env.observation_space,
        env.action_space,
        "cpu",
        env.num_envs
    )
    self.gamma = gamma
    self.max_steps = max_steps

    self.observations, self.actions, self.rewards  = None, None, None
    self.returns, self.log_probs, self.episode_end, self.env_has_ended = None, None, None, None

    self.reset()

  def reset(self):
    self.episode_end = np.full(self.n_envs, np.iinfo(np.int).max) # Points to where the episode actually ended for each env
    self.env_has_ended = np.zeros(self.n_envs, dtype=np.bool)
    self.observations = np.zeros((self.buffer_size, self.n_envs) + self.obs_shape, dtype=np.float32)
    self.actions = np.zeros((self.buffer_size, self.n_envs, self.action_dim), dtype=np.float32)
    self.rewards = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
    self.returns = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
    self.log_probs = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)

    super(EpisodicBuffer, self).reset()

  def add(self, obs, action, reward, dones, log_prob):
    if len(log_prob.shape) == 0:
      # Reshape 0-d tensor to avoid error
      log_prob = log_prob.reshape(-1, 1)

    # Reshape needed when using multiple envs with discrete observations
    # as numpy cannot broadcast (n_discrete,) to (n_discrete, 1)
    if isinstance(self.observation_space, spaces.Discrete):
      obs = obs.reshape((self.n_envs,) + self.obs_shape)

    self.env_has_ended += dones
    self.observations[self.pos] = np.array(obs).copy()
    self.actions[self.pos] = np.array(action).copy()
    self.rewards[self.pos] = np.array(reward).copy()
    self.log_probs[self.pos] = log_prob.clone().cpu().numpy()
    self.pos += 1
    if self.pos == self.buffer_size or self.env_has_ended.all():
        self.full = True

    self.episode_end = np.where(self.env_has_ended, np.minimum(self.episode_end, self.pos), self.episode_end)

  def compute_returns(self):
    effective_rewards = np.where(
      np.indices(self.rewards.shape)[0] >= self.episode_end.reshape(1, -1),
      0.,
      self.rewards
    )

    self.returns = lfilter([1], [1, -self.gamma], x=effective_rewards[::-1, :], axis=0)[::-1, :]

  def _get_samples(self):
    raise NotImplementedError()

  def all(self):
    """Iterate over the episodes, one env at a time and in order"""
    "timestep, observation, action, reward, return, log_prob"
    for episode in range(self.n_envs):
      tail = self.episode_end[episode] if self.env_has_ended[episode] else self.pos
      for timestep in range(tail):
        yield (
          timestep,
          self.observations[timestep, episode],
          self.actions[timestep, episode],
          self.rewards[timestep, episode],
          self.returns[timestep, episode],
          self.log_probs[timestep, episode]
        )