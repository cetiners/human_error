
from map_manager.map_attributer import view_noises
import numpy as np

import math
from itertools import combinations

def ranger(map_name,map_1_range):

    r = view_noises[map_name]["interval"]
    r_b = []
    min_val = map_1_range[1]
    max_val = map_1_range[0]

    inc = (max_val-min_val)/r

    for i in range(1,r):
        r_b.append(min_val + (inc*i))
    return r_b
    
def map_attribute_checker(map_1, map_2, map_1_range, map_2_range,map_name,double=True):

    if not double:
        map_2,map_2_range = map_1,map_1_range

    map_1_increments = ranger(map_name,map_1_range)
    map_2_increments = ranger(map_name,map_2_range)

    size = map_1.shape[0]

    attribute_map = np.zeros((size,size))
    
    for i in range(size):
        for j in range(size):

            idx = 0
            for k in map_1_increments:
                
                if map_1[i,j] > k:
                    idx += 1

            idy = 0
            for k in map_2_increments:
                if map_2[i,j] > k:
                    idy += 1

            for atr_n, atr in view_noises[map_name]["atr"].items(): 
                if [idx,idy] in atr:
                    attribute_name = atr_n

            attribute_map[i,j] = int(view_noises[map_name]["atr_list"].index(attribute_name))

    return attribute_map


def dist(p1, p2):

    """
    Calculates the average distance between a bunch of points
    """
    (x1, y1), (x2, y2) = p1, p2
    
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    x = [89.86, 23.0, 9.29, 55.47, 4.5, 59.0, 1.65, 56.2, 18.53, 40.0]
    y = [78.65, 28.0, 63.43, 66.47, 68.0, 69.5, 86.26, 84.2, 88.0, 111.0]

    points = list(zip(x,y))
    distances = [dist(p1, p2) for p1, p2 in combinations(points, 2)]
    avg_distance = sum(distances) / len(distances)