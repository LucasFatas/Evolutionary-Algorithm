import os
import random
import sys
from TSPData import TSPData
from Chromosome import Chromosome
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# TSP problem solver using genetic algorithms.
class GeneticAlgorithm:

    # Constructs a new 'genetic algorithm' object.
    # @param generations the amount of generations.
    # @param popSize the population size.
    # @param mutation_probability the probability of mutating
    # @param crossover_probability the probability of crossover
    def __init__(self, generations, pop_size, mutation_probability, crossover_probability):
        self.generations = generations
        self.pop_size = pop_size
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability

    # Knuth-Yates shuffle, reordering a array randomly
    # @param chromosome array to shuffle.
    def shuffle(self, chromosome):
        n = len(chromosome)
        for i in range(n):
            r = i + int(random.uniform(0, 1) * (n - i))
            swap = chromosome[r]
            chromosome[r] = chromosome[i]
            chromosome[i] = swap
        return chromosome

    # This method should solve the TSP.
    # @param pd the TSP data.
    # @return the optimized product sequence.
    def solve_tsp(self, tsp_data):
        num_of_products = len(tsp_data.start_to_product)
        population = []
        path = []
        for i in range(num_of_products):
            path.append(i)
        for i in range(self.pop_size):
            path = self.shuffle(path)
            chromosome = Chromosome(path.copy(), tsp_data)
            population.append(chromosome)
        print("Generation 1:", "Min :", population[0].distance)
        for i in range(2, self.generations+1):

            population = self.create_next_gen(population, tsp_data)


            population.sort(key=lambda x: x.distance, reverse=False)
            print("Generation ", i, "Min :" , population[0].distance)
        population.sort(key=lambda x: x.distance, reverse=False)
        return population[0].path

    # This function creates the new population
    # @param population current population
    # @param tsp_data distances from AOC algorithm
    # @return new_population the new population
    def create_next_gen(self, population, tsp_data):

        population.sort(key=lambda x: x.distance, reverse=False)

        new_population = []
        for i in range(round(self.pop_size/2)):
            if random.uniform(0, 1) < self.mutation_probability:
                rand_chromosome = population[self.two_rand_chromosomes(population)[0]].path
                mutated_path = self.mutate(rand_chromosome).copy()
                new_population.append(Chromosome(mutated_path, tsp_data))
            elif random.uniform(0, 1) < self.crossover_probability:
                rands = self.two_rand_chromosomes(population)
                paths = self.create_offspring(population[rands[0]].path, population[rands[1]].path)
                new_population.append(Chromosome(paths[0].copy(), tsp_data))
                new_population.append(Chromosome(paths[1].copy(), tsp_data))
        while len(new_population) != len(population):
            new_population.append(population[0])
        return new_population

    # this is our mutation function, takes a path and "mutates" it by randomly swapping two products positions
    # @param path the path that needs to be mutated
    def mutate(self, path):
        size = len(path)
        indexes = np.random.choice(size, 2)
        temp = path[indexes[0]]
        path[indexes[0]] = path[indexes[1]]
        path[indexes[1]] = temp
        return path

    # picks two random chromosomes from our population, using fitness
    # @param population the population the chromosomes need to be picked from
    # @return the index of the chromosomes randomly picked
    def two_rand_chromosomes(self, population):
        min_distance = population[0].distance
        fitness = []
        for chromosome in population:
            fitness.append(100*(1-(chromosome.distance-min_distance)))
        sum2 = sum(fitness)
        fitness_ratio = []
        for f in fitness:
            fitness_ratio.append(f/sum2)
        return np.random.choice(self.pop_size, 2, fitness)

    # implements order crossover
    # @param parent1 the first parent
    # @param parent2 the second parent
    # @return two child chromosomes path
    def create_offspring(self, parent1, parent2):
        size = len(parent1)
        child1 = np.full(size, -1)
        child2 = np.full(size, -1)

        start, end = sorted([random.randrange(size) for _ in range(2)])
        for i in range(start, end+1):
            child1[i] = parent1[i]
            child2[i] = parent2[i]
        index1 = end + 1
        index2 = index1
        while index1 != start:
            if index2 >= size:
                index2 = 0
            if index1 >= size:
                if start == 0:
                    break
                index1 = 0
            value = parent2[index2]
            index2 += 1
            if value not in child1:
                child1[index1] = value
                index1 += 1

        index1 = end + 1
        index2 = index1
        while index1 != start:
            if index2 >= size:
                index2 = 0
            if index1 >= size:
                if start == 0:
                    break
                index1 = 0
            value = parent1[index2]
            index2 += 1
            if value not in child2:
                child2[index1] = value
                index1 += 1
        return [list(child1.astype(int)), list(child2.astype(int))]


# Assignment 2.b
if __name__ == "__main__":
    # parameters
    population_size = 1000
    generations = 200
    mutation_probability = 0.05
    crossover_probability = 0.7

    persistFile = "./../tmp/productMatrixDist"

    # setup optimization
    tsp_data = TSPData.read_from_file(persistFile)
    ga = GeneticAlgorithm(generations, population_size, mutation_probability, crossover_probability)

    # run optimzation and write to file
    solution = ga.solve_tsp(tsp_data)
    tsp_data.write_action_file(solution, "./../data/TSP solution.txt")
