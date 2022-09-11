
from map_manager.world_encounters import *
import random
import copy


def coordinate_xo(parent_1, parent_2):

    """
    Takes two individual coordinate points as parents. Takes one coordinate axis from each to create two offsprings.
    """

    child_1 = [parent_1[0],parent_2[1]]
    child_2 = [parent_2[0],parent_1[1]]

    return child_1,child_2

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

    
    offspring_1.update_pack_coord()
    offspring_2.update_pack_coord()
    offspring_1.update_pack_fitness()
    offspring_2.update_pack_fitness()

    #offspring_1.pack_coord = new_coord_1
    #offspring_2.pack_coord = new_coord_2

    return offspring_1, offspring_2
