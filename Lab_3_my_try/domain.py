# -*- coding: utf-8 -*-
import pickle
from random import *
from utils import *
import numpy as np
from numpy import average, nanstd


class Gene:
    def __init__(self):
        self._movement = choice(DIRECTIONS)

    @property
    def movement(self):
        return self._movement

    def __getitem__(self, item):
        return self._movement[item]

    def __str__(self):
        return '(' + str(self._movement[0]) + ', ' + str(self._movement[1]) + ')'


class Individual:
    def __init__(self, size=0):
        self.__size_of_path = size
        self.__path = [Gene() for _ in range(self.__size_of_path)]
        self.__fitness = None

    @property
    def fitness(self):
        return self.__fitness

    @property
    def size_of_path(self):
        return self.__size_of_path

    @property
    def path(self):
        return self.__path

    @fitness.setter
    def fitness(self, fitness):
        self.__fitness = fitness

    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability:
            self.__path[randint(0, self.__size_of_path - 1)] = Gene()

    def crossover(self, otherParent, crossoverProbability=0.8):
        offspring1, offspring2 = Individual(self.__size_of_path), Individual(self.__size_of_path)
        if random() < crossoverProbability:
            position_of_splitting = randint(1, self.__size_of_path - 2)
            offspring1.__path = self.__path[:position_of_splitting] + otherParent.__path[position_of_splitting:]
            offspring2.__path = otherParent.__path[:position_of_splitting] + self.__path[position_of_splitting:]
            return offspring1, offspring2

        return self, otherParent

    def __gt__(self, other):
        return self.__fitness > other.fitness

    def __lt__(self, other):
        return self.__fitness < other.fitness

    def __str__(self):
        to_print = 'Individual: ' + str(self.__fitness) + ' path: '
        for gene in self.__path:
            to_print += str(gene)

        return to_print


class Population:
    def __init__(self, populationSize=0, individualSize=0):
        self.__populationSize = populationSize
        self.__population = [Individual(individualSize) for _ in range(populationSize)]
        self.__size = 0

    def add_individual(self, individual):
        self.__population.append(individual)

    def fitness_average(self):
        return average([individual.fitness for individual in self.__population])

    def fitness_standard_deviation(self):
        return nanstd([individual.fitness for individual in self.__population])

    def get_best_individuals(self, index):
        self.__population.sort(reverse=True)
        return self.__population[:index]

    def __iter__(self):
        self.__size = 0
        return self

    def __next__(self):
        if self.__size < len(self.__population):
            item = self.__population[self.__size]
            self.__size += 1
            return item
        else:
            raise StopIteration


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def save_map(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
            f.close()

    def load_map(self, filename):
        with open(filename, "rb") as f:
            data = pickle.load(f)
            self.n = data.width
            self.m = data.height
            self.surface = data.surface
            f.close()

    def get_position(self, x, y):
        return self.surface[x][y]
