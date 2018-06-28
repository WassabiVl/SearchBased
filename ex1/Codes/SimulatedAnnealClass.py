import random
import numpy as np
from typing import List
from Codes.CommonClass import CommonClass


class SimulatedAnneal(object):
    def __init__(self, initial_solution, stopping_iter: int = -1, temperature: float = -1, alpha: float = -1,
                 stopping_temperature: float = -1) -> None:
        self.common_class = CommonClass('city100.txt')
        self.coordinates = self.common_class.trail_coordinates()
        self.N = len(self.coordinates)
        self.T = np.sqrt(self.N) if temperature == -1 else temperature
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 0.00000001 if stopping_temperature == -1 else stopping_temperature
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1
        self.dist_matrix = self.common_class.main_matrix()
        self.nodes = [i for i in range(self.N)]

        self.cur_solution = initial_solution
        self.best_solution = self.cur_solution

        self.cur_fitness = self.fitness(self.cur_solution)
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness

        self.fitness_list = [self.cur_fitness]

    def initial_solution(self) -> List[int]:
        """
        Greedy algorithm to get an initial solution (closest-neighbour)
        """
        cur_node = np.random.choice(self.nodes)
        solution = [cur_node]

        free_list = list(self.nodes)
        free_list.remove(cur_node)

        while free_list:
            closest_dist = min([self.dist_matrix[cur_node][j] for j in free_list])
            cur_node = self.dist_matrix[cur_node].index(closest_dist)
            free_list.remove(cur_node)
            solution.append(cur_node)

        return solution

    def fitness(self, sol) -> float:
        start = 0
        for i in range(0, self.N - 1):
            start += self.dist_matrix[sol[i], sol[i + 1]]
        end = self.dist_matrix[sol[0], sol[self.N - 1]]
        """ Objective value of a solution """
        return round(start + end, 4)

    def p_accept(self, candidate_fitness: float) -> float:
        """
        Probability of accepting if the candidate is worse than current
        Depends on the current temperature and difference between candidate and current
        """
        return np.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate: List) -> None:
        """
        Accept with probability 1 if candidate is better than current
        Accept with probabilty p_accept(..) if candidate is worse
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.best_solution = candidate

        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness = candidate_fitness
                self.cur_solution = candidate

    def anneal(self) -> None:
        """
        Execute simulated annealing algorithm
        """
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            l = np.random.randint(2, self.N - 1)
            i = np.random.randint(0, self.N - l)
            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)

        print('Best fitness obtained: ', self.best_fitness)
        print('Improvement over initial heuristic: ',
              round((self.initial_fitness - self.best_fitness) / self.initial_fitness, 4))
        self.common_class.plot_routes(self.best_solution, self.coordinates)

