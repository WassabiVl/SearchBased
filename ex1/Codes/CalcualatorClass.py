from typing import List

# http://www.psychicorigami.com/2007/05/12/tackling-the-travelling-salesman-problem-hill-climbing/
cartesian_points = List[float]


class CalculatorClass:

    @staticmethod
    def distance(p1: cartesian_points, p2: cartesian_points) -> float:
        """
        Returns the Euclidean distance of two points in the Cartesian Plane.
        """
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    @staticmethod
    def total_distance(points: List[List[float]]) -> float:
        """
        Returns the length of the path passing throught
        all the points in the given order.
        """
        return sum([CalculatorClass.distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])

    @staticmethod
    def read_coords(file_handle):
        coords = []
        for line in file_handle:
            x, y = line.strip().split(',')
            coords.append((float(x), float(y)))
        return coords


