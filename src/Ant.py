import os
import sys
import random
from Route import Route
from Direction import Direction

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Class that represents the ants functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.rand = random
        
        self.rand.seed(30)

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self):
        route = Route(self.start)

        visited = set()
        visited.add(self.start)

        # surr_pheromone = self.maze.get_surrounding_pheromone(self.current_position)
        directions = [Direction.east, Direction.north, Direction.west, Direction.south]

        # iteration = 15
        # for loop in range(iteration):
        while self.current_position != self.end:
            surr_pheromone = self.maze.get_surrounding_pheromone(self.current_position)

            possible_positions = [self.current_position.add_direction(d) for d in Direction]
            weights = [surr_pheromone.east, surr_pheromone.north, surr_pheromone.west, surr_pheromone.south]

            for index, pos in enumerate(possible_positions):
                if pos in visited:
                    weights[index] = 0

            total_pheromones = sum(weights)

            if total_pheromones == 0:
                self.current_position = self.current_position.subtract_direction(route.remove_last())
                continue

            for w in range(len(weights)):
                weights[w] /= total_pheromones

            direction = self.rand.choices(population=directions, weights=weights)[0]

            # Change the direction of the ant
            self.current_position = self.current_position.add_direction(direction)

            # Add to the route and to the list of visited positions
            visited.add(self.current_position)
            route.add(direction)

        return route
