
from map_engine.map_attributer import view_noises
import numpy as np


def freytags(path):
    """
    Checks an any given array for suitability to the freytag pyramid.
    """
    freytag_fitness = 0 
    
    steps = len(path[:-1])

    if steps == 1:
        
        freytag_fitness = 0

    elif steps == 2:
        if path[0] <= path[1]:
            freytag_fitness -= 1000

    elif steps == 3:

        if path[0] >= path[2]:
            freytag_fitness -=  1000

        if path[0] >= path[1]:
            freytag_fitness -=  1000

        if path[2] >= path[1]:
            freytag_fitness -=  1000

    elif steps == 4:

        if path[0] >= path[3]:
            freytag_fitness -=  1000
        
        if path[0] >= path[1]:
            freytag_fitness -=  1000

        if path[0] >= path[2]:
            freytag_fitness -=  1000

        if path[1] >= path[2]:
            freytag_fitness -=  1000

        if path[1] >= path[3]:
            freytag_fitness -=  1000

        if path[3] >= path[2]:
            freytag_fitness -=  1000
        

    elif steps == 5:
        if path[0] >= path[4]:
            freytag_fitness -=  1000

        if path[0] >= path[3]:
            freytag_fitness -=  1000
        
        if path[0] >= path[1]:
            freytag_fitness -=  1000

        if path[0] >= path[2]:
            freytag_fitness -=  1000

        if path[4] >= path[3]:
            freytag_fitness -=  1000
        
        if path[4] >= path[2]:
            freytag_fitness -=  1000

        if path[4] >= path[1]:
            freytag_fitness -=  1000

        if path[3] >= path[2]:
            freytag_fitness -=  1000

        if path[3] >= path[1]:
            freytag_fitness -=  1000
        
        if path[1]>= path[2]:
            freytag_fitness -=  1000

    return freytag_fitness

def basic_distance(coord_1, coord_2):

    x2 = (coord_1[0]-coord_2[0])**2
    y2 = (coord_1[1]-coord_2[1])**2
    dist = np.sqrt((x2+y2))
    
    return dist


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


encounter_biomes ={

"friendly_animals" : {

    "tundra"        : ["arctic_fox","arctic_hare"],
    "rainforest"   : ["sloth", "tapir", "spider_monkey", "parrot", "macaw", "capybara", "iguana"],
    "desert"       : ["camel", "meerkat", "lizard", "tortoise"],
    "grassland"    : ["horse", "bison", "gecko", "deer", "elephant", "gopher"],
    "mountain"     : ["goat", "donkey", "gazelle", "hare"], 
    "forest"       : ["squirrel", "deer", "rabbit"]

},

"hostile_animals" : {

    "tundra"        : ["wolf","bear"],
    "rainforest"   : ["tiger", "jaguar", "snake", "poison_dart_frog", "fire_ant", "mosquitos"],
    "desert"       : ["bobcat", "lion", "coyote", "rattlesnake", "eagle", "scorpion"],
    "grassland"    : ["dog","wolf"],
    "mountain"     : ["bear", "mountain_lion", "leopard", "wolverine"], 
    "forest"       : ["orangutan", "wild_boar"]

},

"natural_encounters" : {

    "tundra"        : ["ravine","frozen_lake","wind_gust","snow"],
    "rainforest"   : ["overgrowth", "spiky_canopy", "maze", "flood"],
    "desert"       : ["sand_dune", "quicksand"],
    "grassland"    : [],
    "mountain"     : ["thunderstorm", "avalanche", "cliff", "ravine"],
    "forest"       : ["fallen_tree"]

},

"special_encounters" : {

    "tundra"        : ["cannibals","frozen_figure"],
    "rainforest"   : ["wood_choppers", "wilds", "climate_activists"],
    "desert"       : ["tuskan_raiders", "fury_road","sand_storm","heat_wave"],
    "grassland"    : ["hunters","animal_migration"],
    "mountain"     : ["monk","tourists"], 
    "forest"       : ["witches_house","cult_meeting"]

}
}

all_encounters = []

required_n_enc = {}

for i in encounter_biomes:
    for j in encounter_biomes[i]:
        for k in encounter_biomes[i][j]:
            if i == "friendly_animals":
                required_n_enc[k] = 50
            elif i == "hostile_animals":
                required_n_enc[k] = 20
            elif i == "natural_encounters":
                required_n_enc[k] = 10
            else:
                required_n_enc[k] = 5 


#
#a = [i.check_coor for i in ]
#cmap = colors.ListedColormap(["dodgerblue","white","yellowgreen","khaki","lawngreen","slategrey","darkgreen"])
#civ = nw.views["civilisation"].copy()
#ter = nw.views["terrain"].copy()
#
#fig, ax = plt.subplots(1,2)
#fig.set_dpi(150)
#fig.set_size_inches(12, 8)
#
#
#ax[0].imshow(ter.T,cmap=cmap,alpha=.66)
#ax[0].set_title("Terrain")
#ax[0].scatter(x=[i[0] for i in a], y=[i[1] for i in a],color="Black",s=25,marker="4")
#
#ax[1].imshow(civ.T,cmap="Blues",alpha=0.66)
#ax[1].set_title("Civilisation")
#ax[1].scatter(x=[i[0] for i in a], y=[i[1] for i in a],color="Black",s=25,marker="4")

