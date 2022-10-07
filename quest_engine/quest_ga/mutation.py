
import random

def q_complete_mutation(quest):
    """
    Takes a "pack" of world encounters, completely randomizes the coordinates of each encounter.
    """

    new_coords = [[round(random.uniform(0, 1024-1),1) for i in range(2)] for i in range(quest.steps)]

    quest.path = new_coords
        
    quest.update()

    return quest

def q_point_mutation(quest):

    point = quest.fitnesses.index(min(quest.fitnesses))

    quest.path[point] = [round(random.uniform(0, 1024-1),1) for i in range(2)] 
        
    quest.update()

    return quest

def q_random_point_mutation(quest):

    point = random.randint(0,quest.steps-1)
    quest.path[point] = [round(random.uniform(0, 1024-1),1) for i in range(2)] 
        
    quest.update()

    return quest


def curate_mutation(q1):
    pass