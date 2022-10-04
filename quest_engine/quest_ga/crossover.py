
import random


def q_ax_pmx(parent_1,parent_2):
    
    from quest_engine.quest_generator import quest 


    """
    
    """

    parent_1_coor_x = [i[0] for i in parent_1.path] 
    parent_2_coor_x = [i[0] for i in parent_2.path]
    parent_1_coor_y = [i[1] for i in parent_1.path] 
    parent_2_coor_y = [i[1] for i in parent_2.path]

    

    offspring_1 = quest(parent_1.map,parent_1.steps)
    offspring_2 = quest(parent_2.map,parent_2.steps)
    
    cut_points = [random.randint(0,parent_1.steps-1)]

    second_cut = random.randint(0,parent_1.steps-1)
    
    while second_cut == cut_points[0]:
        second_cut = random.randint(0,parent_1.steps-1)
    
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

    for i in range(len(offspring_1.path)):

        offspring_1.path[i] = [new_coord_1_x[i],new_coord_1_y[i]]

    for i in range(len(offspring_2.path)):

        offspring_2.path[i] = [new_coord_2_x[i],new_coord_2_y[i]]

    offspring_1.update()
    offspring_2.update()
    
    return offspring_1,offspring_2


def q_sp_xo(parent_1,parent_2):
    from quest_engine.quest_generator import quest 

    cut_point = random.randint(0,parent_1.steps-1)

    p1_coords = parent_1.path
    p2_coords = parent_2.path

    offspring_1 = quest(parent_1.map,parent_1.steps)
    offspring_2 = quest(parent_2.map,parent_2.steps)

    offspring_1.path = p2_coords[:cut_point] + p1_coords[cut_point:]
    offspring_2.path = p1_coords[:cut_point] + p2_coords[cut_point:]

    offspring_1.update()
    offspring_2.update()

    return offspring_1,offspring_2



    





