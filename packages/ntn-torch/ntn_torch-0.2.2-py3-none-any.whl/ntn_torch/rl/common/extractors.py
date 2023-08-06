from ntn_torch.encodings import Thermometer

from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.preprocessing import get_flattened_obs_dim


class ThermometerExtractor(BaseFeaturesExtractor):
  # I'll for now expect the minimum and maximum of the thermometer to be passed as arguments, but if a use a 
  # env wrapper that normalizes observations, I could have a fixed, or at least default thermo interval
  def __init__(self, observation_space, low, high, res):
    super(ThermometerExtractor, self).__init__(observation_space, res*get_flattened_obs_dim(observation_space))

    self.thermometer = Thermometer(low, high, res)

  def forward(self, observations):
    return self.thermometer.encode(observations).reshape((observations.shape[0], -1))