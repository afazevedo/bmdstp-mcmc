from readFiles import *
import networkx as nx
import numpy as np 
import random
import operator
import matplotlib.pyplot as plt

path = 'D:\mndzvd\Documentos\GitHub\project_mcmc\instances\c_v6_a15_d4.txt'


n, C = readFiles(path)
G = create_graph(n, C)

# print(G.number_of_nodes())
# print(G.number_of_edges())

T = nx.bfs_tree(G, 0, reverse=False, depth_limit=None, sort_neighbors=None)
T = T.to_undirected()


def transition_neighbor(graph):
#     '''
#     Cria um novo grafo a partir da adição de uma aresta de G-T e a remoção de uma aresta do ciclo. 
#     :param graph: networkx graph
#     :return: networkx graph
#     '''

    edges = list(graph.edges) # Conjunto das arestas da árvore
    nonedges = list(nx.non_edges(graph))  # Conjunto das arestas de G que não estão em T

    # Escolher uma aresta do conjunto nonedges e adicionar ao grafo fomando um ciclo
    chosen_nonedge = random.choice([x for x in nonedges])
    graph.add_edge(chosen_nonedge[0], chosen_nonedge[1])
    
    # print("Adicionei a aresta (", chosen_nonedge[0], ",", chosen_nonedge[1], ")  ao grafo\n")
    # print("Ciclo encontrado: ", nx.find_cycle(graph), "\n")

    # Escolher uma aresta do ciclo e retirar ela do grafo
    chosen_edge = random.choice([x for x in nx.find_cycle(graph)])
    # print("Removi a aresta (", chosen_edge[0], " , ", chosen_edge[1], ")  do grafo")
    graph.remove_edge(chosen_edge[0], chosen_edge[1])
    
    # nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()
    
    # nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()
    
    return graph

def f(graph):
    e = nx.eccentricity(graph)
    return e[max(e, key=e.get)]

# s_t = transition_neighbor(T)
# nx.draw(s_t, with_labels=True, font_weight='bold')
# plt.show()
# diameter = f(s_t)
# print(diameter)