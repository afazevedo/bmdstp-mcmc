from nodes_generator import NodeGenerator
from simulated_annealing import SimulatedAnnealing
from read_files import *

def main():
    '''set the simulated annealing algorithm params'''
    temp = 1000
    stopping_temp = 0.00000001
    alpha = 0.9995
    stopping_iter = 1000

    # '''set the dimensions of the grid'''
    size_width = 200
    size_height = 200

    path = 'D:\\mndzvd\\Documentos\\GitHub\\project_mcmc\\instances\\states_brazil.txt'
    
    '''set the number of nodes'''
    n, matrix_cost = readFiles(path)
    G = create_graph(n, matrix_cost)

    # initial_solution()

    # '''generate random list of nodes'''
    

    '''run simulated annealing algorithm with 2-opt'''
    sa = SimulatedAnnealing(G, temp, alpha, stopping_temp, stopping_iter, matrix_cost)
    sa.anneal()

    '''animate'''
    # sa.animateSolutions()

    '''show the improvement over time'''
    sa.plotLearning()


if __name__ == "__main__":
    main()
