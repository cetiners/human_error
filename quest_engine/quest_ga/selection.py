import operator
import numpy.random as npr
import numpy as np


def q_rank_selection(population):

    ranked_pop = sorted(population.population, key=operator.attrgetter('fitness',"act_fitness","suitable_fitness","total_dist"))
    
    rank_sum = (population.size * (population.size +1) / 2)

    selection_p = []

    for rank, _ in enumerate(ranked_pop):

        selection_p.append((rank+1)/rank_sum)

    selected_individual_1 = ranked_pop[npr.choice(population.size, p=selection_p)]
    selected_individual_2 = ranked_pop[npr.choice(population.size, p=selection_p)]

    while selected_individual_1 == selected_individual_2:
        selected_individual_2 = ranked_pop[npr.choice(population.size, p=selection_p)]

    return selected_individual_1, selected_individual_2