from nodes_generator import NodeGenerator
from simulated_annealing import SimulatedAnnealing
from read_files import *
import time

def main():
    '''set the simulated annealing algorithm params'''
    temp = 100000
    stopping_temp = 0.000001
    alpha = 0.995
    # alpha = 0.98
    stopping_iter = 1000000

    path = 'D:\\mndzvd\\Documentos\\GitHub\\project_mcmc\\instances\\states_brazil.txt'
    
    '''set instances parameters'''
    n, matrix_cost = readFiles(path)
    G = create_graph(n, matrix_cost)
    
    start_time = time.time()
    '''run simulated annealing'''
    sa = SimulatedAnnealing(G, temp, alpha, stopping_temp, stopping_iter, matrix_cost, 13500)
    sa.anneal()
    
    '''show the improvement'''
    sa.print_solution(start_time)

    '''ploting solution'''
    sa.plotLearning_diameter()
    sa.plotLearning_weight()
    sa.plotLearning_best_solution_diameter()
    
if __name__ == "__main__":
    main()



