import datetime
import random
from copy import deepcopy
from typing import List, Tuple, Union, Any, Dict
from PIL import Image, ImageDraw, ImageFont
import matplotlib as plt

from Codes.CommonClass import CommonClass


class HillClimbing:

    def __init__(self, trail_coordinates):
        self.trail_coordinates = trail_coordinates
        self.common_class = CommonClass('city100.txt')
        self.hill_climbing_matrix = self.common_class.main_matrix()

    def do_hc_evaluations(self, max_evaluations: int, init_function) -> List[int]:

        move_operator = HillClimbing.swapped_cities
        then = datetime.datetime.now()
        objective_function = lambda tour: HillClimbing.tour_length(self, tour)  # this should return the length of
        # the tour
        num_evaluations, best_score, best = HillClimbing.hc(init_function, move_operator, objective_function,
                                                            max_evaluations)
        now = datetime.datetime.now()
        print("computation time ", now - then)
        print(best_score)
        print(best)
        filename = "test" + str(max_evaluations) + ".PNG"
        HillClimbing.write_tour_to_img(self.trail_coordinates, best, filename, open(filename, "ab"))
        HillClimbing.reload_image_for_jupyter(filename)
        return best

    @staticmethod
    def reload_image_for_jupyter(filename: str) -> None:
        # pick a random integer with 1 in 2 billion chance of getting the same
        # integer twice
        import random
        __counter__ = random.randint(0, 2e9)

        # now use IPython's rich display to display the html image with the
        # new argument
        from IPython.display import HTML, display
        display(HTML('<img src="./' + filename + '?%d" alt="Schema of adaptive filter" height="100">' % __counter__))

    @staticmethod
    def write_tour_to_img(coords: List[Tuple[float, float]], tour, title: str, img_file) -> None:
        padding = 20
        # shift all coords in a bit
        coords = [(x + padding, y + padding) for (x, y) in coords]
        maxx, maxy = 0, 0
        for x, y in coords:
            maxx = max(x, maxx)
            maxy = max(y, maxy)
        maxx += padding
        maxy += padding
        img = Image.new("RGB", (int(maxx), int(maxy)), color=(255, 255, 255))

        font = ImageFont.load_default()
        d = ImageDraw.Draw(img)
        num_cities = len(tour)
        for i in range(num_cities):
            j = (i + 1) % num_cities
            city_i = tour[i]
            city_j = tour[j]
            x1, y1 = coords[city_i]
            x2, y2 = coords[city_j]
            d.line((int(x1), int(y1), int(x2), int(y2)), fill=(0, 0, 0))
            d.text((int(x1) + 7, int(y1) - 5), str(i), font=font, fill=(32, 32, 32))

        for x, y in coords:
            x, y = int(x), int(y)
            d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(0, 0, 0), fill=(196, 196, 196))

        d.text((1, 1), title, font=font, fill=(0, 0, 0))

        del d
        img.save(img_file, "PNG")

    @staticmethod
    def hc(init_function, move_operator, objective_function, max_evaluations) -> Tuple[
        Union[int, Any], Any, Any]:
        """
        Hillclimb until either max_evaluations is
        reached or we are at a local optima.
        """
        best = init_function
        best_score = objective_function(best)

        num_evaluations = 1

        while num_evaluations < max_evaluations:
            # move around the current position
            move_made = False
            for next_line in move_operator(best):
                if num_evaluations >= max_evaluations:
                    break

                next_score = objective_function(next_line)
                num_evaluations += 1
                if next_score < best_score:
                    best = next_line
                    best_score = next_score
                    move_made = True
                    break  # depth first search
            if not move_made:
                break  # couldn't find better move - must be a local max
        return num_evaluations, best_score, best

    def tour_length(self, tour: List[int]) -> float:
        """Sum up the total length of the tour based on the distance matrix"""
        result = 0
        num_cities = len(list(tour))
        for i in range(num_cities):
            j = (i + 1) % num_cities
            city_i = tour[i]
            city_j = tour[j]
            result += self.hill_climbing_matrix[city_i, city_j]
        return result

    @staticmethod
    def all_pairs(size, shuffle=random.shuffle):
        r1 = list(range(size))
        r2 = list(range(size))
        if shuffle:
            shuffle(r1)
            shuffle(r2)
        for i in r1:
            for j in r2:
                yield (i, j)  # yield is an iterator function
                # for each call of the generator it returns the next value in yield

    # Tweak 1
    @staticmethod
    def swapped_cities(tour):
        """
        Generator to create all possible variations where two
        cities have been swapped
        """
        for i, j in HillClimbing.all_pairs(len(tour)):
            if i < j:
                copy = deepcopy(tour)
                copy[i], copy[j] = tour[j], tour[i]
                yield copy

    # Tweak 2
    @staticmethod
    def reversed_sections(tour):
        """
        Generator to return all possible variations where the
        section between two cities are swapped.
        It preserves entire sections of a route,
        yet still affects the ordering of multiple cities in one go.
        """
        for i, j in HillClimbing.all_pairs(len(tour)):
            if i != j:
                copy = deepcopy(tour)
                if i < j:
                    copy[i:j + 1] = reversed(tour[i:j + 1])
                else:
                    copy[i + 1:] = reversed(tour[:j])
                    copy[:j] = reversed(tour[i + 1:])
                if copy != tour:  # not returning same tour
                    yield copy

    """
       :param input_tour_length: the starting length 
       :return: a list of points to visit
   """
    @staticmethod
    def init_random_tour(input_tour_length: int):
        new_tour = list(range(input_tour_length))
        random.shuffle(list(new_tour))
        return new_tour

    """
    Steepest Ascent Hill Climbing
    :param init_function: 
    :param move_operator: 
    :param objective_function: 
    :param max_evaluations: 
    :param num_tweaks: 
    :return: 
   """
    def hc_steepest_ascent(self, init_function, move_operator, objective_function, max_evaluations, num_tweaks):
        best = init_function()
        best_score = objective_function(best)

        num_evaluations = 1

        while num_evaluations < max_evaluations:
            if num_evaluations >= max_evaluations:
                break
            move_made = False
            r = next(move_operator(best))
            r_score = objective_function(r)
            for n in range(num_tweaks):
                w = next(move_operator(best))
                w_score = objective_function(w)
                if w_score < r_score:
                    r = w
                    r_score = w_score
            num_evaluations += 1
            if r_score < best_score:
                best = r
                best_score = r_score
                move_made = True
            if not move_made:
                break
        return num_evaluations, best_score, best

    def do_hc_steepest_ascent_evaluations(self, evaluations: int, move_operator=swapped_cities, num_tweaks=20):
        max_evaluations = evaluations
        then = datetime.datetime.now()
        num_evaluations, best_score, best = HillClimbing.hc_steepest_ascent(self,init_function,
                                                                            move_operator,
                                                                            objective_function,
                                                                            max_evaluations,
                                                                            num_tweaks)
        now = datetime.datetime.now()

        print("computation time ", now - then)
        print(best_score)
        print(best)
        filename = "test" + str(max_evaluations) + ".PNG"
        plt.figure(figsize=(10, 15))
        img = create_image(coords, best, filename)
        imshow(np.array(img), aspect=1)
        # reload_image_for_jupyter(filename)
