import networkx as nx
import numpy as np 
import math
import random

class NodeGenerator:
    def __init__(self, original_graph, spanning_tree):
        self.original_graph = original_graph
        self.spanning_tree = spanning_tree


    def generate(self):
    #     '''
    #     Cria um novo grafo a partir da adição de uma aresta de G-T e a remoção de uma aresta do ciclo. 
    #     :param graph: networkx graph
    #     :return: networkx graph
    #     '''
        
        edges_original_graph = list(self.original_graph.edges) # Conjunto de arestas do grafo original
        edges_spanning_tree = list(self.spanning_tree.edges) # Conjunto das arestas da árvore
        
        nonedges_spanning_tree = list(nx.non_edges(self.spanning_tree))  # Conjunto de arestas que não estão em T
        A = list(set(edges_original_graph) & set(nonedges_spanning_tree)) # Conjunto das arestas de G que não estão em T

        # Escolher uma aresta do conjunto nonedges e adicionar ao grafo fomando um ciclo
        chosen_A = random.choice([x for x in A])
        self.spanning_tree.add_edge(chosen_A[0], chosen_A[1])

        # Escolher uma aresta do ciclo e retirar ela do grafo
        chosen_B = random.choice([x for x in nx.find_cycle(self.spanning_tree)])
        self.spanning_tree.remove_edge(chosen_B[0], chosen_B[1])
        
        
        return self.spanning_tree