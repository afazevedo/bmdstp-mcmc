import networkx as nx
import numpy as np 
import random

class PointGenerator:
    def __init__(self, iteration):
        self.iter = iteration

    def generate(self):
        xs = np.arange(1, int(self.iter))
        ys = np.arange(1, int(self.iter))

        return np.column_stack((xs, ys))


