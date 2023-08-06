import torch
import gym
from gym import spaces

import numpy as np

from stable_baselines3.common.on_policy_algorithm import OnPolicyAlgorithm
from stable_baselines3.common.env_util import unwrap_wrapper
from stable_baselines3.common.utils import obs_as_tensor

from ntn_torch.rl.common.policies import NTNPolicy
from ntn_torch.rl.common.buffers import EpisodicBuffer

class NTNReinforce(OnPolicyAlgorithm):
  def __init__(
    self,
    env,
    learning_rate=3e-4,
    n_epochs=1,
    gamma=0.99,
    max_grad_norm=0.5,
    tensorboard_log=None,
    create_eval_env=False,
    policy_kwargs=None,
    verbose=0,
    seed=None,
    device='cpu',
    _init_setup_model=True
  ):
    super(NTNReinforce, self).__init__(
      NTNPolicy,
      env,
      learning_rate,
      unwrap_wrapper(env.envs[0], gym.wrappers.TimeLimit)._max_episode_steps,
      gamma,
      1.0,
      1.0, # ent_coef
      1.0, # vf_coef
      max_grad_norm,
      False, # use_sde
      0, # sde_sample_freq
      policy_base=NTNPolicy,
      tensorboard_log=tensorboard_log,
      create_eval_env=create_eval_env,
      policy_kwargs=policy_kwargs,
      verbose=verbose,
      seed=seed,
      device=device,
      _init_setup_model=_init_setup_model,
      supported_action_spaces=(
        spaces.Box,
        spaces.Discrete
      )
    )

    self.episodic_buffer = None

    if _init_setup_model:
      self._setup_model()

  def _setup_model(self):
    self._setup_lr_schedule()
    self.set_random_seed(self.seed)

    self.episodic_buffer = EpisodicBuffer(self.env, gamma=self.gamma)
    self.rollout_buffer = self.episodic_buffer
    self.policy = NTNPolicy(self.env.observation_space, self.env.action_space, self.lr_schedule, **self.policy_kwargs)
    
  def collect_episode(self):
    assert self._last_obs is not None, "No previous observation was provided"
    self.policy.set_training_mode(False)
    self.episodic_buffer.reset()

    n_envs = self.env.num_envs
    dones = np.zeros(n_envs, dtype=np.bool)
    while not dones.all():
      with torch.no_grad():
        obs_tensor = obs_as_tensor(self._last_obs, self.device)
        actions, log_prob = self.policy(obs_tensor)

      # Rescale and perform action
      clipped_actions = actions.numpy()
      # Clip the actions to avoid out of bound error
      if isinstance(self.action_space, gym.spaces.Box):
          clipped_actions = np.clip(actions, self.action_space.low, self.action_space.high)

      obs, rew, done, infos = self.env.step(np.atleast_1d(clipped_actions))
      dones += done
      
      self.episodic_buffer.add(self._last_obs, clipped_actions.reshape((n_envs,1)), rew, dones, log_prob)

      self.num_timesteps += self.env.num_envs - dones.sum()
      self._last_obs = obs
      self._last_episode_starts = done
      self._update_info_buffer(infos)

    self.num_timesteps += self.env.num_envs # Accounting for the last step in each env
    self.episodic_buffer.compute_returns()

    return True

  def collect_rollouts(self, env, callback, rollout_buffer, n_rollout_steps):
    """Just passes through to collect_episode"""
    return self.collect_episode()

  def _loss(self, timestep, observation, action, ret):
    return -self.gamma**timestep*ret*self.policy.get_distribution(
        torch.atleast_2d(obs_as_tensor(observation, self.device))).log_prob(
            obs_as_tensor(action, self.device))

  def train(self):
     # Switch to train mode
    self.policy.set_training_mode(True)
    # Update optimizer learning rate
    self._update_learning_rate(self.policy.optimizer)

    for timestep, observation, action, reward, ret, log_prob in self.episodic_buffer.all():
      loss = self._loss(timestep, observation, action, ret)

      # Optimization step
      self.policy.optimizer.zero_grad()
      loss.backward()
      self.policy.optimizer.step()