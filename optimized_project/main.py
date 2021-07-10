from nodes_generator import NodeGenerator
from simulated_annealing import SimulatedAnnealing
from read_files import *

def main():
    '''set the simulated annealing algorithm params'''
    temp = 100
    stopping_temp = 0.00000001
    alpha = 0.9995
    # alpha = 0.96
    stopping_iter = 10000

    path = 'D:\\mndzvd\\Documentos\\GitHub\\project_mcmc\\instances\\states_brazil.txt'
    
    '''set the number of nodes'''
    n, matrix_cost = readFiles(path)
    G = create_graph(n, matrix_cost)


    '''run simulated annealing algorithm with 2-opt'''
    sa = SimulatedAnnealing(G, temp, alpha, stopping_temp, stopping_iter, matrix_cost, 12733)
    sa.anneal()

    '''animate'''
    # sa.animateSolutions()

    '''show the improvement over time'''
    sa.plotLearning()
    
    
    


if __name__ == "__main__":
    main()
