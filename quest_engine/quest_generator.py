# dex: Stealth, Steal, 
# str
# con
# int
# wis 
# cha

import random
import numpy as np
from tools.utils import basic_distance, freytags
from map_manager.map_attributer import view_noises

class quest:
    """
    Class that holds attributes of a single quest.

    Attributes:
        map (str):          The map the quest is on.
        quest_type (str):   The attributes quest focuses on, origin of the challange.
        difficulty (int):   The difficulty level of the quest.
        act (str):          The overall game act that the quest belongs to.
        quest_steps (int):  The number of keys and locks in the quest.
        quest_radius (int): Total distance needed to travel for the quest.
        fitness (int):      The fitness of the quest.

    """
    
    def __init__(self, map, max_steps=5):

        self.map = map
        self.challange_type = [np.random.choice(["dex", "str", "con", "int", "wis", "cha"]) for i in range(2)]        

        self.steps = random.randint(1,max_steps)
        self.path = []
        self.is_npc = [random.getrandbits(1) for i in range(self.steps-1)]
        self.is_npc.append(1)

        for i in range(self.steps):
            self.path.append([round(random.uniform(0, map.size-1),1) for i in range(2)])   
        self.path.append(self.path[0])

        print(self.path)

        self.point_distances()
        self.difficulty = self.check_difficulty()
        self.fitness = self.check_fitness()
        self.act = self.act_check()
        


    def check_fitness(self):

        fitness = 0 

        ## Total distance and individual distances.

        if self.dist_dict["total"] > 512:

            fitness -= 1000

        if max(self.dist_dict["individual"]) > 256:

            fitness -= 1000

        for location in self.path:

        ## If the quest giver is not in populus areas, punish the fitness.
            if (int(self.map.views["civilisation"][int(location[0]),int(location[1])])) < 2:
                fitness -= 1000

            elif (int(self.map.views["civilisation"][int(location[0]),int(location[1])])) < 3:
                fitness -= 500
        ## If quest key/locks are in sea, punish the fitness substantially.

            if (int(self.map.views["terrain"][int(location[0]),int(location[1])]))  == 0:
                fitness -= 10000

        ## Check the quest progression for threat, if it does not fit the Freytag's Pyramid, punish the fitness.

        fitness += freytags(self.check_threat())

        self.fitness = fitness

        return self.fitness

    def check_threat(self):

        path_check = [[int(i) for i in j] for j in self.path]
        path_threat = []

        for i in path_check:
            threat_level = view_noises["threat"]["atr_list"][(int(self.map.views["threat"][i[0], i[1]])-1)]
            path_threat.append(int(threat_level))

        return path_threat
        
    def act_check(self):

        path = [[int(i) for i in j] for j in self.path]
        path_act = []

        for i in path:
            act = view_noises["threat"]["atr_list"][(int(self.map.views["story_act"][i[0], i[1]])-1)]
            path_act.append(int(act))

        return path_act

    def check_difficulty(self):
        self.difficulty = 0
        return self.difficulty

    def point_distances(self):
        self.dist_dict = {}
        distances = []
        for i in range(len(self.path)-1):
            distances.append(basic_distance(self.path[i], self.path[i+1]))
        self.dist_dict["total"] = sum(distances)
        self.dist_dict["individual"] = distances

class quest_line:

    def __init__(self):

        self.theme = [np.random.choice(["dex", "str", "con", "int", "wis", "cha"]) for i in range(2)]
        self.fitness = self.check_fitness()

    def check_fitness(self):
        self.fitness = 0
        return self.fitness
