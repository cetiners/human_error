import operator
from select import select
import numpy.random as npr
import numpy as np
from operator import itemgetter

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


def curate_selection(q_line):

    ranked_pop = sorted(q_line, key=itemgetter(1))
    rank_sum = (len(ranked_pop) * (len(ranked_pop) +1) / 2)

    selection_p = []

    for rank in range(len(ranked_pop)):
            
        selection_p.append((rank+1)/rank_sum)

    selected_individual_1 = ranked_pop[npr.choice(len(ranked_pop), p=selection_p)]
    selected_individual_2 = ranked_pop[npr.choice(len(ranked_pop), p=selection_p)]
    
    while selected_individual_1 == selected_individual_2:
        selected_individual_2 = ranked_pop[npr.choice(len(ranked_pop), p=selection_p)]
        
    return selected_individual_1, selected_individual_2