import torch

from ntn_torch.net import FunctionalDiscriminator
from ntn_torch.rl.common.extractors import ThermometerExtractor

from stable_baselines3.common.policies import BasePolicy
from stable_baselines3.common.preprocessing import get_action_dim
from stable_baselines3.common.distributions import (
    CategoricalDistribution,
    DiagGaussianDistribution,
    make_proba_distribution,
)

class NTNPolicy(BasePolicy):
  def __init__(
    self,
    observation_space,
    action_space,
    lr_schedule,
    tuple_size,
    squash_output = False,
    features_extractor_class = ThermometerExtractor,
    features_extractor_kwargs = {'low': -1., 'high': 1., 'res': 16},
    optimizer_class = torch.optim.SGD,
    optimizer_kwargs = None
  ):
    super(NTNPolicy, self).__init__(
      observation_space,
      action_space,
      features_extractor_class,
      features_extractor_kwargs,
      optimizer_class=optimizer_class,
      optimizer_kwargs=optimizer_kwargs,
      squash_output=squash_output,
    )

    self.tuple_size = tuple_size
    # print("Here?")
    self.features_extractor = features_extractor_class(
        self.observation_space, **self.features_extractor_kwargs)
    # print("There??")
    self.features_dim = self.features_extractor.features_dim
    # print(self.features_dim)

    self.action_dist = make_proba_distribution(
        action_space, use_sde=False, dist_kwargs=None)

    self._build(lr_schedule)

  def _get_constructor_parameters(self):
    raise NotImplementedError()

  def _build(self, lr_schedule):
    if isinstance(self.action_dist, DiagGaussianDistribution):
      output_dim = 2*get_action_dim(self.action_space)
    elif isinstance(self.action_dist, CategoricalDistribution):
      output_dim = self.action_space.n
    else:
      raise NotImplementedError(f"Unsupported distribution '{self.action_dist}'.")

    self.policy_net = FunctionalDiscriminator(
        self.features_dim, output_dim, self.tuple_size)
    self.optimizer = self.optimizer_class(
        self.policy_net.parameters(), lr=lr_schedule(1), **self.optimizer_kwargs)
    
    # TODO: Consider having the std not be action-dependent in the gaussian case,
    # as in the library. Something like:
    # self.log_std = nn.Parameter(th.ones(self.action_dim) * log_std_init, requires_grad=True)
  def _get_action_dist_from_net_out(self, net_output):
    net_output = torch.atleast_2d(net_output)
    if isinstance(self.action_dist, DiagGaussianDistribution):
      # First half of the output is the mean vector and the second half, the
      # diagonal of the covariance matrix
      return self.action_dist.proba_distribution(*torch.tensor_split(net_output, 2))
    elif isinstance(self.action_dist, CategoricalDistribution):
      return self.action_dist.proba_distribution(action_logits=net_output)
    else:
      raise ValueError("Invalid action distribution")

  def get_distribution(self, obs):
    # obs = self.obs_to_tensor(obs)
    features = self.extract_features(obs)
    net_out  = self.policy_net(features)
    return self._get_action_dist_from_net_out(net_out)

  def forward(self, obs,  deterministic=False):
    distribution = self.get_distribution(obs)
    actions = distribution.get_actions(deterministic=deterministic)
    log_prob = distribution.log_prob(actions)
    return actions, log_prob

  def _predict(self, observation, deterministic = False):
    # observation = torch.atleast_2d(observation)
    return self.get_distribution(observation).get_actions(deterministic=deterministic)
