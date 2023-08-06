import torch
import numpy as np
from .utils import bitarray_to_word

class FunctionalDiscriminator(torch.nn.Module):
  def __init__(self, input_dim, output_dim, n):
    super(FunctionalDiscriminator, self).__init__()

    self.input_dim = input_dim
    self.output_dim = output_dim
    self.n = n
    self.n_nodes = torch.ceil(torch.tensor(input_dim/n)).type(torch.int).item()
    self.mapping = torch.randperm(input_dim)
    self.nodes = [dict() for _ in range(self.n_nodes)]
    self.params = torch.nn.ParameterList([
      torch.nn.Parameter(torch.zeros((output_dim,)), requires_grad=True)
      for _ in range(self.n_nodes)])

  def _keys(self, x):
    tuples = torch.tensor_split(x[self.mapping], self.n_nodes)
    
    return map(bitarray_to_word, tuples)

  # This forward variant expects inputs to be 1D tensors
  def _forward(self, x):
    keys = self._keys(x)

    if self.training:
      response = torch.zeros((self.output_dim,))
      for (node, param, key) in zip(self.nodes, self.params, keys):
        param.data = node.setdefault(key, torch.zeros((self.output_dim,), requires_grad=True))[:]
        param.requires_grad=True
        response += param

      return response/self.n

    response = torch.zeros((self.output_dim,))
    for (node, key) in zip(self.nodes, keys):
      response += node.get(key, torch.zeros((self.output_dim,)))

    return response/self.n

  def forward(self, x):
    x = torch.atleast_2d(x)

    result = torch.zeros((x.shape[0], self.output_dim))
    for i, sample in enumerate(x):
      result[i, :] = self._forward(sample)

    return result.squeeze()