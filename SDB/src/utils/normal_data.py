import numpy as np
from numpy.random import Generator, PCG64


gen = Generator(PCG64(12345))

def normal_data():
    x = np.zeros(60, dtype=int)
    ns = gen.normal(30, 10, 1000)
    ns = ns[ns >= 0]
    ns = ns[ns < 60]
    ns = ns.astype(int)
    unique, counts = np.unique(ns, return_counts=True)
    x[unique] += counts
    return x.tolist()

def random(n):
    """
    Return a random number between [0, n)
    """
    return int(gen.random() * n)
    
