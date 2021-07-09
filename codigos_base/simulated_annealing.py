from cadeia_base import *
from readFiles import *
from important_functions import *
from initial_tree import *
import networkx as nx
import numpy as np 
import random
import operator
import matplotlib.pyplot as plt


def SA(G, eps, alpha, SAmax, T_initial, s, B, C, original_cost):
    """
    Algoritmo para calcular o metaheurística Simulated Annealing.

    Args:
        G (nx.Graph): Grafo G original não direcionado.
        eps (Float): Precisão do critério de parada para temperatura.
        alpha (Float): Taxa de resfriamento.
        SAmax (Int): Número de iterações máximas para cada temperatura.
        T_initial (Float): Temperatura inicial.
        s (nx.Graph): Solução inicial (Árvore Geradora).

    Returns:
        best_solution (nx.Graph): Melhor árvore encontrada.
        sol_otima (Int): Melhor diâmetro encontrado.
    """
    solucao_otima = g(s, C)
    iterT = 0 
    T = T_initial
    best_solution = nx.Graph.copy(s)
    # best_cost = g(s, C)
    while T > eps:
        while iterT < SAmax:
            iterT = iterT + 1
            
            sol_atual = g(s, C)
            diam_atual = f(s)
            s_t = transition_neighbor(G, s)
            sol_vizinho =  g(s_t, C)
            diam_vizinho = f(s_t)
            
            delta = sol_vizinho - sol_atual
            # print("Solução atual: ", sol_atual, "Solução do vizinho: ", sol_vizinho)
            # if diam_vizinho > diam_atual:
            #     C[nonedge[0],nonedge[1]] = 1.1*C[nonedge[0],nonedge[1]]
                
            if delta < 0 and sol_vizinho <= B:   
                s = s_t 
                # print(sol_vizinho)
                # if diam_vizinho < solucao_otima:
                #     best_solution = nx.Graph.copy(s_t)
                #     solucao_otima = diam_vizinho
                if diam_vizinho < diam_atual:
                    best_solution = nx.Graph.copy(s_t)
                    solucao_otima = sol_vizinho
            else:
                x = np.random.uniform(0, 1)
                boltzmann = np.exp(((-1)*delta)/T)
                if x < boltzmann:
                    s = s_t
        T = T*alpha
        iterT = 0  
    return best_solution, solucao_otima  

# Leitura do grafo
path = 'D:\\mndzvd\\Documentos\\GitHub\\project_mcmc\\instances\\c_v10_a45_d4.txt'
n, C = readFiles(path)
original_cost = np.copy(C)
G = create_graph(n, C)
B = generate_B(G, C, 0.30)
# B = 12733

# Solução inicial
b_tree = generate_random_tree(G)
# b_tree = mst(G, C)
# b_tree = nx.bfs_tree(G, 0)
# b_tree = b_tree.to_undirected()

# nx.draw(b_tree, with_labels=True)
# plt.show()


# Simulated Annealing
graph, sol = SA(G, 0.001, 0.5, 1000, 10, b_tree, B, C, original_cost)
print("Custo total: ", check_cost(graph, original_cost), "Budget: ", B, "Diametro:", f(graph))
nx.draw(graph, with_labels=True)
plt.show()
# pos = nx.spring_layout(b_tree)
# nx.draw(b_tree, pos, font_weight='bold')
# nx.draw_networkx_labels(b_tree, pos, labels=x)
# plt.show()
