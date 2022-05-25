
from skimage import exposure
import numpy as np



view_noises = {
    "terrain" : { 
        "atr" :{
            "tundra"            : [[0,0]] ,
            "rainforest"        : [[2,2]] ,
            "desert"            : [[0,2],[0,1]] ,
            "grassland"         : [[1,1],[2,1]],
            "mountain"          : [[1,0],[2,0]] ,
            "forest"            : [[1,2]]
            },
        "interval" : 3,
        "atr_names": ["rain","heat"],
        "atr_list" : ["tundra","rainforest","desert","grassland","mountain","forest"]
    },
    "civilisation" : { 
        "atr" :{
            "ruins"         : [[0,2]],   
            "metropol"      : [[2,2]],       
            "city"          : [[2,1],[1,2],[2,0]],       
            "town"          : [[1,1]],      
            "wild"          : [[0,0],[0,1],[1,0]],           
            },
        "interval" : 3,
        "atr_names": ["population","history"],
        "atr_list" : ["ruins","metropol","city","town","wild"]
    },
    "threat" : { 
        "atr" :{
            "very_high" : [[5,5]],   
            "high"      : [[4,4]],       
            "medium"    : [[3,3]],       
            "low"       : [[2,2]],   
            "very_low"  : [[1,1]],       
            "safe"      : [[0,0]],           
            },
        "interval" : 6,
        "atr_names": ["threat","threat"],
        "atr_list" : ["very_high","high","medium","low","very_low","safe"]
    },
    "faction" : { 
        "atr" :{
            "fac1_main"      :  [[2,0]],   
            "fac1_ext"       :  [[2,1],[1,0]],       
            "fac2_main"      :  [[0,2]],       
            "fac2_ext"       :  [[1,2],[0,1]],
            "warzone"        :  [[1,1],[2,2]],
            "undisputed"     :  [[0,0]]
            },
        "interval" : 3,
        "atr_names": ["fac1","fac2"],
        "atr_list" : ["fac1_main","fac1_ext","fac2_main","fac2_ext","warzone","undisputed"]

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