import torch

def bitarray_to_word(bitarray):
  return torch.sum(bitarray*torch.special.exp2(torch.arange(len(bitarray)))).type(torch.int).item()