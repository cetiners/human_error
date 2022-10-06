import random
import time
import numpy as np
from map_engine.map_attributer import *
from map_engine.map_ga.crossover import *
from map_engine.map_ga.mutation import *
from map_engine.map_ga.selection  import *
    

class w_encounter:

    """
        Handles placements for the world encounters, given the map. Checks the appropriate map placements 
        considering biomes, danger level and civilisation to calculate the appropriate fitness.
        
        Attributes:
            map (map): The map object to be used for the encounter placement.
            encounter_type (str): The type of encounter to be placed. Can be "friendly_animals", "hostile_animals", "natural_encounters" or "special_encounters".
            type (str): The type of the encounter.
            size (int): The size of the map.
            check_coor (list): The coordinates of the encounter in integer form.
            fitness (int): The fitness of the encounter.
            coord (list): The coordinates of the encounter in float form.

        Methods:
            check_fitness: Checks the fitness of the encounter.
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

        if (civ == 1):
            fitness -= 500

        # check if the biome is correct
        if active_biome != supposed_biome:
            fitness -= 1000


        # check threat levels
        thr = int(self.map.views["threat"][self.check_coor[0],self.check_coor[1]])-1

        if self.encounter_type == "friendly_animals":

            if thr > 7:
                fitness -= 1000

        elif self.encounter_type == "hostile_animals":

            if thr < 3:
                fitness -= 1000 

        self.fitness = fitness
        return fitness

class pack:

    """
        Creates a set or a "pack" of w_encounter individuals, returns a list of individuals within
        the pack and their individual fitnesses

        Args:
            map (map): The map object to be used for the encounter placement.
            encounter_type (str): The type of encounter to be placed. Can be "friendly_animals", "hostile_animals", "natural_encounters" or "special_encounters".
            type (str): The type of the encounter.
            size (int): The size of the map.

        Methods:
            update_pack_fitness: Updates the fitness of the pack.
            update_pack_coord: Updates the coordinates of the pack.

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

        average_fitness = sum([ind.check_fitness() for ind in self.pack])/self.size

        self.pack_fitness = average_fitness
        return average_fitness

    def update_pack_coord(self):
        self.pack_coord =  [ind.coord for ind in self.pack]
        self.check_coor = [ind.check_coor for ind in self.pack]
        return self.pack_coord

    def __repr__(self):
        return f"pack of {self.size} individuals"
    def __str__(self):
        return f"pack of {self.size} individuals"

class pack_population:

    """
        Population of pack of world encounters containing individuals.

        Args:
            map (map): The map object to be used for the encounter placement.
            encounter_type (str): The type of encounter to be placed. Can be "friendly_animals", "hostile_animals", "natural_encounters" or "special_encounters".
            type (str): The type of the encounter.
            size (int): The size of the map.
            pop_size (int): The size of the population.

        Methods:
            evolve: Evolves the population coordinates using genetic operators.
                gens (int): The number of generations to evolve the population.
                mu_p (float): The probability of mutation.
                crossover (str): The crossover operator to be used. Can be "ax_pmx", "pmx", "ar_xo" or "ax_ar_xo".
                mutation (str): The mutation operator to be used. Can be "complete" or "inversion".
                early_stop (bool): If True, the evolution will stop after the number of generations specified in gens.
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

            for pack_b in self.population:
                for ind_b in pack_b.pack:
                    if ind_b.fitness > -1000:
                        if ind_b.coord not in self.world_atlas:
                            self.yellow_pages.append(ind_b)
                            self.world_atlas.append(ind_b.coord)
                            added += 1
                            if added == n_ind:
                                satisfied = True
                                break

                if satisfied:
                    break

            print(f'Gen {self.gen}, found individuals: {added}')
            
            if added == n_ind:
                print(f'Found required individuals: {added}, on generation {self.gen}')
                satisfied = True
                break

            if early_stop:
                if self.gen == gens:
                    satisfied = True

            self.gen += 1
        
        def __repr__(self):
            return f'Population of {self.size} individuals, generation {self.gen}'

        def __len__(self):
            return self.size


class w_encounter_manager:
    
    """
    Generates all the required world encounters through the genetic operators.

    Args:
        map (map): The map object to be used for the encounter placement.
        pop_size (int): The size of the population.
        gens (int): The number of generations to evolve the population.
        mu_p (float): The probability of mutation.
        crossover (str): The crossover operator to be used. Can be "ax_pmx", "pmx", "ar_xo" or "ax_ar_xo".
        mutation (str): The mutation operator to be used. Can be "complete" or "inversion".
        early_stop (bool): If True, the evolution will stop after the number of generations specified in gens.

    Methods:
        let_there_be_light: Evolves the population coordinates using genetic operators.

    """

    def __init__(self,map,list_of_encounters):

        self.encounters = list_of_encounters
        self.coordinates = []
        self.individuals = []
        self.map = map

    def let_there_be_light(self, pop_size=10, pack_size=10):

        for encounter in self.encounters:

            print(f"\nGenerating {encounter} encounters, {required_n_enc[encounter]} required.")

            pop = pack_population(self.map,pop_size=pop_size,pack_size=pack_size,type=encounter,world_atlas=self.coordinates,yellow_pages=self.individuals)
            pop.evolve(mu_p=0.22,mutation="complete",crossover="ax_pmx")

            self.individuals == pop.yellow_pages
            self.coordinates == [i.coord for i in pop.yellow_pages]

            print("\n Total found individuals: ",len(self.individuals))


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