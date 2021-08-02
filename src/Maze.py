import os
import sys
import traceback
import numpy as np
from SurroundingPheromone import SurroundingPheromone
from Coordinate import Coordinate
from Direction import Direction

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.walls = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.pheromones = self.initialize_pheromones()

    # Initialize pheromones to a start value.
    def initialize_pheromones(self):
        return self.walls.copy()

    # Reset the maze for a new shortest path problem.
    def reset(self):
        self.initialize_pheromones()

    # Update the pheromones along a certain route according to a certain Q
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_route(self, route, q):
        coordinate = route.start

        for r in route.get_route():
            self.pheromones[coordinate.x][coordinate.y] += q / route.size()
            coordinate = coordinate.add_direction(r)
        return

    # Update pheromones for a list of routes
    # @param routes A list of routes
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    def evaporate(self, rho):
        self.pheromones = [[entry * (1 - rho) for entry in path] for path in self.pheromones]
        return

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    # Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param position The position to check the neighbours of.
    # @return the pheromones of the neighbouring positions.
    def get_surrounding_pheromone(self, position):
        # Checks if the coordinates are within the bounds
        if not self.in_bounds(position):
            return None

        surrounding_pheromones = [0] * 4
        # Creates a list of surrounding pheromones
        for index, direction in enumerate(Direction):
            coord = Coordinate(position.x, position.y).add_direction(direction)

            if self.in_bounds(coord):
                surrounding_pheromones[index] = self.pheromones[coord.x][coord.y]

        # print(f"Surrounding pheromones: {surrounding_pheromones}")
        return SurroundingPheromone(surrounding_pheromones[0], surrounding_pheromones[1], surrounding_pheromones[2],
                                    surrounding_pheromones[3])

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):
        # Checks if the coordinates are within the bounds
        if (pos.x < 0 or pos.x > self.width) or (pos.y < 0 or pos.y > self.length):
            return -1
        return self.pheromones[pos.x][pos.y]

    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])

            # make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])

            for y in range(length):
                line = lines[y + 1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()
