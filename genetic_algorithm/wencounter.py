
import random

from genetic_algorithm.world_encounters import *
from map_manager.map_attributer import *


class w_encounter:
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
    def __init__(self,map,type="",size=25,encounter_type=""):

        self.pack = []

        for _ in range(size):
            ind = w_encounter(map=map,type=type,encounter_type="")
            self.pack.append(ind)

        self.pack_fitness = [ind.fitness for ind in self.pack]