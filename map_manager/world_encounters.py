import random

from map_manager.map_attributer import *


encounter_biomes ={

"friendly_animals" : {

    "tundra"        : ["arctic_fox","arctic_hare"],
    "rainforest"   : ["sloth", "tapir", "spider_monkey", "parrot", "macaw", "capybara", "iguana"],
    "desert"       : ["camel", "meerkat", "lizard", "tortoise", "ferret"],
    "grassland"    : ["horse", "bison", "gecko", "deer", "elephant", "gopher"],
    "mountain"     : ["goat", "donkey", "gazelle", "hare"], 
    "forest"       : ["squirrel", "deer", "rabbit"]

},

"hostile_animals" : {

    "tundra"        : ["wolf","bear"],
    "rainforest"   : ["tiger", "jaguar", "snake", "poison_dart_Frog", "fire_ant", "mosquitos"],
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
    "rainforests"   : ["wood_choppers", "wilds", "climate_activists"],
    "deserts"       : ["tuskan_raiders", "fury_road","sand_storm","heat_wave"],
    "grasslands"    : ["hunters","animal_migration"],
    "mountains"     : ["monk","tourists"], 
    "forests"       : ["witches_house","cult_meeting"]

}
}

class w_encounter:

    """
        Handles placements for the world encounters, given the map. Checks the appropriate map placements 
        considering biomes, danger level and civilisation to calculate the appropriate fitness.
    """

    def __init__(self,map,size=1024,type="",encounter_type=""):

        self.coord = [round(random.uniform(0, size),1) for i in range(2)]
        self.check_coor = [int(i) for i in self.coord]

    def check_fitness(self,encounter_type):
        
            fitness = 0
            civ = map.views["civilisation"][self.check_coor[0],self.check_coor[1]]
            biome = view_noises["terrain"]["atr_list"][(int(map.views["terrain"][self.check_coor[0], self.check_coor[1]]))]

            if (civ == 0) | (civ != 4):
                fitness -= 1000

            biomes = encounter_biomes[encounter_type]

            if type not in biomes[biome]:
                fitness -= 1000

            self.fitness = fitness

class pack:

    """
        Creates a set or a "pack" of w_encounter individuals, returns a list of individuals within
        the pack and their individual fitnesses
    """

    def __init__(self,map,type="",size=25,encounter_type=""):

        self.pack = []
        
        for _ in range(size):
            ind = w_encounter(map=map,type=type,encounter_type="")
            self.pack.append(ind)

        self.pack_fitness = [ind.fitness for ind in self.pack]