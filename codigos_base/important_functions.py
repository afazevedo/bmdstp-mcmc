import networkx as nx
import numpy as np 
import random
import operator
import matplotlib.pyplot as plt

def check_cost(G, C):
    """[Calcula o custo total de um grafo]

    Args:
        G ([type]): [Grafo G]
        C ([type]): [Custo do grafo G]

    Returns:
        total_cost [Float]: [Custo total da árvore]
    """
    total_cost = 0
    for i,j in G.edges():
        total_cost += C[i,j]

    return total_cost
    
def generate_B(G, C, percent):
    budget = 0
    
    sorted_C = np.sort(C, axis=None)  
    reverse_C = sorted_C[::-1]
    
    n = nx.number_of_nodes(G)
    
    for i in range(n-1):
        budget += reverse_C[i]
    
    return percent*budget    


def f(graph):
    e = nx.eccentricity(graph)
    return e[max(e, key=e.get)]

def g(graph, C):
    return check_cost(graph, C)

def mst(graph, C):
    b_tree = nx.Graph()
    mst = nx.minimum_spanning_edges(graph, algorithm="prim", data=False)
    edges_lists = list(mst)
    for i in edges_lists:
        nx.Graph.add_edge(b_tree, i[0], i[1])
        
    return b_tree
        
        
