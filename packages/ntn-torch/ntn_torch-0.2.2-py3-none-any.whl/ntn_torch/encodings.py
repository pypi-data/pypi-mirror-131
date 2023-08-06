import numpy as np
import torch


class Thermometer(object):
    def __init__(self, minimum, maximum, resolution):
        self.minimum = minimum
        self.maximum = maximum
        self.resolution = resolution

    def __repr__(self):
        return f"Thermometer(minimum={self.minimum}, maximum={self.maximum}, resolution={self.resolution})"

    def encode(self, X):
        X = torch.as_tensor(X, device='cpu')

        enc = torch.arange(self.resolution).expand(*X.shape, self.resolution)
        threshold = (X.reshape((*X.shape, 1)) - self.minimum)/(self.maximum - self.minimum)*self.resolution

        return enc < threshold

    # def decode(self, pattern):
    #     pattern = np.asarray(pattern)

    #     # TODO: Check if pattern is at least a vector
    #     # TODO: Check if pattern length or number of rows is equal to resolution
    #     # TODO: Check if pattern is a binary array
    #     if pattern.ndim == 1:
    #         # TODO: Test np.count_nonzero
    #         popcount = np.sum(pattern)

    #         return self.minimum + popcount*(self.maximum - self.minimum)/self.resolution

    #     return np.asarray([self.decode(pattern[..., i]) for i in range(pattern.shape[-1])])


# class CircularThermometerEncoder(object):
#     def __init__(self, minimum, maximum, resolution, wrap=True):
#         self.minimum = minimum
#         self.maximum = maximum
#         self.resolution = resolution
#         self.block_len = np.floor(self.resolution/2)
#         self.wrap = wrap
#         self.max_shift = resolution if wrap else resolution - self.block_len

#     def __repr__(self):
#         return f"CircularThermometerEncoder(minimum={self.minimum}, maximum={self.maximum}, resolution={self.resolution}), wrap={self.wrap}"

#     def encode(self, X):
#         X = np.asarray(X)

#         if X.ndim == 0:
#             if X < self.minimum or X > self.maximum:
#                 raise ValueError(
#                     f"Encoded values should be in the range [{self.minimum}, {self.maximum}]. Value given: {X}")

#             base_pattern = np.fromfunction(
#                 lambda i: i < self.block_len, (self.resolution,)).astype(np.uint8)
#             shift = int(np.abs(self.minimum-X) /
#                         (self.maximum-self.minimum)*self.max_shift)

#             return np.roll(base_pattern, shift)

#         return np.stack([self.encode(v) for v in X], axis=X.ndim)

    # def decode(self, pattern):
    #     pattern = np.asarray(pattern)

    #     # TODO: Check if pattern is at least a vector
    #     # TODO: Check if pattern length or number of rows is equal to resolution
    #     # TODO: Check if pattern is a binary array
    #     if pattern.ndim == 1:
    #         first_0 = index(pattern, 0)[0]
    #         first_1 = index(pattern, 1)[0]

    #         if first_0 > first_1:
    #             shift = (first_0 - self.block_len) % self.resolution
    #         else:
    #             shift = first_1

    #         if shift > self.max_shift:
    #             raise ValueError(
    #                 "Input pattern wraps around. Consider using a encoder with wrap enabled")

    #         return self.minimum + shift*(self.maximum - self.minimum)/self.max_shift

    #     return np.asarray([self.decode(pattern[..., i]) for i in range(pattern.shape[-1])])
