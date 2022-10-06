from skimage import exposure
import numpy as np

view_noises = {
    "terrain" : { 
        "atr" :{
            "tundra"            : [[0,0]],
            "rainforest"        : [[2,2]],
            "desert"            : [[0,2]],
            "grassland"         : [[1,1],[1,2],[0,1]],
            "mountain"          : [[1,0],[2,0]] ,
            "forest"            : [[2,1]]
            },
        "interval" : 3,
        "atr_names": ["rain","heat"],
        "atr_list" : ["tundra","rainforest","desert","grassland","mountain","forest"]
    },
    "civilisation" : { 
        "atr" :{ 
            "wild"          : [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4],[5,5]],
            "countryside"   : [[6, 6], [7, 7], [8, 8]],      
            "city"          : [[9,9]],       
          
            },
        "interval" : 10,
        
        "atr_names": ["population","population"],
        "atr_list" : ["wild","countryside","city"]
    },
    "threat" : { 
        "atr" :{
            "9" : [[9,9]],
            "8" : [[8,8]],
            "7" : [[7,7]],
            "6" : [[6,6]],
            "5" : [[5,5]],   
            "4" : [[4,4]],       
            "3" : [[3,3]],       
            "2" : [[2,2]],   
            "1" : [[1,1]],       
            "0" : [[0,0]],           
            },
        "interval" : 10,
        "atr_names": ["threat","threat"],
        "atr_list" : ["9","8","7","6","5","4","3","2","1","0"]
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

    },
    "story_act" : {
        "atr" :{
            0      :  [[0,0]],
            1      :  [[1,1]],
            2      :  [[2,2]],
            },
        "interval" : 3,
        "atr_names": ["act","act"],
        "atr_list" : [0,1,2]
    },


}

def histeq(img,  alpha=1):
    """
    Histogram equalization of a grayscale image.
    """
    img_cdf, bin_centers = exposure.cumulative_distribution(img)
    img_eq = np.interp(img, bin_centers, img_cdf)
    img_eq = np.interp(img_eq, (0, 1), (-1, 1))
    return alpha * img_eq + (1 - alpha) * img

def average_cells(vor, data):
    """
    Averages the values of the cells in the Voronoi diagram.
    """

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
    """
    Fills the cells in the Voronoi diagram with the average value.
    """
    size = vor.shape[0]
    image = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            p = vor[i, j]
            image[i, j] = data[p]

    return image


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