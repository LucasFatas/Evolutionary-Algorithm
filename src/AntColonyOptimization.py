import os
import sys
import time
from Maze import Maze
from Ant import Ant
from PathSpecification import PathSpecification

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, maze, ants_per_gen, generations, q, evaporation):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation

    # Loop that starts the shortest path process
    # @param spec Specification of the route we wish to optimize
    # @return ACO optimized route
    def find_shortest_route(self, path_specification):

        shortest_path = None

        for iterations in range(self.generations):
            # Creates the ants for a single generation
            ants = [Ant(self.maze, path_specification) for _ in range(self.ants_per_gen)]
            routes = [ant.find_route() for ant in ants]

            for r in routes:
                if shortest_path is None or shortest_path.size() > r.size():
                    shortest_path = r

            self.maze.evaporate(self.evaporation)
            self.maze.add_pheromone_routes(routes, self.q)

        return shortest_path


# Prints the matrix containing the pheromones
def print_pheromones(pheromones, width, length):
    string = "\nPheromone Matrix\n"
    # string += str(width)
    # string += " "
    # string += str(length)
    # string += " \n"

    for y in range(length):
        for x in range(width):
            string += str(pheromones[x][y])
            string += " "
        string += "\n"

    print(string)


# Driver function for Assignment 1
if __name__ == "__main__":
    # parameters
    gen = 20
    no_gen = 1000
    q = 1600
    evap = 0.10

    # construct the optimization objects
    maze = Maze.create_maze("./../data/hard maze.txt")
    spec = PathSpecification.read_coordinates("./../data/hard coordinates.txt")
    aco = AntColonyOptimization(maze, gen, no_gen, q, evap)

    # print(maze)
    # print(spec)

    # save starting time
    start_time = int(round(time.time() * 1000))

    # run optimization
    shortest_route = aco.find_shortest_route(spec)
    print(f"Shortest route: {shortest_route}")

    # print time taken
    print("Time taken: " + str((int(round(time.time() * 1000)) - start_time) / 1000.0))

    # save solution
    shortest_route.write_to_file("./../data/hard_solution_two.txt")

    # print route size
    print("Route size: " + str(shortest_route.size()))
