from map_manager.world_encounters import *

import random
import copy



def inversion_mutation(pack):

    
    mutation_times = random.randint(0,pack.size-1)
    offspring_pack = copy.deepcopy()

    for _ in range(mutation_times):
        
        mutation_point = random.randint(0,pack.size-1)
        
        offspring = pack.pack[mutation_point]

        coord = offspring.coord

        mutated = [coord[-1], coord[0]]

        offspring.coord = mutated

        pack.update_pack_coord()
        pack.update_pack_fitness()
    
    return pack


def complete_mutation(pack):

    new_coords = [[round(random.uniform(0, 1024-1),1) for i in range(2)] for i in range(pack.size)]

    for i in range(len(new_coords)):
        pack.pack[i].coord = new_coords[i]

    pack.update_pack_coord()
    pack.update_pack_fitness()

    return pack
