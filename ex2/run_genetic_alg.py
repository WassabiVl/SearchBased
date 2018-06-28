#!python3
import datetime
import math
import random
from typing import List
import numpy as np


def main(the_features, the_interactions, max_evaluations: int = None, num_tweaks: int = None,
         population_size: int = None) -> None:
    then = datetime.datetime.now()
    max_evaluations = 5000 if max_evaluations is None else max_evaluations
    num_tweaks = 30 if num_tweaks is None else num_tweaks
    population_size = 30 if population_size is None else population_size
    length = len(the_features)
    population = []
    for i in range(population_size):
        population.append(initialize_population(length).tolist())
    new_feature, feature_list = transform_key_feature(the_features)
    new_transformation = transform_interaction(the_interactions, feature_list)
    num_evaluations, best_score, best = optimize(new_feature, new_transformation, max_evaluations,
                                                 num_tweaks, population)
    now = datetime.datetime.now()

    print("computation time ", now - then)
    print(best_score)
    print(best)


def optimize(new_feature, new_transformation, max_evaluations: int, num_tweaks: int, populations):
    evaluate = False
    best = None
    best_fitness = 0  # initialize the variable
    num_evaluations = 1  # keep track of how many times the algo run
    tweak_solution = False  # to stop the algo running in the local optima
    full_population = populations  # to reduce children creation that are a replica of the parents

    while num_evaluations < max_evaluations:
        if num_evaluations >= max_evaluations:
            break
        for population in populations:
            pi_fitness = assess_fitness(population, new_feature, new_transformation)
            if best is None or pi_fitness > best_fitness:
                best = population
                best_fitness = assess_fitness(best, new_feature, new_transformation)
                print("best", best, best_fitness, "num_evaluations: ", num_evaluations)
                evaluate = True
        Q = []
        if num_evaluations % num_tweaks == 0 and evaluate is False:
            for i in range(int(len(populations) / 2)):
                parent_a = next(select(populations, new_feature, new_transformation))
                parent_b = next(select(populations, new_feature, new_transformation))
                child_a, child_b = line_recombination_algorithm(parent_a, parent_b)
                Q, full_population = add_to_q(Q, mutate(child_a), mutate(child_b), full_population, num_tweaks)
            num_evaluations += 1
            if not Q:  # if the randomize returned an empty list, break out of loop
                print("second", num_evaluations)
                break
            elif tweak_solution is True:
                populations = tweak(Q)
                tweak_solution = False
            else:
                populations = Q
                tweak_solution = True
        else:  # mutation half-life starts here
            evaluate = False
            # for i in range(int(population_size / 2)):
            for i in range(int(len(populations) / 2)):
                parent_a = next(select(populations, new_feature, new_transformation))
                parent_b = next(select(populations, new_feature, new_transformation))
                child_a, child_b = crossover(parent_a, parent_b)
                Q, full_population = add_to_q(Q, child_a, child_b, full_population, num_tweaks)
            num_evaluations += 1
            if not Q:  # if the randomize returned an empty list, break out of loop
                print("first", num_evaluations, Q)
                break
            populations = Q
    return num_evaluations, best_fitness, best


def initialize_population(length: int) -> np.ndarray:
    return np.random.randint(2, None, length)


def mutate(solution: List[int]) -> List[int]:
    for i in range(len(solution)):
        probability = np.random.randint(1, 100)
        if probability >= 50:
            solution[i] = (solution[i] + 1) % 2  # convert 1 and 0 using mod
    return solution


def tweak(solution):
    for i, j in all_pairs(len(solution)):
        if i < j:
            solution[i], solution[j] = solution[j], solution[i]
    return solution


def all_pairs(size: int):
    shuffle = random.shuffle
    r1 = np.random.randint(2, None, size)
    r2 = np.random.randint(2, None, size)
    if shuffle:
        shuffle(r1)
        shuffle(r2)
    for i in r1:
        for j in r2:
            yield (i, j)  # yield is an iterator function


def select(populations, new_feature, new_transformation):
    sorted(populations, key=lambda solution: assess_fitness(solution, new_feature, new_transformation), reverse=True)
    for pop in populations:
        if isinstance(pop, (np.ndarray, np.generic)):
            yield (pop.tolist())
        else:
            yield (pop)


