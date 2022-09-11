import operator
from random import uniform


#def fps(population):
#    min_fitness = min(population.population, key=operator.attrgetter('pack_fitness')).pack_fitness
#
#    # Sum total fitnesses with adjustment
#    total_fitness = 
#
#    # Get a 'position' on the wheel
#    spin = uniform(0, total_fitness)
#    
#    position = 0
#
#    # Find individual in the position of the spin
#
#    for individual in population.population:
#
#        position += individual.pack_fitness
#
#        if position > spin:
#
#            return individual    
#

import numpy.random as npr

def fps(population):

    min_val = min(population.population, key=operator.attrgetter('pack_fitness')).pack_fitness

    max = sum([i.pack_fitness + abs(min_val) for i in population.population])

    selection_probs = [(c.pack_fitness + abs(min_val))/max for c in population.population]

    selected_individual = population.population[npr.choice(len(population.population), p=selection_probs)]
    
    return selected_individual