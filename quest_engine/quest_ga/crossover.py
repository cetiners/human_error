
import random


def q_ax_pmx(parent_1,parent_2):
    
    from quest_engine.quest_generator import quest 


    """
    
    """

    parent_1_coor_x = [i[0] for i in parent_1.path] 
    parent_2_coor_x = [i[0] for i in parent_2.path]
    parent_1_coor_y = [i[1] for i in parent_1.path] 
    parent_2_coor_y = [i[1] for i in parent_2.path]

    offspring_1 = quest(parent_1.map,parent_1.act,parent_1.steps)
    offspring_2 = quest(parent_2.map,parent_2.act,parent_2.steps)
    
    cut_points_x = [random.randint(0,parent_1.steps-1)]

    second_cut_x = random.randint(0,parent_1.steps-1)
    
    while second_cut_x == cut_points_x[0]:
        second_cut_x = random.randint(0,parent_1.steps-1)
    
    cut_points_x.append(second_cut_x)

    cut_points_x = sorted(cut_points_x)


    cut_points_y = [random.randint(0,parent_1.steps-1)]

    second_cut_y = random.randint(0,parent_1.steps-1)
    
    while second_cut_y == cut_points_y[0]:
        second_cut_y = random.randint(0,parent_1.steps-1)
    
    cut_points_y.append(second_cut_x)

    cut_points_y = sorted(cut_points_x)

    new_coord_1_x = parent_1_coor_x.copy()
    new_coord_2_x = parent_2_coor_x.copy()
    new_coord_1_y = parent_1_coor_y.copy()
    new_coord_2_y = parent_2_coor_y.copy()

    for i in range(cut_points_x[0],cut_points_x[1]+1):
        new_coord_1_x[i] = parent_2_coor_x[i]
        new_coord_2_x[i] = parent_1_coor_x[i]

    for i in range(cut_points_y[0],cut_points_y[1]+1):
        new_coord_1_y[i] = parent_2_coor_y[i]
        new_coord_2_y[i] = parent_1_coor_y[i]

    for i in range(len(offspring_1.path)):
        offspring_1.path[i] = [new_coord_1_x[i],new_coord_1_y[i]]
        offspring_2.path[i] = [new_coord_2_x[i],new_coord_2_y[i]]

    offspring_1.update()
    offspring_2.update()
    
    return offspring_1,offspring_2


def q_sp_xo(parent_1,parent_2):
    from quest_engine.quest_generator import quest 

    cut_point = random.randint(0,parent_1.steps-1)

    p1_coords = parent_1.path
    p2_coords = parent_2.path

    offspring_1 = quest(parent_1.map,parent_1.act, parent_1.steps)
    offspring_2 = quest(parent_2.map,parent_2.act, parent_2.steps)

    offspring_1.path = p1_coords[:cut_point] + p2_coords[cut_point:]
    offspring_2.path = p2_coords[:cut_point] + p1_coords[cut_point:]

    offspring_1.update()
    offspring_2.update()

    return offspring_1,offspring_2


def q_ar_xo(parent_1,parent_2):
    
    from quest_engine.quest_generator import quest 

    """
    
    """
    alpha = random.random()

    parent_1_coor_x = [i[0] for i in parent_1.path] 
    parent_2_coor_x = [i[0] for i in parent_2.path]
    parent_1_coor_y = [i[1] for i in parent_1.path] 
    parent_2_coor_y = [i[1] for i in parent_2.path]

    offspring_1 = quest(parent_1.map,parent_1.act,parent_1.steps)
    offspring_2 = quest(parent_2.map,parent_2.act,parent_2.steps)
    
    cut_points_x = [random.randint(0,parent_1.steps-1)]

    second_cut_x = random.randint(0,parent_1.steps-1)
    
    while second_cut_x == cut_points_x[0]:
        second_cut_x = random.randint(0,parent_1.steps-1)
    
    cut_points_x.append(second_cut_x)

    cut_points_x = sorted(cut_points_x)


    cut_points_y = [random.randint(0,parent_1.steps-1)]

    second_cut_y = random.randint(0,parent_1.steps-1)
    
    while second_cut_y == cut_points_y[0]:
        second_cut_y = random.randint(0,parent_1.steps-1)
    
    cut_points_y.append(second_cut_x)

    cut_points_y = sorted(cut_points_x)

    new_coord_1_x = parent_1_coor_x.copy()
    new_coord_2_x = parent_2_coor_x.copy()
    new_coord_1_y = parent_1_coor_y.copy()
    new_coord_2_y = parent_2_coor_y.copy()

    for i in range(cut_points_x[0],cut_points_x[1]+1):
        new_coord_1_x[i] = ((new_coord_1_x[i]*alpha) + (new_coord_2_x[i]*(1-alpha)))
        new_coord_2_x[i] = ((new_coord_2_x[i]*alpha) + (new_coord_1_x[i]*(1-alpha)))

    for i in range(cut_points_y[0],cut_points_y[1]+1):
        new_coord_1_y[i] = ((new_coord_1_y[i]*alpha) + (new_coord_2_y[i]*(1-alpha)))
        new_coord_2_y[i] = ((new_coord_2_y[i]*alpha) + (new_coord_1_y[i]*(1-alpha)))

    for i in range(len(offspring_1.path)):
        offspring_1.path[i] = [new_coord_1_x[i],new_coord_1_y[i]]
        offspring_2.path[i] = [new_coord_2_x[i],new_coord_2_y[i]]

    offspring_1.update()
    offspring_2.update()
    
    return offspring_1,offspring_2


    





