import operator
import numpy.random as npr
import numpy as np

def fps(population):

    #min_val = min(population.population, key=operator.attrgetter('pack_fitness')).pack_fitness
    max = sum([i.pack_fitness for i in population.population])

    if max == 0:

        selected_individual_1 = population.population[npr.choice(len(population.population))]
        selected_individual_2 = population.population[npr.choice(len(population.population))]

        while selected_individual_1 == selected_individual_2:

            selected_individual_2 = population.population[npr.choice(len(population.population))]
    
    else:
        selection_probs = [c.pack_fitness/max for c in population.population]
        selection_probs = [1-i for i in selection_probs]

        selected_individual_1 = population.population[npr.choice(len(population.population), p=selection_probs)]
        selected_individual_2 = population.population[npr.choice(len(population.population), p=selection_probs)]

        while selected_individual_1 == selected_individual_2:
            selected_individual_2 = population.population[npr.choice(len(population.population), p=selection_probs)]
    
    return selected_individual_1, selected_individual_2


def rank_selection(population):

    ranked_pop = sorted(population.population, key=operator.attrgetter('pack_fitness'))
    
    rank_sum = (population.size * (population.size +1) / 2)

    selection_p = []

    for rank, _ in enumerate(ranked_pop):

        selection_p.append((rank+1)/rank_sum)

    selected_individual_1 = ranked_pop[npr.choice(population.size, p=selection_p)]
    selected_individual_2 = ranked_pop[npr.choice(population.size, p=selection_p)]

    while selected_individual_1 == selected_individual_2:
        selected_individual_2 = ranked_pop[npr.choice(population.size, p=selection_p)]

    return selected_individual_1, selected_individual_2