from cadeia_base import *
from readFiles import *
from important_functions import *
from initial_tree import *
import networkx as nx
import numpy as np 
import random
import operator
import matplotlib.pyplot as plt


def SA(G, eps, alpha, SAmax, T_initial, s, B, C):
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
    solucao_otima = f(s)
    iterT = 0 
    T = T_initial
    best_solution = nx.Graph.copy(s)
    best_cost = check_cost(s, C)
    while T > eps:
        while iterT < SAmax:
            iterT = iterT + 1
            sol_atual = f(s)
            s_t = transition_neighbor(G, s)
            sol_vizinho =  f(s_t)
            cost_vizinho = check_cost(s_t, C)
            delta = sol_vizinho - sol_atual
            if delta < 0 or cost_vizinho <= B:
                s = s_t 
                if sol_vizinho < solucao_otima and cost_vizinho <= best_cost:
                    best_solution = nx.Graph.copy(s_t)
                    solucao_otima = sol_vizinho 
                    best_cost = cost_vizinho
            else:
                x = np.random.uniform(0, 1)
                boltzmann = np.exp(((-1)*delta)/T)
                if x < boltzmann:
                    s = s_t
        T = T*alpha
        iterT = 0  
    print("Solução ótima", solucao_otima)
    return best_solution, solucao_otima  

# Leitura do grafo
path = 'D:\\mndzvd\\Documentos\\GitHub\\project_mcmc\\instances\\c_v10_a45_d4.txt'
n, C = readFiles(path)
G = create_graph(n, C)
B = generate_B(G, C, 0.30)


# Solução inicial
b_tree = generate_random_tree(G)
b_tree = mst(G, C)
# b_tree = nx.dfs_tree(G, 0)
# b_tree = b_tree.to_undirected()

nx.draw(b_tree, with_labels=True)
plt.show()


# Simulated Annealing
graph, sol = SA(G, 0.00001, 0.98, 100, 100, b_tree, B, C)
print("Custo total: ", check_cost(graph, C), "Budget: ", B, "Diametro:", f(graph))
# pos = nx.spring_layout(b_tree)
# nx.draw(b_tree, pos, font_weight='bold')
# nx.draw_networkx_labels(b_tree, pos, labels=x)
# plt.show()
