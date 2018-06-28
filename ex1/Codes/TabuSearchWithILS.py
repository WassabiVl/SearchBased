from typing import List, Dict
from random import randint
from Codes.CommonClass import CommonClass


class TabuSearch:
    def __init__(self, iteration: int = -1, initial_function: List[float] = None, repeat_tabu: int = -1) -> None:
        self.common_class = CommonClass('city100.txt')
        self.matrix: dict = self.common_class.main_matrix()
        self.init_function: List[int] = self.common_class.get_initial_function() if initial_function is not None \
            else initial_function  # returns a random solution
        self.objective_function: float = self.common_class.tour_length(self.matrix, self.init_function)  # length of the
        # initial solution
        print('initial length ' + self.objective_function.__str__())
        self.iteration = 5000 if iteration == -1 else iteration
        self.trail_coordinates = self.common_class.trail_coordinates()
        self.repeat_tabu = 2 if repeat_tabu == -1 else repeat_tabu

    def main(self) -> Dict:
        optimum_matrix = None
        optimum_length: int = None
        repeat_tabu: int = 0
        start_iteration: int = 0
        start_index: int = 0
        start_matrix = self.init_function
        start_length = self.objective_function
        # start of the tabu search
        for j in range(0, self.iteration):
            for i in range(len(self.init_function)):
                new_matrix = TabuSearch.switch_neighbor(start_matrix, start_index)
                new_length = self.common_class.tour_length(self.matrix, new_matrix)
                if new_length < start_length:
                    start_matrix = new_matrix
                    start_length = new_length
                start_iteration += 1
            if start_index < len(self.init_function) - 1:
                start_index += 1
            else:
                start_index = 0
                repeat_tabu += 1
                # start of the ILS search hoping to find another minial
                if optimum_length is not None and start_length > optimum_length and repeat_tabu == self.repeat_tabu:
                    common_class = CommonClass('city100.txt')
                    some_matrix = common_class.get_initial_function()
                    some_length = common_class.tour_length(self.matrix, some_matrix)
                    while some_length > optimum_length:
                        some_matrix = common_class.get_initial_function()
                        some_length = common_class.tour_length(self.matrix, some_matrix)
                    start_matrix = some_matrix
                    start_length = some_length
                else:
                    optimum_length = start_length
                    optimum_matrix = start_matrix
        print('Best fitness obtained: ', optimum_length)
        print('Improvement over initial heuristic: ',
              round((self.objective_function - optimum_length) / self.objective_function, 4))
        self.common_class.plot_routes(optimum_matrix, self.trail_coordinates)
        return {'optimal matrix': optimum_matrix}

    @staticmethod
    def switch_neighbor(matrix: List[int], index: int) -> List[int]:
        random_integer = randint(index, len(matrix) - 1)
        matrix[index], matrix[random_integer] = matrix[random_integer], matrix[index]
        return matrix
