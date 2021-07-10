import networkx as nx
import numpy as np 
import random
import operator
import matplotlib.pyplot as plt


def random_walk(G):
    '''
        Criação do passeio aleatório
        :params: G - grafo original
    '''
    n = nx.number_of_nodes(G)
    
    # Vértice inicial escolhido ao acaso
    first_node = random.randint(0, n-1)
    
    # Controle dos vértices visitados
    is_visited = np.zeros(n, dtype=bool)
    
    # Criação do mapeamento da primeira visita a cada vértice
    first_visit = np.zeros(n, dtype=int)
    
    # Nó inicial foi visitado
    is_visited[first_node] = True
    
    # Escolhe um vizinho aleatoriamente
    neighbor = np.random.choice(list(G.neighbors(first_node)))
    is_visited[neighbor] = 1

    # Amarração entre o nó inicial e seu vizinho
    first_visit[first_node] = neighbor
    first_visit[neighbor] = first_node
    
    cont = 2
    while True:
        # Guardar o último nó visitado
        last_node = neighbor
        
        # Escolher aleatoriamente um vizinho
        neighbor_edge = np.random.choice(list(G.neighbors(neighbor)))
        
        if not is_visited[neighbor_edge]:
            first_visit[neighbor_edge] = last_node
            is_visited[neighbor_edge] = 1
            cont = cont + 1
        
        # Se visitou todos os nós, para
        if cont == n:
            break  
        
        neighbor = neighbor_edge
        
    return first_visit, first_node

def generate_random_tree(G):
    # Executa o passeio aleatório
    first_visit, first_node = random_walk(G)
    
    # Inicializar a árvore aleatória
    random_tree = nx.Graph()
    
    # Preencher com (j,i) para todo i != first_node
    for i in range(len(first_visit)):
        if i != first_node:
            random_tree.add_edge(first_visit[i], i)

    return random_tree

  



def mst(graph, C):
    b_tree = nx.Graph()
    mst = nx.minimum_spanning_edges(graph, algorithm="prim", data=False)
    edges_lists = list(mst)
    for i in edges_lists:
        nx.Graph.add_edge(b_tree, i[0], i[1])
        
    return b_tree