# -*- coding: utf-8 -*-

from domain import *
import random


class Repository:
    def __init__(self, seed, population_size, individual_size):
        random.seed(seed)
        self._seed = seed
        self.__populations = [Population(population_size, individual_size)]
        self.map = Map()
        self.population_size = population_size
        self.individual_size = individual_size

    @property
    def seed(self):
        return self._seed

    @property
    def last_iteration(self):
        return self.__populations[-1]

    def add_iteration(self, population):
        self.__populations.append(population)

    def __getitem__(self, item):
        return self.__populations[item]
