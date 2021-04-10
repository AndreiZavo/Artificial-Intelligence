from time import time

from repository import *
import matplotlib.pyplot as plotlib
from random import random


class Controller:
    def __init__(self):
        self._map = Map()
        self._current_population_size = 1
        self._current_coordinates = (-1, -1)
        self._battery = 20
        self._mutation_probability = 0.04
        self._crossover_probability = 0.8
        self._generations = 20
        self._population_size = 20
        self._parent_count = 6
        self._current_repo = None
        self._repositories = []

    @property
    def map(self):
        return self._map

    @property
    def current_coordinates(self):
        return self._current_coordinates

    def iteration(self):
        population = self._current_repo.last_iteration
        for individual in population:
            self.compute_fitness(individual)

        best_individuals = population.get_best_individuals(self._parent_count)

        second_population = Population()

        for i in range(self._population_size // 2):
            first_individual = choice(best_individuals)
            second_individual = choice(best_individuals)

            first_offspring, second_offspring = first_individual.crossover(
                second_individual, self._crossover_probability)

            second_population.add_individual(first_offspring)
            second_population.add_individual(second_offspring)

        for individual in second_population:
            individual.mutate(self._mutation_probability)

        return population, second_population

    def run(self):
        for i in range(self._generations):
            population, new_population = self.iteration()
            self._current_repo.add_iteration(new_population)

    def solver(self, count=1):
        for i in range(count):
            start = time()
            self._current_repo = Repository(random(), self._population_size, self._battery)
            self._repositories.append(self._current_repo)
            self.run()
            end = time()
            duration = end - start
            if int(duration) == 1:
                print(duration, "second needed to compute run", self._current_population_size)
            else:
                print(duration, "seconds needed to compute run", self._current_population_size)
            self._current_population_size += 1

    def create_map(self, width, height, fill):
        self._map = Map(width, height)
        self._map.randomMap(fill)

    def save_map(self, filename):
        self._map.save_map(filename)

    def load_map(self, filename):
        self._map.load_map(filename)

    def get_size_of_map(self):
        return self._map.n * 20, self._map.m * 20

    def discover(self, position, surface, width, height):
        for direction in DIRECTIONS:
            x, y = (position[0] + direction[0], position[1] + direction[1])
            while 0 <= x < width and 0 <= y < height and self._map.get_position(x, y) != 1:
                if surface[x][y] == 0:
                    surface[x][y] = 2
                x, y = (position[0] + x, position[1] + y)

    def compute_fitness(self, individual: Individual):
        fitness = 0
        current_position = self._current_coordinates
        map_width = self._map.n
        map_height = self._map.m

        surface = np.zeros((map_width, map_height))
        surface[current_position[0]][current_position[1]] = 1

        self.discover(current_position, surface, map_width, map_height)

        for gene in individual.path:
            (x, y) = (current_position[0] + gene[0], current_position[1] + gene[1])
            if not (0 <= x < map_width and 0 <= y < map_height):
                fitness -= 8
                break
            if self._map.get_position(x, y) == 1:
                fitness -= 8
                break
            if surface[x][y] == 1:
                fitness -= 5
            surface[x][y] = 1
            self.discover(current_position, surface, map_width, map_height)
            current_position = (x, y)

        fitness += len([x for x in range(map_width) for y in range(map_height) if surface[x][y] == 2])
        individual.fitness = fitness

    def _place_drone_random(self):
        while True:
            x = randint(0, self._map.n - 1)
            y = randint(0, self._map.m - 1)
            print(x, y)
            if self._map.get_position(x, y):
                self._current_coordinates = (x, y)
                return

    def set_drone_coordinates(self, coordinates):
        if coordinates == (-1, -1):
            self._place_drone_random()
        else:
            self._current_coordinates = coordinates

    def set_generations(self, generations):
        self._generations = generations

    def set_population_size(self, populationSize):
        self._population_size = populationSize

    def set_battery(self, battery):
        self._battery = battery

    def statistics(self):
        fitness_list = []
        i = 1
        print("Run #, Seed, Fitness")

        for repository in self._repositories:
            best_individual = repository[self._generations - 1].get_best_individuals(1)[0]
            fitness_list.append(best_individual.fitness)
            print(i, ',', repository.seed, ',', best_individual.fitness)
            i += 1

        print("Average fitness:", np.average(fitness_list), "standard deviation:",
              np.nanstd(fitness_list))

        x = []
        y = []
        z = []
        for i in range(self._generations):
            x.append(i)
            population = self._current_repo[i]
            y.append(population.get_best_individuals(1)[0].fitness)
            z.append(population.fitness_average())

        plotlib.plot(x, y, label="Best fitness")
        plotlib.plot(x, z, label="Average fitness")
        plotlib.legend(loc="lower right")
        plotlib.xlabel("Iterations")
        plotlib.ylabel("Fitness score")
        plotlib.show()

    def _get_best_repository(self):
        best_repository = None
        fitness = 0
        for repository in self._repositories:
            individual = repository[self._generations - 1].get_best_individuals(1)[0]
            if individual.fitness > fitness:
                fitness = individual.fitness
                best_repository = repository

        return best_repository

    def get_best_path(self):
        repository = self._get_best_repository()
        path = []
        for gene in repository[self._generations - 1].get_best_individuals(1)[0].path:
            path.append(gene.movement)
        return path
