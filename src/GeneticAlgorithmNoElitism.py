import os
import random
import sys
from TSPData import TSPData

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# TSP problem solver using genetic algorithms.
class GeneticAlgorithm:

    # Constructs a new 'genetic algorithm' object.
    # @param generations the amount of generations.
    # @param popSize the population size.
    def __init__(self, generations, pop_size):
        self.generations = generations
        self.pop_size = pop_size

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
    # @param tsp_data the TSP data.
    # @return the optimized product sequence.
    def solve_tsp(self, tsp_data):
        products = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        overall_min_distance = None
        overall_best_chromosome = None

        # Creates a matrix of random chromosomes
        chromosomes = [self.shuffle(products.copy()) for _ in range(self.pop_size)]

        for iterations in range(self.generations):
            distance_list = [self.compute_distances(c, tsp_data) for c in chromosomes]

            min_distance = min(distance_list)
            max_distance = max(distance_list)

            # Checks for the new optimal path
            if overall_min_distance is None or min_distance < overall_min_distance:
                overall_min_distance = min_distance
                overall_best_chromosome = chromosomes[distance_list.index(min_distance)]

            # print(f"Iteration: {iterations + 1}\tMin Distance: {min_distance}")

            # List of all fitness
            fitness = [self.fitness_function(d, max_distance, min_distance) for d in distance_list]
            overall_fitness = sum(fitness)

            # Determines the weights of each chromosome
            weights = [f / overall_fitness for f in fitness]

            # Creates a new generation
            new_generation = random.choices(chromosomes.copy(), weights, k=self.pop_size)
            new_generation = [c.copy() for c in new_generation]

            # Probability of a chromosome being crossed
            crossover_probability = 0.5

            # Crossing of chromosomes
            for ch_index, c in enumerate(new_generation):
                if random.random() < crossover_probability:
                    self.crossover(c, random.choice(new_generation))

            chromosomes = new_generation    # New generation of chromosomes

        print(f"Min Distance: {overall_min_distance}")

        return overall_best_chromosome, overall_min_distance

    def compute_distances(self, chromosomes, matrix):
        distance = matrix.start_distances[chromosomes[0]]   # Distance between the start and the first product

        for i in range(1, len(chromosomes)):
            # Distance between two products
            distance += matrix.distances[chromosomes[i - 1]][chromosomes[i]]

        # Distance between the last product and the end
        distance += matrix.end_distances[chromosomes[-1]]
        return distance

    def fitness_function(self, distance, max_distance, min_distance):
        if max_distance == min_distance:
            return 100

        function = 100 * (1 - (distance - min_distance) / (max_distance - min_distance))
        return function

    # Crosses chromosomes on the given index
    def crossover(self, ch1, ch2):
        ch1_start = random.randint(0, len(ch1) - 1)
        rand_length = random.randint(1, len(ch1) - ch1_start)
        ch2_start = random.randint(0, len(ch2) - rand_length)

        for index in range(0, rand_length):
            index_of = ch1.index(ch2[ch2_start + index])

            temp = ch1[index_of]
            ch1[index_of] = ch1[ch1_start + index]
            ch1[ch1_start + index] = temp


# Assignment 2.b
if __name__ == "__main__":
    # parameters
    population_size = 1000
    generations = 600
    persistFile = "./../data/productMatrixDist"

    # Setup optimization
    tsp_data = TSPData.read_from_file(persistFile)
    ga = GeneticAlgorithm(generations, population_size)

    for _ in range(20):
        # Run optimization and write to file
        seed = random.randint(0, sys.maxsize)
        random.seed(seed)
        solution, distance_result = ga.solve_tsp(tsp_data)
        tsp_data.write_action_file(solution, f"./../data/TSP solution_{distance_result}_seed_{seed}.txt")