def crossover(solution_a, solution_b):
    # uniform crossover with probability of 50% and higher
    for i in range(len(solution_a)):
        if solution_b[i] != solution_a[i]:  # reduce processing time by ignoring any gene that is similar
            probability = random.randint(1, 100)
            if probability >= 50:
                solution_a[i], solution_b[i] = solution_b[i], solution_a[i]
    return solution_a, solution_b


def assess_fitness(solution, features, interaction):
    """Sum up the total performance value of the solution"""
    result = 0
    # add the features first
    for i, k in enumerate(solution):
        if k == 1:
            result += features[i]
    # add the interactions second
    for i, k in enumerate(solution):
        for x, y in enumerate(solution):
            if k == 1 and y == 1:
                try:
                    result += interaction[i, x]
                except KeyError:
                    continue
                else:
                    result += interaction[i, x]
    return result


def read_txt(path):
    result = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        name = line.split(" ")[0][:-1]
        names = name.split("#")
        value = float(line.split(" ")[1].strip())
        configuration = [names, value]
        result.append(configuration)
    return result


def transform_key_feature(features):
    new_feature = []
    feature_list = []
    for x in features:
        new_feature.append(x[1])
        feature_list.append(x[0])
    return new_feature, feature_list


def transform_interaction(interactions, features_list):
    new_interaction = {}
    replace = {}
    for k, z in enumerate(features_list):
        replace[z[0]] = k
    for x in interactions:
        # for y in x:
        i = replace[x[0][0]]
        j = replace[x[0][1]]
        new_interaction[i, j] = x[1]
    return new_interaction


def line_recombination_algorithm(solution_a, solution_b):
    outreach_p = 0.25
    alpha = random.uniform(-outreach_p, 1 + outreach_p)
    beta = random.uniform(-outreach_p, 1 + outreach_p)
    for i in range(len(solution_a)):
        if solution_a[i] != solution_a[i]:
            t = alpha * solution_a[i] + (1 - alpha) * solution_b[i]
            s = beta * solution_b[i] + (1 - beta) * solution_a[i]
            if (math.isclose(t, 0, rel_tol=1e-2) or math.isclose(t, 1, rel_tol=1e-2)) and (
                    math.isclose(s, 0, rel_tol=1e-2) or math.isclose(s, 1, rel_tol=1e-2)):
                solution_a[i] = int(t)
                solution_b[i] = int(s)
    return solution_a, solution_b


def add_to_q(Q, child_a, child_b, full_population, num_tweaks):
    something = 0
    if child_a in full_population and child_b not in full_population:
        Q.append(child_b)
        full_population.append(child_b)
        while child_a in full_population and something < num_tweaks:
            child_a = mutate(child_a)
            something += 1
        Q.append(child_a)
    elif child_a not in full_population and child_b in full_population:
        Q.append(child_a)
        full_population.append(child_a)
        while child_b in full_population and something < num_tweaks:
            child_b = mutate(child_b)
            something += 1
        Q.append(child_b)
    elif child_a not in full_population and child_b not in full_population:
        Q.append(child_a)
        Q.append(child_b)
        full_population.append(child_b)
        full_population.append(child_a)
    else:
        while child_b in full_population and something < num_tweaks:
            child_b = mutate(child_b)
            something += 1
        Q.append(child_b)
        something = 0
        while child_a in full_population and something < num_tweaks:
            child_a = mutate(child_a)
            something += 1
        Q.append(child_a)
    return Q, full_population


# if __name__ == "__main__":
#     # input scheme: run_genetic_alg.py model_features.txt model_interactions.txt
#     if len(sys.argv) != 3:
#         print("Not a valid input! Please use:" + \
#               "python3 run_genetic_alg.py model_features.txt model_interactions.txt")
#         sys.exit(0)
#     features = read_txt(sys.argv[1])
#     interactions = read_txt(sys.argv[2])
#     main(features, interactions)


feature_file = 'bdbc_feature.txt'
interaction_file = 'bdbc_interactions.txt'
new_features = read_txt(feature_file)
new_interactions = read_txt(interaction_file)
print("bdbc")
main(new_features, new_interactions)

feature_file = 'h264_feature.txt'
interaction_file = 'h264_interactions.txt'
new_features = read_txt(feature_file)
new_interactions = read_txt(interaction_file)
print("h264")
main(new_features, new_interactions)
