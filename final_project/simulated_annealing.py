import networkx as nx
from initial_solution import *
import numpy as np 
import math
import random
from nodes_generator import NodeGenerator
from animated_visualizer import *
from grid import PointGenerator

class SimulatedAnnealing:
    def __init__(self, original_graph, temp, alpha, stopping_temp, stopping_iter, matrix_cost):
        ''' animate the solution over time

            Parameters
            ----------
            coords: array_like
                list of coordinates
            temp: float
                initial temperature
            alpha: float
                rate at which temp decreases
            stopping_temp: float
                temperature at which annealing process terminates
            stopping_iter: int
                interation at which annealing process terminates

        '''
        self.temp = temp
        self.alpha = alpha
        self.stopping_temp = stopping_temp
        self.stopping_iter = stopping_iter

        
        
        self.iteration = 1
        self.original_graph = original_graph
        self.sample_size = nx.number_of_nodes(self.original_graph)
        self.dist_matrix = matrix_cost
        
        self.graph = generate_random_tree(self.original_graph)
        self.curr_solution = self.graph
        self.best_solution = self.curr_solution
        
        self.curr_weight = self.weight(self.curr_solution)
        self.initial_weight = self.curr_weight
        self.min_weight = self.curr_weight

        self.curr_diameter = self.calculate_diameter(self.curr_solution)
        self.initial_diameter = self.curr_diameter
        self.min_diameter = self.curr_diameter

        self.weight_list = [self.curr_weight]
        self.diameter_list = [self.curr_diameter]
        
        self.solution_history = [self.curr_diameter]
        
        print('Intial weight: ', self.curr_weight)
        print('Initial diameter: ', self.curr_diameter)
        
    def weight(self, candidate):
        '''
        Calculate weight
        '''
        total_cost = 0
        for i,j in candidate.edges():
            total_cost += self.dist_matrix[i,j]

        return total_cost

    def calculate_diameter(self, candidate):
        e = nx.eccentricity(candidate)
        return e[max(e, key=e.get)]
    
    def acceptance_probability(self, candidate_weight):
        '''
        Acceptance probability using boltzmann:
        '''
        return math.exp(-abs(candidate_weight - self.curr_weight) / self.temp)

    def accept(self, candidate):
        '''
        Accept with probability 1 if candidate solution is better than
        current solution, else accept with probability equal to the
        acceptance_probability()
        '''
        # candidate_weight = self.weight(candidate)
        # if candidate_weight < self.curr_weight:
        #     self.curr_weight = candidate_weight
        #     self.curr_solution = candidate
        #     if candidate_weight < self.min_weight:
        #         self.min_weight = candidate_weight
        #         self.best_solution = candidate
        # else:
        #     if random.random() < self.acceptance_probability(candidate_weight):
        #         self.curr_weight = candidate_weight
        #         self.curr_solution = candidate
        
        
        candidate_diameter = self.calculate_diameter(candidate)
        if candidate_diameter < self.curr_diameter:
            self.curr_diameter = candidate_diameter
            self.curr_solution = candidate
            if candidate_diameter < self.min_diameter:
                self.min_diameter = candidate_diameter
                self.best_solution = candidate
        else:
            if random.random() < self.acceptance_probability(candidate_diameter):
                self.curr_diameter = candidate_diameter
                self.curr_solution = candidate

    def anneal(self):
        '''
        Annealing process with 2-opt
        described here: https://en.wikipedia.org/wiki/2-opt
        '''
        while self.temp >= self.stopping_temp and self.iteration < self.stopping_iter:
            candidate = NodeGenerator(self.original_graph, self.curr_solution).generate()

            self.accept(candidate)
            self.temp *= self.alpha
            self.iteration += 1
            # self.weight_list.append(self.curr_weight)
            self.diameter_list.append(self.curr_solution)
            self.solution_history.append(self.calculate_diameter(self.curr_solution))

        # print('Minimum weight: ', self.min_weight)
        # print('Improvement: ',
        #       round((self.initial_weight - self.min_weight) / (self.initial_weight), 4) * 100, '%')
        print('Minimum diameter: ', self.min_diameter)
        print('Improvement: ',
              round((self.initial_diameter - self.min_diameter) / (self.initial_diameter), 4) * 100, '%')

    def animateSolutions(self):        
        animateTSP(self.solution_history)

    def plotLearning(self):
        plt.plot([i for i in range(len(self.solution_history))], self.solution_history)
        line_init = plt.axhline(y=self.initial_diameter, color='r', linestyle='--')
        line_min = plt.axhline(y=self.min_diameter, color='g', linestyle='--')
        plt.legend([line_init, line_min], ['Initial Diameter', 'Optimized Diameter'])
        plt.ylabel('Diameter')
        plt.xlabel('Iteration')
        plt.show()
