from cadeia_base import *
from readFiles import *
import networkx as nx
import numpy as np 
import random
import operator
import matplotlib.pyplot as plt


def SA(eps, alpha, SAmax, T_initial, s):
    solucao_otima = f(s)
    iterT = 0 
    T = T_initial
    aux = s
    best_solution = aux
    while T > eps:
        while iterT < SAmax:
            iterT = iterT + 1
            s_t = transition_neighbor(s)
            sol_atual = f(s)
            sol_vizinho = f(s_t) 
            delta = sol_vizinho - sol_atual
           
            if delta <= 0:
                s = s_t 
                if sol_vizinho < solucao_otima:
                    aux = s_t
                    best_solution = aux
                    solucao_otima = sol_vizinho 

            else:
                x = np.random.uniform(0,1)
                boltzmann = np.exp(((-1)*delta)/T)
                if x < boltzmann:
                    s = s_t
        T = T*alpha
        iterT = 0  
    return best_solution, solucao_otima  

# Leitura do grafo
path = 'C:\\Users\\Wanderson\\OneDrive\\Documentos\\GitHub\\project_mcmc\\instances\\states_brazil.txt'
n, C = readFiles(path)
G = create_graph(n, C)

# Solução inicial
b_tree = nx.bfs_tree(G, 0, reverse=False, depth_limit=None, sort_neighbors=None)
b_tree = b_tree.to_undirected()

# Precisão da temperatura final, taxa de resfriamento, 
# número maximo de iterações por temperatura, temperatura inicial, solução inicial

graph, sol = SA(0.001, 0.6, 10, 100, b_tree)
nx.draw(graph, with_labels=True, font_weight='bold')
plt.show()
print(f(graph), sol)



# s = b_tree

# iterT = 0 
# T_initial = 1000
# T = T_initial
# for i in range(10):
#     s_t = 0
#     aux = f(s)
#     #print('f(st) antes de transitar ', f(s_t))
#     print('O valor de f(s) é: ', aux)
#     s_t = transition_neighbor(s)
#     print('f(st) após transitar ', f(s_t), 'f(s): ', aux)
#     delta = f(s_t) - aux
#     print(delta)
#     # if delta != 0:
#     #     print('é diferente')
#     #print("f(st): ",f(s_t), "f(s): ", f(s))     
#     if delta <= 0:
#         s = s_t 
#         #print('f(s_t): ', f(s_t), 'best_solution: ', f(best_solution))
#         if f(s_t) < solucao_otima:
#             best_solution = s_t
#             solucao_otima = f(s_t) 
#     else:
#         #print('delta: ',delta, "T: ", T)
#         x = np.random.uniform(0,1)
#         print('x: ', x)
#         boltzmann = np.exp(((-1)*delta)/T)
#         print('boltzmann: ', boltzmann,"\n")
#         if x < boltzmann:
#             s = s_t
#             print('aceitou')
# print('solução ótima: ', solucao_otima)