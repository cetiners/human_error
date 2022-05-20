
from skimage import exposure
import numpy as np



view_noises = {
# number of different types, [rain,heat] , 0 (min) - 2 (max)
    "terrain" : { 
        "atr" :{
            "tundra"         : [0,0] ,
            "rainforest"     : [2,2] ,
            "desert"         : [0,2] ,
            "grassland"      : [1,1] ,
            "mountain/rocky" : [1,0] ,
            "forest"         : [1,2] ,
            "wetland"        : [2,1] ,
            "drought"        : [0,1] ,
            "mountain/forest" : [2,0]
            },
        "interval" : 3,
        "atr_names": ["rain","heat"],
        "atr_list" : ["tundra","rainforest","desert","grassland","mountain/rocky","forest","wetland","drought","mountain/forest"]
    }
 }

def histeq(img,  alpha=1):
    img_cdf, bin_centers = exposure.cumulative_distribution(img)
    img_eq = np.interp(img, bin_centers, img_cdf)
    img_eq = np.interp(img_eq, (0, 1), (-1, 1))
    return alpha * img_eq + (1 - alpha) * img

def average_cells(vor, data):
    """Returns the average value of data inside every voronoi cell"""
    size = vor.shape[0]
    count = np.max(vor)+1

    sum_ = np.zeros(count)
    count = np.zeros(count)

    for i in range(size):
        for j in range(size):
            p = vor[i, j]
            count[p] += 1
            sum_[p] += data[i, j]

    average = sum_/count
    average[count==0] = 0

    return average

def fill_cells(vor, data):
    size = vor.shape[0]
    image = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            p = vor[i, j]
            image[i, j] = data[p]

    return image