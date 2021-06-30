import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt

# path = 'D:\mndzvd\Documentos\GitHub\project_mcmc\instances\c_v6_a15_d4.txt'

def readFiles(path):
    cont = 0
    with open(path, 'r') as arq:
        for line in arq:
            line = line.strip()
            line = line.split()
            if cont == 0:
                n = int(line[0])
                C = np.zeros((n, n))
            else:
                i = int(line[0])
                j = int(line[1])
                C[i,j] = int(line[2])
                C[j,i] = C[i,j]
            cont = cont + 1 
    return n, C


# def readFiles(path):
# C = np.loadtxt(path)
# n = len(C)
    # return n, C


def create_graph(n,C):
    G = nx.Graph()

    for i in range(n): 
        G.add_node(i)
        for j in range(n):
            G.add_node(j)
            if C[i][j] > 0.00001:
                G.add_edge(i, j)
    return G

