from Codes.HillClimbingClass import HillClimbing
from Codes.SimulatedAnnealClass import SimulatedAnneal
from Codes.TabuSearchWithILS import TabuSearch
from Codes.CommonClass import CommonClass

common_class = CommonClass('city100.txt')
hill_climbing_matrix = common_class.main_matrix()
trail_coordinates = common_class.trail_coordinates()
hill_climbing = HillClimbing(trail_coordinates)

move_operator = hill_climbing.swapped_cities
# move_operator = hill_climbing.reversed_sections
max_evaluations = 50000
init_function = common_class.get_initial_function()  # returns a random solution
objective_function = lambda tour: hill_climbing.tour_length(hill_climbing_matrix,
                                                            tour)  # this should return the length of the tour
print('hill Climbing')
best = hill_climbing.do_hc_evaluations(max_evaluations, init_function)
print()
print('simulated Anneal')
sim_anneal = SimulatedAnneal(best, 5000)
sim_anneal.anneal()

print()
print('Tabu then ILS search')
tabu_search = TabuSearch(5000, best)
print(tabu_search.main())
