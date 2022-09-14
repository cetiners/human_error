
from map_manager.world_encounters import *
import random
import copy

def partially_mapped_xo(parent_1,parent_2):

    """
    Takes a "pack" of world encounters, selects two random crossing points from the list of encounters and swaps coordinates between them.
    """

    parent_1_coor = [i.coord for i in parent_1.pack] 
    parent_2_coor = [i.coord for i in parent_2.pack]

    offspring_1 = copy.deepcopy(parent_1)
    offspring_2 = copy.deepcopy(parent_2)
    
    cut_points = [random.randint(0,len(parent_1_coor))-1]

    second_cut = random.randint(0,len(parent_1_coor)-1)
    
    while second_cut == cut_points[0]:
        second_cut = random.randint(0,len(parent_1_coor)-1)
    
    cut_points.append(second_cut)
    cut_points = sorted(cut_points)

    new_coord_1 = parent_1_coor.copy()
    new_coord_2 = parent_2_coor.copy()

    for i in range(cut_points[0],cut_points[1]+1):
    
        new_coord_1[i] = parent_2_coor[i]
        new_coord_2[i] = parent_1_coor[i]

    for i in range(len(offspring_1.pack)):

        offspring_1.pack[i].coord = new_coord_1[i]

    for i in range(len(offspring_2.pack)):

        offspring_2.pack[i].coord = new_coord_2[i]

    
    offspring_1.update_pack_coord()
    offspring_2.update_pack_coord()
    offspring_1.update_pack_fitness()
    offspring_2.update_pack_fitness()

    #offspring_1.pack_coord = new_coord_1
    #offspring_2.pack_coord = new_coord_2

    return offspring_1, offspring_2


def ar_xo(parent_1,parent_2):

    """
    Takes a "pack" of world encounters, selects two random crossing points from the list of encounters and uses weighted averages to randomize each points.
    """

    alpha = random.random()

    parent_1_coor = [i.coord for i in parent_1.pack] 
    parent_2_coor = [i.coord for i in parent_2.pack]

    offspring_1 = copy.deepcopy(parent_1)
    offspring_2 = copy.deepcopy(parent_2)
    
    cut_points = [random.randint(0,len(parent_1_coor))-1]

    second_cut = abs(random.randint(0,len(parent_1_coor)-1))
    
    while second_cut == cut_points[0]:
        second_cut = abs(random.randint(0,len(parent_1_coor)-1))
    
    cut_points.append(second_cut)
    cut_points = sorted(cut_points)

    new_coord_1 = parent_1_coor.copy()
    new_coord_2 = parent_2_coor.copy()

    for i in range(cut_points[0],cut_points[1]+1):
    
    # Takes X and Y coordinates and gets the weighted average for each point using alpha value.
    
        new_coord_1[i] = [((new_coord_1[i][0]*alpha) + (new_coord_2[i][0]*(1-alpha))), ((new_coord_1[i][1]*alpha) + (new_coord_2[i][1]*(1-alpha)))]
        new_coord_2[i] = [((new_coord_2[i][0]*alpha) + (new_coord_1[i][0]*(1-alpha))), ((new_coord_2[i][1]*alpha) + (new_coord_1[i][1]*(1-alpha)))]

    for i in range(len(offspring_1.pack)):

        offspring_1.pack[i].coord = new_coord_1[i]

    for i in range(len(offspring_2.pack)):

        offspring_2.pack[i].coord = new_coord_2[i]

    offspring_1.update_pack_coord()
    offspring_2.update_pack_coord()
    offspring_1.update_pack_fitness()
    offspring_2.update_pack_fitness()


    return offspring_1,offspring_2

## Applying XO with X-Y axes seperately

def ax_pmx(parent_1,parent_2):

    """
    Takes a "pack" of world encounters, selects two random crossing points from the list of encounters and swaps coordinates between them.
    """

    parent_1_coor_x = [i.coord[0] for i in parent_1.pack] 
    parent_2_coor_x = [i.coord[0] for i in parent_2.pack]

    parent_1_coor_y = [i.coord[1] for i in parent_1.pack] 
    parent_2_coor_y = [i.coord[1] for i in parent_2.pack]

    offspring_1 = copy.deepcopy(parent_1)
    offspring_2 = copy.deepcopy(parent_2)
    
    cut_points = [random.randint(0,parent_1.size-1)]

    second_cut = random.randint(0,parent_1.size-1)
    
    while second_cut == cut_points[0]:
        second_cut = random.randint(0,parent_1.size-1)
    
    cut_points.append(second_cut)

    cut_points = sorted(cut_points)

    new_coord_1_x = parent_1_coor_x.copy()
    new_coord_2_x = parent_2_coor_x.copy()
    new_coord_1_y = parent_1_coor_y.copy()
    new_coord_2_y = parent_2_coor_y.copy()

    for i in range(cut_points[0],cut_points[1]+1):
    
        new_coord_1_x[i] = parent_2_coor_x[i]
        new_coord_2_x[i] = parent_1_coor_x[i]

        new_coord_1_y[i] = parent_2_coor_y[i]
        new_coord_2_y[i] = parent_1_coor_y[i]

    for i in range(len(offspring_1.pack)):

        offspring_1.pack[i].coord = [new_coord_1_x[i],new_coord_1_y[i]]

    for i in range(len(offspring_2.pack)):

        offspring_2.pack[i].coord = [new_coord_2_x[i],new_coord_2_y[i]]

    
    offspring_1.update_pack_coord()
    offspring_2.update_pack_coord()
    offspring_1.update_pack_fitness()
    offspring_2.update_pack_fitness()

    #offspring_1.pack_coord = new_coord_1
    #offspring_2.pack_coord = new_coord_2

    return offspring_1, offspring_2