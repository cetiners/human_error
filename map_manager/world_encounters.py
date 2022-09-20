import random
import time
import numpy as np
from map_manager.map_attributer import *
from genetic_algorithm.crossover import *
from genetic_algorithm.mutation import *
from genetic_algorithm.selection  import *
from tools.utils import encounter_biomes, required_n_enc

    

class w_encounter:

    """
        Handles placements for the world encounters, given the map. Checks the appropriate map placements 
        considering biomes, danger level and civilisation to calculate the appropriate fitness.
    """

    def __init__(self,map,encounter_type="", type="", size=1024):

        self.coord = [round(random.uniform(0, size-1),1) for i in range(2)]
        self.encounter_type = encounter_type
        self.type = type

        self.check_coor = [int(i) for i in self.coord]
        self.map = map
        self.size = size
        self.fitness = self.check_fitness()

    def check_fitness(self):
        
        self.check_coor = [int(i) for i in self.coord]
        active_biome =  view_noises["terrain"]["atr_list"][(int(self.map.views["terrain"][self.check_coor[0], self.check_coor[1]])-1)]
        
        fitness = 0

        # Reverse check the key to see the name of the biome

        active_biome = view_noises["terrain"]["atr_list"][(int(self.map.views["terrain"][self.check_coor[0], self.check_coor[1]])-1)]

        for i in encounter_biomes[self.encounter_type]:
            if self.type in encounter_biomes[self.encounter_type][i]:
                supposed_biome = i 

        # Discourage from placing in the sea and check the biome of the encounter.

        if (int(self.map.views["terrain"][self.check_coor[0], self.check_coor[1]])) == 0:
            
            fitness -= 1000

        # Add the distance to the nearest biome centroid to the mix. Closer to the biome centroid, better the fitness.

        else:
            min_distance = 99999

            for centroid in self.map.atr_centroids[supposed_biome]:

                x2 = (self.check_coor[0]-centroid[0])**2
                y2 = (self.check_coor[1]-centroid[1])**2
                dist = np.sqrt((x2+y2))
    
                if dist < min_distance:
                    min_distance = dist

            fitness -= min_distance

        # if location is in the developed regions punish the algorithm

        civ = self.map.views["civilisation"][self.check_coor[0],self.check_coor[1]]-1
        
        if (civ == 2):
            fitness -= 1000

        # check if the biome is correct
        if active_biome != supposed_biome:
            fitness -= 1000


        # check threat levels
        thr = self.map.views["threat"][self.check_coor[0],self.check_coor[1]]-1
        if self.encounter_type == "friendly_animals":

            if thr < 3:
                fitness -= 1000

        elif self.encounter_type == "hostile_animals":

            if thr > 2:
                fitness -= 1000 

        self.fitness = fitness
        return fitness


class pack:

    """
        Creates a set or a "pack" of w_encounter individuals, returns a list of individuals within
        the pack and their individual fitnesses
    """

    def __init__(self,map,encounter_type="",type="",size=25):

        self.pack = []
        self.size = size
        self.map = map

        self.encounter_type = encounter_type
        self.type = type

        for _ in range(size):
            ind = w_encounter(map=map,encounter_type=self.encounter_type,type=self.type)
            self.pack.append(ind)

        self.pack_coord =  self.update_pack_coord()
        self.pack_fitness = self.update_pack_fitness()

    def update_pack_fitness(self):

        pack_fitness = 0

        for ind_s in self.pack:
            if ind_s.check_fitness() > -1000:
                pack_fitness += 1

        self.pack_fitness = pack_fitness
        return pack_fitness

    def update_pack_coord(self):
        self.pack_coord =  [ind.coord for ind in self.pack]
        self.check_coor = [ind.check_coor for ind in self.pack]
        return self.pack_coord

