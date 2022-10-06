
from map_engine.map_attributer import view_noises
import numpy as np

def basic_distance(coord_1, coord_2):

    x2 = (coord_1[0]-coord_2[0])**2
    y2 = (coord_1[1]-coord_2[1])**2
    dist = np.sqrt((x2+y2))
    
    return dist

