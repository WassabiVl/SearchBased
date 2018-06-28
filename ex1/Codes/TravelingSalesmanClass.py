from itertools import permutations
import datetime
import random
from copy import deepcopy
from typing import List

from ex1.code.CalcualatorClass import CalculatorClass

trail_points = [
    [0, 0],
    [1, 5.7],
    [2, 3],
    [3, 7],
    [0.5, 9],
    [3, 5],
    [9, 1],
    [10, 5],
    [20, 5],
    [12, 12],
    [20, 19],
    [25, 6],
    [23, 7]
]


# *permutations* returns tuples with all possible orderings without repeat
# function returns minimum of all possible tuples by the help of the function *total_distance* from above
class TravelingSalesman:

    @staticmethod
    def traveling_salesman(points: List[float], start: float = None) -> list:
        calculator_class = CalculatorClass()
        """
        Finds the shortest route to visit all the cities by bruteforce.
        Time complexity is O(N!), so never use on long lists.
        """
        if start is None:
            start = points[0]
        return min([perm for perm in permutations(points) if perm[0] == start], key=calculator_class.total_distance)

    @staticmethod
    def main(points: List = None):
        calculator_class = CalculatorClass()
        points = points[:-5]
        # points = points[:-4]
        # points = points[:-3]
        # points = points[:-2]

        then = datetime.datetime.now()
        result = TravelingSalesman.traveling_salesman(points)
        distance_result = calculator_class.total_distance(result)
        now = datetime.datetime.now()
        return "calculation time", now - then, """
        The minimum distance to visit all 
        of the following points:\n
        {0}
    
        starting at
        {1} is {2} and takes this
        route:
        {3}""".format(
            points,
            points[0],
            distance_result,
            result)


traveling_salesman = TravelingSalesman()
class_calculator = CalculatorClass()
with open('city100.txt', 'r') as coord_file:
    coords = class_calculator.read_coords(coord_file)
print(traveling_salesman.main(coords))
