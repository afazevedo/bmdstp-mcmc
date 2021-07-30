from nodes_generator import NodeGenerator
from simulated_annealing import SimulatedAnnealing
from simulated_temperature import SimulatedAnnealing_initial
from read_files import *
import time

def main(path, B, i):
    print("Log instance: ", path[51:], " with budget: ", B)
    
    '''set instances parameters'''
    n, m, matrix_cost = readFiles(path, True)
    G = create_graph(n, matrix_cost)
    
    '''set the first simulated annealing algorithm params'''
    temp = 100000
    stopping_temp = 0.0001
    alpha = 0.7
    stopping_iter = m-n
    stopping_iter = 100
    
    first = SimulatedAnnealing_initial(G, temp, alpha, stopping_temp, stopping_iter, matrix_cost, B)
    temp_initial = first.anneal()
    print('Temperatura inicial: ', temp_initial)
    
    '''set the simulated annealing algorithm params'''
    
    stopping_temp = 0.0001
    alpha = 0.7
    start_time = time.time()
    
    '''run simulated annealing'''
    sa = SimulatedAnnealing(G, temp_initial, alpha, stopping_temp, stopping_iter, matrix_cost, B, start_time)
    sa.anneal()
    
    '''show the improvement'''
    sa.print_solution(start_time)

    # '''ploting solution'''
    # sa.plotLearning_diameter()
    # sa.plotLearning_weight()
    # sa.plotLearning_best_solution_diameter()
    
    
if __name__ == "__main__":
    B = [904.95]
    files = ['D:\\mndzvd\\Documentos\\GitHub\\project_mcmc\\instances\\s_v40_a100_d4.txt']
    cont = 0
    for i in files:
        main(i, B[cont], cont)
        cont += 1



