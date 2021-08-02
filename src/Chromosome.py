import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Chromosome:

    def __init__(self, path, tsp_data):
        self.path = path
        self.distance = self.calculate_distance(tsp_data)

    # calculates distance of path for new chromosomes
    def calculate_distance(self, tsp_data):
        distance = 0
        distance += len(tsp_data.start_to_product[self.path[0]].route)
        for i in range(1, len(self.path)):
            distance += len(tsp_data.product_to_product[self.path[i-1]][self.path[i]].route)
        distance += len(tsp_data.product_to_end[self.path[-1]].route)
        return distance
