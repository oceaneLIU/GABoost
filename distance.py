import numpy as np


def dynamic_commonality(ctx1: set, ctx2: set):
    a = len(ctx1 & ctx2)
    return -a


def static_commonality(ctx1: np.array, ctx2: np.array):
    a = np.sum(np.minimum(ctx1, ctx2))
    return -a
