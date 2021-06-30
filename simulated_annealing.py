from cadeia_base import *
from readFiles import *
import networkx as nx
import numpy as np 
import random
import operator
import matplotlib.pyplot as plt


def SA(eps, alpha, SAmax, T_initial, s):
    best_solution = s 
    iterT = 0 
    T = T_initial
    while T > eps:
        while iterT < SAmax:
            iterT = iterT + 1
            s_t = transition_neighbor(s)
            delta = f(s_t) - f(s)     
            if delta < 0:
                s = s_t 
                if f(s_t) < best_solution:
                    best_solution = s_t 
            else:
                x = np.random.uniform(0,1)
                boltzmann = np.exp(((-1)*delta)/T)
                if x < boltzmann:
                    s = s_t 
        T = T*alpha
        iterT = 0  
    return best_solution       

# Leitura do grafo
path = 'D:\mndzvd\Documentos\GitHub\project_mcmc\instances\c_v6_a15_d4.txt'
n, C = readFiles(path)
G = create_graph(n, C)

# Solução inicial
b_tree = nx.bfs_tree(G, 0, reverse=False, depth_limit=None, sort_neighbors=None)
b_tree = b_tree.to_undirected()

# Precisão da temperatura final, taxa de resfriamento, 
# número maximo de iterações por temperatura, temperatura inicial, solução inicial

graph = SA(0.0001, 0.6, 10, 100000, b_tree)
nx.draw(graph, with_labels=True, font_weight='bold')
plt.show()
print(f(graph))