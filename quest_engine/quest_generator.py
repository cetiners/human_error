import random
import numpy as np
from tools.utils import basic_distance, freytags
from map_engine.map_attributer import view_noises
from quest_engine.quest_ga.selection import *
from quest_engine.quest_ga.crossover import *
from quest_engine.quest_ga.mutation import *


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
    
    def __init__(self, map,act, steps=5):
        
        self.map = map
        self.challange_type = [np.random.choice(["dex", "str", "con", "int", "wis", "cha"]) for i in range(2)]     
        self.act = act   

        self.steps = steps
        self.path = []
        self.is_npc = [random.getrandbits(1) for i in range(self.steps-1)]
        self.is_npc.append(1)

        for _ in range(self.steps):

            self.path.append([round(random.uniform(0, map.size-1),1) for i in range(2)])

        # Chance to finish the quest at the quest giver.
        
        if random.random() < 0.40:
                self.path[-1] = self.path[0]

        self.point_distances()
        self.difficulty = self.check_difficulty()
        self.path_act = self.act_check()
        self.fitness = self.check_fitness()
        


    def check_fitness(self):

        fitness = 0 

        ## Total distance and individual distances.

        fitness -= self.dist_dict["total"]

        for idx, location in enumerate(self.path):
            if idx == 0:
        ## Punish the quest giver depending on how far they are from a nearest civilisation & if it is in the sea.
                if (int(self.map.views["civilisation"][int(location[0]),int(location[1])])) < 2:
                    fitness -= 1000

                else:
                    for centroid in self.map.atr_centroids["city"]:
                        min_dist = 9999999
                        dist = basic_distance(location, centroid)
                        if dist < min_dist:
                            min_dist = dist
                    fitness -= min_dist
        
        ## If quest key/locks are in sea, punish the fitness substantially.

            if (int(self.map.views["terrain"][int(location[0]),int(location[1])]))  == 0:

                fitness -= 1000

        ## Check the story act that the quest points belong to, if they are not as specified, punish the fitness.

            if self.path_act[idx] != self.act:
                fitness -= 1000


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
            act = view_noises["story_act"]["atr_list"][(int(self.map.views["story_act"][i[0], i[1]])-1)]
            path_act.append(int(act[-1]))

        self.path_act = path_act

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

        if len(distances) == 0:
            self.dist_dict["individual"] = [0]

    def update(self):
        self.point_distances()
        self.check_difficulty()
        self.act_check()
        self.check_fitness()

class quest_pop:

    def __init__(self,map,act, pop_size = 20,steps=5):

        self.theme = [np.random.choice(["dex", "str", "con", "int", "wis", "cha"]) for i in range(2)]
        self.population = []
        self.map = map
        self.size = pop_size
        self.steps = steps

        for _ in range(self.size):
            self.population.append(quest(self.map,act=act,steps=self.steps))



    def evolve(self, early_stop = False, gens=100, mu_p = 0.1, mutation="point",xo = "single_point", print_it=False):

        save_dict = []
        
        gen = 0
        satisfied = False

        while not satisfied:
            new_pop = []
            while len(new_pop) < self.size:
                used_parents = []
                suitable = False
                while not suitable:
                    parent1, parent2 = q_rank_selection(self)
                    if parent1 in used_parents:
                        suitable = False
                    elif parent2 in used_parents:
                        suitable = False
                    else:
                        suitable = True
                        used_parents.append(parent1)
                        used_parents.append(parent2)
                if xo == "pmx":
                    offspring1, offspring2 = q_ax_pmx(parent1, parent2)
                if xo == "single_point":
                    offspring1, offspring2 = q_sp_xo(parent1, parent2)
                if mutation == "point":
                    if random.random() < mu_p:
                        offspring1 = q_point_mutation(offspring1)
                    if random.random() < mu_p:
                        offspring2 = q_point_mutation(offspring2)
                if mutation == "complete":
                    if random.random() < mu_p:
                        offspring1 = q_complete_mutation(offspring1)
                    if random.random() < mu_p:
                        offspring2 = q_complete_mutation(offspring2)
                new_pop.append(offspring1)
                offspring1.update()
                offspring2.update()
                if len(new_pop) < self.size:    
                    new_pop.append(offspring2)
            self.population = new_pop
            gen += 1
            best_ind =  sorted(self.population, key=operator.attrgetter('fitness'))[-1]
            save_dict.append(best_ind.fitness)
            if print_it:
                print(f"Best ind in gen {gen} is {best_ind.fitness}")
            if best_ind.fitness > -500:
                satisfied = True
                print(f"Found the required fitness on gen {gen} with fitness {best_ind.fitness}")
                break
            if early_stop:
                if gen == gens:
                    satisfied = True
                    break
        return save_dict