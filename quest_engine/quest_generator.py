import random
import numpy as np
from tools.utils import basic_distance
from quest_engine.freytags_fitness import freytags
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
        
        if random.random() < 0.50:
                self.path[-1] = self.path[0]

        self.point_distances()
        self.difficulty = self.check_difficulty()
        self.path_act = self.act_check()
        self.fitness = self.check_fitness()
        self.path_threat = self.check_threat()

    def check_fitness(self):
        
        fitnesses = []
         
        ## Total distance and individual distances.

        # fitness -= self.dist_dict["total"]

        for idx, location in enumerate(self.path):
            fitness = 0
            if idx == 0:
        ## Punish the quest giver depending on how far they are from a nearest civilisation & if it is in the sea.
                if view_noises["civilisation"]["atr_list"][(int(self.map.views["civilisation"][int(location[0]), int(location[1])])-1)] == "Wild":
                    fitness -= 1000
                #else:
                #    for centroid in self.map.atr_centroids["city"]:
                #        min_dist = 9999999
                #        dist = basic_distance(location, centroid)
                #        if dist < min_dist:
                #            min_dist = dist
                #    fitness -= min_dist
        
        ## If quest key/locks are in sea, punish the fitness substantially.

            if (int(self.map.views["terrain"][int(location[0]),int(location[1])])) == 0:
                fitness -= 1000

        ## Check the story act that the quest points belong to, if they are not as specified, punish the fitness.

            if max(self.path_act,key=self.path_act.count) != self.act:
                fitness -= 1000

            if max(self.path_act) > self.act:
                fitness -= 1000

            fitnesses.append(fitness)


        ## Check the quest progression for threat, if it does not fit the Freytag's Pyramid, punish the fitness.
        if self.steps != 1:
            freytags_fitnesses = freytags(self.check_threat())
            fitnesses = [i + j for (i, j) in zip(fitnesses, freytags_fitnesses)]

        if self.steps == 1:
            freytags_fitnesses = [0]
            fitnesses = [0]
        

        self.fitnesses = fitnesses
        self.fitness = sum(fitnesses)
        self.freytags_fitnesses = freytags_fitnesses
        self.suitable_fitness = sum([i>-1000 for i in self.fitnesses])
        self.act_fitness = sum([i == self.act for i in self.path_act])

        return self.fitness

    def check_threat(self):
        path_threat = []

        for i in self.path:
            threat_level = view_noises["threat"]["atr_list"][(int(self.map.views["threat"][int(i[0]), int(i[1])])-1)]
            path_threat.append(int(threat_level))

        return path_threat
        
    def act_check(self):

        path_act = []

        for i in self.path:
            act = view_noises["story_act"]["atr_list"][(int(self.map.views["story_act"][int(i[0]), int(i[1])])-1)]
            path_act.append(act)

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

        self.total_dist = sum(distances)
        self.ind_dist = distances

        if len(distances) == 0:
            self.ind_dist = distances = [0]

    def update(self):

        self.point_distances()
        self.check_threat()
        self.check_difficulty()
        self.act_check()
        self.check_fitness()

    def summary(self):
        print("Quest type: ", self.challange_type)
        print("Quest difficulty: ", self.difficulty)
        print("Quest act: ", self.act)
        print("Quest steps: ", self.steps)
        print("Quest total distance: ", self.total_dist)
        print("Quest fitness: ", self.fitness)
        print("Quest freytags fitness: ", self.freytags_fitnesses)
        print("Quest fitnesses: ", self.suitable_fitness)
        print("Quest path: ", self.path)
        print("Quest path threat: ", self.path_threat)
        print("Quest path act: ", self.path_act)


        

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

        if self.steps == 1:
            satisfied = True

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

                    if parent1 != parent2:
                        suitable = True

                if xo == "pmx":
                    offspring1, offspring2 = q_ax_pmx(parent1, parent2)
                if xo == "single_point":
                    offspring1, offspring2 = q_sp_xo(parent1, parent2)
                if xo == "ar":
                    offspring1, offspring2 = q_ar_xo(parent1, parent2)

                if mutation == "single_point":
                    if random.random() < mu_p:
                        offspring1 = q_point_mutation(offspring1)
                    if random.random() < mu_p:
                        offspring2 = q_point_mutation(offspring2)

                if mutation == "complete":
                    if random.random() < mu_p:
                        offspring1 = q_complete_mutation(offspring1)
                    if random.random() < mu_p:
                        offspring2 = q_complete_mutation(offspring2)

                if mutation == "random_point":
                    if random.random() < mu_p:
                        offspring1 = q_random_point_mutation(offspring1)
                    if random.random() < mu_p:
                        offspring2 = q_random_point_mutation(offspring2)    

                offspring1.update()
                offspring2.update()

                new_pop.append(offspring1)

                if len(new_pop) < self.size:    
                    new_pop.append(offspring2)

            self.population = new_pop

            ## Save good individuals to a dictionary.
            #if save_inds:
            #    for i in self.population:
            #        if i.fitness > -600:
            #            if len(library) == library_size:
            #                satisfied = True
            #                print(f"Found the required individuals on gen {gen}")
            #                break
            #            else:
            #                library.append(i)
            #                print(f"Total found so far: {len(library)}")


            gen += 1
            
            best_ind =  sorted(self.population, key=operator.attrgetter('fitness'))[-1]
            self.best_ind = best_ind

            save_dict.append(best_ind.fitness)

            if print_it:
                print(f"Best ind in gen {gen} is {best_ind.fitness}")

            if early_stop:
                if gen == gens:
                    satisfied = True
                    break

            else:
                if best_ind.fitness > -1000:
                    satisfied = True
                    print(f"Found the required individual on gen {gen}")
                    break

        return best_ind


class quest_library:

    def __init__(self, map,params, shelf_size=50):

        for key, value in params.items():
            setattr(self, key, value)

        self.library = []
        self.map = map
        self.shelf_size = shelf_size
        
        
        for act in [0,1,2]:
            for steps in [3,4,5]:        
                for _ in range(self.shelf_size):
                    pop = quest_pop(self.map,act=act, pop_size=self.pop_size, steps=steps)
                    print(act,steps)
                    ind = pop.evolve(gens=self.gens,early_stop=False, mu_p=self.mu_p, xo=self.xo, mutation=self.mutation,print_it=self.print_it)
                    self.library.append(ind)


        def browse(self, number_of_quests=1, act=0, challange_type="dex",steps=3):
            output = []

            while len(output) < number_of_quests:
                q = random.select(self.library)
                if q.act == act and q.challange_type == challange_type and q.steps == steps and q not in output:
                    output.append(q)

            return output

        def curate(self):
            pass

