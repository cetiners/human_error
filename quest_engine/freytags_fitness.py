def freytags(path):
    """
    Checks an any given array for suitability to the freytag pyramid.
    """
    
    steps = len(path)
    freytag_fitness = [0 for i in range(steps)]


    if steps == 1:
        
        freytag_fitness = 0

    elif steps == 2:
        if path[0] >= path[1]:
            freytag_fitness[0] -= 1000
            freytag_fitness[1] -= 1000

    elif steps == 3:

        #if path[0] >= path[2]:
        #    freytag_fitness[0] -=  1000
        #    freytag_fitness[2] -=  1000


        if path[0] >= path[1]:
            freytag_fitness[0] -=  1000
            freytag_fitness[1] -=  1000

        if path[2] >= path[1]:
            freytag_fitness[2] -=  1000
            freytag_fitness[1] -=  1000


    elif steps == 4:

        #if path[0] >= path[3]:
        #    freytag_fitness[0] -=  1000
        #    freytag_fitness[3] -=  1000
        
        if path[0] >= path[1]:
            freytag_fitness[0] -=  1000
            freytag_fitness[1] -=  1000

        if path[0] >= path[2]:
            freytag_fitness[0] -=  1000
            freytag_fitness[2] -=  1000

        if path[1] >= path[2]:
            freytag_fitness[1] -=  1000
            freytag_fitness[2] -=  1000

        if path[1] >= path[3]:
            freytag_fitness[1] -=  1000
            freytag_fitness[3] -=  1000

        if path[3] >= path[2]:
            freytag_fitness[3] -=  1000
            freytag_fitness[2] -=  1000
        

    elif steps == 5:
        #if path[0] >= path[4]:
        #    freytag_fitness[0] -=  1000
        #    freytag_fitness[4] -=  1000

        if path[0] >= path[3]:
            freytag_fitness[0] -=  1000
            freytag_fitness[3] -=  1000
        
        if path[0] >= path[1]:
            freytag_fitness[0] -=  1000
            freytag_fitness[1] -=  1000

        if path[0] >= path[2]:
            freytag_fitness[0] -=  1000
            freytag_fitness[2] -=  1000

        if path[4] >= path[3]:
            freytag_fitness[4] -=  1000
            freytag_fitness[3] -=  1000
        
        if path[4] >= path[2]:
            freytag_fitness[4] -=  1000
            freytag_fitness[2] -=  1000

        if path[4] >= path[1]:
            freytag_fitness[4] -=  1000
            freytag_fitness[1] -=  1000

        if path[3] >= path[2]:
            freytag_fitness[3] -=  1000
            freytag_fitness[2] -=  1000
            
        if path[3] >= path[1]:
            freytag_fitness[3] -=  1000
            freytag_fitness[1] -=  1000
        
        if path[1]>= path[2]:
            freytag_fitness[1] -=  1000
            freytag_fitness[2] -=  1000

    return freytag_fitness


def curate_fitness(curated, max_act):
    
    fitness = sum(freytags([i.difficulty for i in curated]))

    if max([i.act for i in curated],key=[i.act for i in curated].count) != max_act:
        fitness -= 1000

    return fitness