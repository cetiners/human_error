
import random

from genetic_algorithm.world_encounters import *
from map_manager.map_attributer import *


class animal:
    def __init__(self,map,size=1024,type=""):
        self.coord = [round(random.uniform(0, size),1) for i in range(2)]
        self.check_coor = [int(i) for i in self.coord]

        fitness = 0
        civ = map.views["civilisation"][self.check_coor[0],self.check_coor[1]]
        biome = view_noises["terrain"]["atr_list"][(int(map.views["terrain"][self.check_coor[0], self.check_coor[1]]))]



        if (civ == 0) | (civ != 4):
            fitness -= 1000

        if type not in friendly_animals[biome]:
            fitness -= 1000

        self.fitness = fitness

class herd:
    def __init__(self,map,type="",size=25):

        self.pack = []

        for _ in range(size):
            ind = animal(map=map,type=type)
            self.pack.append(ind)

        self.pack_fitness = [ind.fitness for ind in self.pack]