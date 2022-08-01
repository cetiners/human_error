
from map_manager.world_encounters import *


def coordinate_xo(parent_1, parent_2):

    """
    Takes two individual coordinate points as parents. Takes one coordinate axis from each to create two offsprings.
    """

    child_1 = [parent_1[0],parent_2[1]]
    child_2 = [parent_2[0],parent_1[1]]

    return child_1,child_2

def partially_mapped_xo(parent_1,parent_2):
    """
    Takes a "pack" of world encounters, 
    """
    parent_1_coor = [i.coord for i in parent_1.pack] 
    parent_2_coor = [i.coord for i in parent_2.pack]

    offspring_1 = parent_1.copy()
    offspring_2 = parent_2.copy()
    
    #offspring_1 = pack(parent_1.pack[0].map, type=parent_1.pack[0].type ,size=parent_1.pack[0].size, encounter_type=parent_1.pack[0].encounter_type)
    #offspring_2 = pack(parent_1.pack[0].map, type=parent_1.pack[0].type ,size=parent_1.pack[0].size, encounter_type=parent_1.pack[0].encounter_type)

    "XO Schenenagens"

    cut_points = sorted([random.randint(0,len(parent_1_coor)) for i in range(2)])


    new_coord_1 = parent_1_coor.copy()
    new_coord_2 = parent_2_coor.copy()

    for i in range(cut_points[0],cut_points[1]+1):
    
        new_coord_1[i] = parent_2_coor[i]
        new_coord_2[i] = parent_1_coor[i]

    for i in range(offspring_1.pack):
        offspring_1[i].coord = new_coord_1[i]

    return offspring_1, offspring_2
