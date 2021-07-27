import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt

def readFiles(path, fst):
    cont = 0
    with open(path, 'r') as arq:
        if fst:
            for line in arq:
                line = line.strip()
                line = line.split()
                if cont == 0:
                    n = int(line[0])
                    m = int(line[1])
                    C = np.zeros((n, n))
                else:
                    i = int(line[0])
                    j = int(line[1])
                    C[i-1,j-1] = int(line[2])
                    C[j-1,i-1] = C[i-1,j-1]
                cont = cont + 1 
        else:
            for line in arq:
                line = line.strip()
                line = line.split()
                if cont == 0:
                    n = int(line[0])
                    m = int(line[1])
                    C = np.zeros((n, n))
                else:
                    i = int(line[0])
                    j = int(line[1])
                    C[i,j] = int(line[2])
                    C[j,i] = C[i,j]
                cont = cont + 1 
    return n, m, C

def create_graph(n,C):
    G = nx.Graph()

    for i in range(n): 
        G.add_node(i)
        for j in range(n):
            G.add_node(j)
            if C[i,j] > 0.00001:
                G.add_edge(i, j, weight=C[i,j])
    return G

def generate_B(G, C, percent):
    budget = 0
    
    sorted_C = np.sort(C, axis=None)  
    reverse_C = sorted_C[::-1]
    
    n = nx.number_of_nodes(G)
    
    for i in range(n-1):
        budget += reverse_C[i]
    
    return percent*budget   

x = {
    0 : "RS", 
    1 : "SC",
    2 : "PR",
    3 : "MS",
    4 : "SP", 
    5 : "RJ", 
    6 : "ES", 
    7 : "MG", 
    8 : "GO", 
    9 : "MT",
    10 : "RO",
    11 : "AC",
    12 : "AM",
    13 : "RR", 
    14 : "PA", 
    15 : "AP", 
    16 : "TO", 
    17 : "BA", 
    18 : "MA", 
    19 : "PI", 
    20 : "CE", 
    21 : "RN", 
    22 : "PB", 
    23 : "AL", 
    24 : "SE", 
    25 : "PE"
    }
