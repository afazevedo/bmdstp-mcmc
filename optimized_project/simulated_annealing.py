import networkx as nx
from initial_solution import *
import numpy as np 
import math
import random
from nodes_generator import NodeGenerator
import matplotlib.pyplot as plt
import time
import os


class SimulatedAnnealing:
    def __init__(self, original_graph, initial_temp, alpha, stopping_temp, stopping_iter, matrix_cost, B):
        ''' 
            Parameters
            ----------
            original_graph: nx.graph
                original graph G
            initial_temp: float
                initial temperature
            alpha: float
                rate at which temp decreases
            stopping_temp: float
                temperature at which annealing process terminates
            stopping_iter: int
                interation at which annealing process terminates
            matrix_cost: array like
                original cost from G
            B: float
                budget from source data
        '''
        
        # set simulated annealing parameters
        self.temp = initial_temp # set temperature to initial temperature
        self.initial_temp = initial_temp
        self.alpha = alpha 
        self.stopping_temp = stopping_temp
        self.stopping_iter = stopping_iter
        self.penalty = 4 # set penalty 
        
        # set initial parameters
        self.iteration = 1
        self.original_graph = original_graph
        self.dist_matrix = matrix_cost
        self.budget = B
        self.curr_solution = generate_random_tree(self.original_graph)
        self.best_solution = nx.Graph.copy(self.curr_solution)
        
        # set initial weight parameters
        self.curr_weight = self.weight(self.curr_solution)
        aux_weight = self.curr_weight
        self.initial_weight = aux_weight
        self.min_weight = aux_weight

        # set initial diameter parameters
        self.curr_diameter = self.calculate_diameter(self.curr_solution)
        aux_diameter = self.curr_diameter
        self.initial_diameter = aux_diameter
        self.min_diameter = aux_diameter

        # set initial list parameters
        self.weight_list = [aux_weight]
        self.diameter_list = [aux_diameter]
        self.solution_history = [initial_temp]
        self.best_solution_history_diameter = []
        self.best_solution_history_weight = []
        
        # print initial log
        print('===================================')
        print('Initial weight: ', aux_weight)
        print('Initial diameter: ', aux_diameter)
            
    def weight(self, candidate):
        '''
        Calculate weight
        '''
        total_cost = 0
        for i,j in candidate.edges():
            total_cost += self.dist_matrix[i,j]

        return total_cost

    def calculate_diameter(self, candidate):
        '''
        Calculate diameter
        '''
        e = nx.eccentricity(candidate)
        return e[max(e, key=e.get)]
    
    def acceptance_probability(self, candidate_diameter):
        '''
        Acceptance probability using boltzmann:
        '''
        return math.exp(-abs(candidate_diameter - self.curr_diameter) / self.temp)

    def accept(self, candidate):
        '''
        Accept with probability 1 if candidate solution is better than
        current solution, else accept with probability equal to the
        acceptance_probability()
        '''
        
        # calculate the diameter and weight of the neighbor
        candidate_diameter = self.calculate_diameter(candidate)
        candidate_weight = self.weight(candidate)
        
        if candidate_weight > self.budget: # if the neighbor's weight is greater than the budget
            candidate_diameter += self.penalty # we penalize the diameter of the neighbor

        # if the diameter of the neighbor is smaller or equal but with a smaller weight, we accept    
        if candidate_diameter < self.curr_diameter or (candidate_diameter == self.curr_diameter and candidate_weight < self.curr_weight):
            candidate_diameter -= self.penalty
            # update current solutions
            self.curr_diameter = candidate_diameter
            self.curr_weight = candidate_weight
            self.curr_solution = candidate
            
            # updates the best solution
            if candidate_weight <= self.budget:
                current = nx.Graph.copy(self.curr_solution)
                self.best_solution = current
                self.best_solution_history_diameter.append(self.calculate_diameter(current))
                self.best_solution_history_weight.append(self.weight(current))
        else:
            candidate_diameter -= self.penalty
            # if not, we will accept according to boltzmann distribution
            unif = random.random() # generate a uniform number between 0 and 1
            if unif < self.acceptance_probability(candidate_diameter):
                
                # # updates the best solution
                # if candidate_diameter <= self.calculate_diameter(self.best_solution):
                #     current = nx.Graph.copy(self.curr_solution)
                #     self.best_solution = current
                #     self.best_solution_history_diameter.append(self.calculate_diameter(current))
                #     self.best_solution_history_weight.append(self.weight(current))
                
                # update current solutions
                self.curr_diameter = candidate_diameter
                self.curr_weight = candidate_weight
                self.curr_solution = candidate
    
    def anneal(self):
        '''
        Annealing process 
        '''
        # as long as the temperature is greater than zero and the number of iterations is less than the maximum number of iterations
        self.iteration = 0
        while self.temp >= self.stopping_temp:
            improve = False 
            while self.iteration < self.stopping_iter:
                
                # we generate a new neighbor
                candidate = NodeGenerator(self.original_graph, self.curr_solution).generate()
                
                # we check whether we transition or not
                self.accept(candidate)
                
                # if the current diameter is greater than or equal to the best diameter found
                if self.calculate_diameter(self.curr_solution) <= self.calculate_diameter(self.best_solution):
                    # if the weight of the current solution is less than or equal to the budget (feasible solution)
                    improve = True
                    if self.weight(self.curr_solution) <= self.budget:
                        # updates the best solution
                        current = nx.Graph.copy(self.curr_solution)
                        self.best_solution = current
                        self.best_solution_history_diameter.append(self.calculate_diameter(current))
                        self.best_solution_history_weight.append(self.weight(current))
                
                # if the current diameter is less than the smallest known diameter
                if self.calculate_diameter(self.curr_solution) < self.min_diameter:
                    # we keep it
                    self.min_diameter = self.calculate_diameter(self.curr_solution)

                # if the current weight is less than the smallest known weight
                if self.weight(self.curr_solution) < self.min_weight:
                    # we keep it
                    self.min_weight = self.weight(self.curr_solution)
        
                # storing a history of solutions
                self.weight_list.append(self.curr_weight)
                self.diameter_list.append(self.curr_diameter)
                self.solution_history.append(self.temp)
                
                # increase the iteration
                self.iteration += 1
            # self.temp = 15/(np.log(self.iteration+1))

            # cooling
            # if not improve:
            #     self.alpha *= 0.5
            
            beta = (self.initial_temp - self.stopping_temp)/(self.stopping_iter*self.initial_temp*self.stopping_temp)
            self.temp = self.temp/(1+beta*self.temp)
            
            # self.temp = self.initial_temp*self.alpha
        
            # update iteration
            self.iteration = 0
        
    def print_solution(self, start_time):
        print('Minimum weight: ', self.min_weight, " ", 'Improvement: ',
            round((self.initial_weight - self.min_weight) / (self.initial_weight), 4) * 100, '%')
        print('Minimum diameter: ', self.min_diameter, " ", 'Improvement: ',
            round((self.initial_diameter - self.min_diameter) / (self.initial_diameter), 4) * 100, '%')
        print('=====================================')
        print('Final solution:')
        index_weight = self.best_solution_history_diameter.index(min(self.best_solution_history_diameter))
        print('Weight: ', self.best_solution_history_weight[index_weight])
        print('Diameter: ', min(self.best_solution_history_diameter))
        print('Iterations:', self.stopping_iter)
        print("--- %s seconds ---" % (time.time() - start_time))
        print('=====================================')

        # nx.draw(self.best_solution, with_labels=True)
        # plt.show()

    def plotLearning_diameter(self):
        number_iterations = len(self.solution_history)

        fig = plt.figure(figsize=(18, 8))
        x_axis = np.linspace(self.initial_temp, self.temp, number_iterations)
        
        plt.plot(x_axis, self.diameter_list, color = 'blue')
        
        line_init = plt.axhline(y = self.initial_diameter, color='r', linestyle='--')
        line_min = plt.axhline(y = min(self.diameter_list), color='g', linestyle='--')
        plt.xlim(self.initial_temp, self.temp)
        
        plt.legend([line_init, line_min], ['Initial Diameter', 'Optimized Diameter'])
        plt.ylabel('Diameter')
        plt.xlabel('Temperature')
        path = os.getcwd()
        plt.savefig(os.path.join(path, 'images', 'grafic1_{}.png'.format(self.budget)), bbox_inches='tight', pad_inches=0.1)
        # plt.show()
    
    def plotLearning_best_solution_diameter(self):
        number_iterations = len(self.best_solution_history_diameter)
        
        fig = plt.figure(figsize=(18, 8))
        x_axis = np.linspace(self.initial_temp, self.temp, number_iterations)
        
        plt.plot(x_axis, self.best_solution_history_diameter, color = 'blue')
        
        line_init = plt.axhline(y = self.initial_diameter, color='r', linestyle='--')
        line_min = plt.axhline(y = min(self.best_solution_history_diameter), color='g', linestyle='--')
        plt.xlim(self.initial_temp, self.temp)
        
        plt.legend([line_init, line_min], ['Initial Diameter', 'Optimized Diameter'])
        plt.ylabel('Diameter')
        plt.xlabel('Temperature')
        # plt.show()
        path = os.getcwd()
        plt.savefig(os.path.join(path, 'images', 'grafic2_{}.png'.format(self.budget)), bbox_inches='tight', pad_inches=0.1)
        
    def plotLearning_weight(self):
        number_iterations = len(self.solution_history)

        fig = plt.figure(figsize=(18, 8))
        x_axis = np.linspace(self.initial_temp, self.temp, number_iterations)
        plt.plot(x_axis, self.weight_list, color = 'blue')

        line_init = plt.axhline(y = self.initial_weight, color='r', linestyle='--')
        line_min = plt.axhline(y = min(self.weight_list), color='g', linestyle='--')
        plt.xlim(self.initial_temp, self.temp)
        
        plt.legend([line_init, line_min], ['Initial Cost', 'Optimized Cost'])
        plt.ylabel('Cost')
        plt.xlabel('Temperature')
        # plt.show()
        path = os.getcwd()
        plt.savefig(os.path.join(path, 'images', 'grafic3_{}.png'.format(self.budget)), bbox_inches='tight', pad_inches=0.1)
