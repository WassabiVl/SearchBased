import random
from typing import List, Tuple, Dict

from Codes import visualize_tsp


class CommonClass:

    def __init__(self, filename: str):
        self.filename = filename

    @staticmethod
    def read_coordinates(file_handle) -> List[Tuple]:
        coordinates = []
        for line in file_handle:
            x, y = line.strip().split(',')
            coordinates.append((float(x), float(y)))
        return coordinates

    @staticmethod
    def cartesian_matrix(coordinates: List) -> Dict:
        """
        Creates a distance matrix for the city coords using straight line distances
        computed by the Euclidean distance of two points in the Cartesian Plane.
        """
        matrix = {}
        for i, (x1, y1) in enumerate(coordinates):
            for j, (x2, y2) in enumerate(coordinates):
                dx, dy = x1 - x2, y1 - y2
                car_distance = (dx ** 2 + dy ** 2) ** 0.5
                matrix[i, j] = car_distance
        return matrix

    def trail_coordinates(self) -> List[tuple]:
        with open(self.filename, 'r') as coord_file:
            trail_coordinates = CommonClass.read_coordinates(coord_file)
        return trail_coordinates

    def main_matrix(self):
        trail_coordinates = CommonClass.trail_coordinates(self)
        return CommonClass.cartesian_matrix(trail_coordinates)

    @staticmethod
    def init_random_tour(input_tour_length: int) -> List[int]:
        new_tour = list(range(input_tour_length))
        random.shuffle(new_tour)
        return new_tour

    def get_initial_function(self) -> List[int]:
        trail_coordinates = CommonClass.trail_coordinates(self)
        return CommonClass.init_random_tour(len(trail_coordinates))

    @staticmethod
    def tour_length(input_matrix: Dict, tour: List[int]) -> float:
        """Sum up the total length of the tour based on the distance matrix"""
        result = 0
        num_cities = len(tour)
        for i in range(num_cities):
            j = (i + 1) % num_cities
            city_i = tour[i]
            city_j = tour[j]
            result += input_matrix[city_i, city_j]
        return result

    @staticmethod
    def plot_routes(best_solution, coordinates) -> None:
        """
        Visualize the TSP route with matplotlib
        """
        visualize_tsp.plotTSP2(best_solution, coordinates)