class pack_population:

    """
        Population of pack of world encounters containing individuals.
    """

    def __init__(self, map, pop_size,pack_size,type,world_atlas,yellow_pages):
        
        self.population = []
        self.gen = 1
        self.map = map
        self.timestamp = int(time.time())
        self.size = pop_size
        self.best_inds = ""
        self.pack_size = pack_size
        self.type = type

        self.world_atlas = world_atlas
        self.yellow_pages = yellow_pages

        for i in encounter_biomes:
            for j in encounter_biomes[i]:
                if self.type in encounter_biomes[i][j]:
                    self.encounter_type = i


        for _ in range(self.size):
            self.population.append(pack(map,type=self.type,size = self.pack_size,encounter_type = self.encounter_type))


    def evolve(self,gens=50, mu_p=0.01,crossover="ax_pmx",mutation="inversion", early_stop=False):

        satisfied = False

        added = 0 
        
        while not satisfied:

            new_pop = []
            
            while len(new_pop) < self.size:

                used_parents = []

                suitable = False

                # Check if parents are eligible and used.
                while not suitable:
                    
                    parent1,parent2 = rank_selection(self)

                    if (parent1 in used_parents):

                        suitable = False

                    elif (parent2 in used_parents):

                        suitable = False

                    else:
                        suitable = True
                        used_parents.append(parent1)
                        used_parents.append(parent2)
                
                # to assess if things are going well:
                
                # Crossover
                if crossover == "ax_pmx":

                    offspring1, offspring2 = ax_pmx(parent1, parent2)

                elif crossover == "pmx":

                    offspring1, offspring2 = pmx(parent1, parent2)

                elif crossover == "ar_xo":

                    offspring1, offspring2 = ar_xo(parent1, parent2)
                
                elif crossover == "ax_ar_xo":
                    
                    offspring1, offspring2 = ax_ar_xo(parent1,parent2)

                    
                # Mutation
                if mutation == "complete":

                    if random.random() < mu_p:
                        offspring1 = complete_mutation(offspring1)

                    if random.random() < mu_p:
                        offspring2 = complete_mutation(offspring2)

                elif mutation == "inversion":

                    if random.random() < mu_p:
                        offspring1 = inversion_mutation(offspring1)

                    if random.random() < mu_p:
                        offspring2 = inversion_mutation(offspring2)


                offspring1.update_pack_fitness()
                offspring2.update_pack_fitness()

                offspring1.update_pack_coord()
                offspring2.update_pack_coord()

                new_pop.append(offspring1)

                if len(new_pop) < self.size:

                    new_pop.append(offspring2)

            self.population = new_pop

            n_ind = required_n_enc[self.type]

            final_list = self.yellow_pages
            final_coords = self.world_atlas

#            added = 0
#
#            while added < n_ind:
#
#                if self.gen % 1 == 0:
#
#                    for pack_b in new_pop:
#                        
#                        while added < n_ind:
#
#                            for ind_b in pack_b.pack:
#                                print("checking for new individuals")
#
#                                if ind_b.fitness > -1000:
#
#                                    if ind_b.check_coor not in self.world_atlas:
#                                        print("Found one!")
#                                        self.yellow_pages.append(ind_b)
#                                        self.world_atlas.append(ind_b.check_coor)
#                                        added += 1
#                                        if added == n_ind:
#                                            break
#                                        
#                            if added == n_ind:
#                                    break
            
#                                    

            if self.gen % 1 == 0:
                for pack_b in self.population:
                    for ind_b in pack_b.pack:
                        if ind_b.fitness > -1000:
                            if ind_b.check_coor not in final_coords:
                                final_list.append(ind_b)
                                final_coords.append(ind_b.check_coor)
                                added += 1
                            if added == n_ind:
                                break
                    
                    if added == n_ind:
                        break

            print(f'Gen {self.gen}, found individuals: {added}')

            self.world_atlas = final_coords
            self.yellow_pages = final_list




            if added < n_ind:

                satisfied = False
            
            elif added == n_ind:
                print(f'Found required individuals: {added}, on generation {self.gen}')
                satisfied = True
                break

            if early_stop:
                if self.gen == gens:
                    satisfied = True

            self.gen += 1


class w_encounter_manager:
    
    """
    Generates all the required world encounters through the genetic operators.
    """

    def __init__(self,map,list_of_encounters):

        self.encounters = list_of_encounters
        self.coordinates = []
        self.individuals = []
        self.map = map

    def let_there_be_light(self):

        for encounter in self.encounters:

            print(f"\nGenerating {encounter} encounters, {required_n_enc[encounter]} required.")

            pop = pack_population(self.map,pop_size=100,pack_size=100,type=encounter,world_atlas=self.coordinates,yellow_pages=self.individuals)
            pop.evolve(mu_p=0.22,mutation="complete",crossover="ax_pmx")

            self.coordinates.append(pop.world_atlas)
            self.individuals.append(pop.yellow_pages)

            del(pop)

    
      

#    def log(self):
#        
#        '''
#        To register the evolution process - a csv is saved with the following info for each pack:
#        
#        Generation | Type | Individual Fitness | Individual Coordinates
#            
#        This will be useful for report analysis of results
#        
#        '''
#        
#        with open(f'run_{self.timestamp}.csv', 'a', newline='') as file:
#            writer = csv.writer(file)
#            for i in self:
#               writer.writerow([self.gen, i., i.fitness, i.score])

    #def __len__(self):
    #    return len(self.individuals)
#
    #def __getitem__(self, position):
    #    return self.individuals[position]
#
    #def __repr__(self):
#        return f"Population(size={len(self.individuals)})"


