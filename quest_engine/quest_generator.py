# dex: Stealth, Steal, 
# str
# con
# int
# wis 
# cha

import random
import numpy as np
from map_manager.map_attributer import view_noises

class quest:
    """
    Class that holds attributes of a single quest.

    Attributes:
        map (str): The map the quest is on.
        quest_type (str): The attributes quest focuses on, origin of the challange.
        difficulty (int): The difficulty level of the quest.
        arc (str): The overall game arc that the quest belongs to.
        quest_steps (int): The number of keys and locks in the quest.
        quest_radius (int): Total distance needed to travel for the quest.
        fitness (int): The fitness of the quest.
    """
    
    def __init__(self, map, max_steps=5):

        self.map = map
        self.challange_type = [np.random.choice(["dex", "str", "con", "int", "wis", "cha"]) for i in range(2)]

        #self.dif = difficulty
        #self.radius = random.randint(1, map.size)


        self.steps = random.randint(1,max_steps)
        self.lock_coords = []
        self.key_coords =  []

        for i in range(self.steps):
            if i == 0:
                add_key = [[round(random.uniform(0, map.size-1),1) for i in range(2)] for i in range(random.randint(1, 3))]
                add_lock = []

            elif i == self.steps-1:
                add_key = [[round(random.uniform(0, map.size-1),1) for i in range(2)]]
                add_lock = [[round(random.uniform(0, map.size-1),1) for i in range(2)] for i in range(random.randint(1, 3))]
            
            else:
                add_key = [[round(random.uniform(0, map.size-1),1) for i in range(2)]]
                add_lock = [[round(random.uniform(0, map.size-1),1) for i in range(2)]]

            self.key_coords.append(add_key)
            self.lock_coords.append(add_lock)

        self.arc = np.random.choice(view_noises["story_arc"]["atr_list"])
        self.fitness = self.check_fitness()

    def check_fitness(self):
        self.fitness = 0
        return self.fitness

    def check_difficulty(self):
        self.difficulty = 0
        return self.difficulty

    def check_radius(self):
        pass


    def __repr__(self):
        return f"{self.arc} {self.steps}"