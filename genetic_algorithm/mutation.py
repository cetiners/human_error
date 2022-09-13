from map_manager.world_encounters import *
import random



def inversion_mutation(pack):

    mutation_point = random.randint(0,pack.size-1)
    mutation_times = random.randint(0,pack.size-1)

    for _ in range(mutation_times):
        
        offspring = pack.pack[mutation_point]

        coord = offspring.coord

        mutated = [coord[-1], coord[0]]

        offspring.coord = mutated

        pack.update_pack_coord()
        pack.update_pack_fitness()
    
    return pack

 
