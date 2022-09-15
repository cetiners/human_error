import random
import time
import pickle
from unittest.mock import seal
from map_manager.map_attributer import *
from genetic_algorithm.crossover import *
from genetic_algorithm.mutation import *
from genetic_algorithm.selection  import *


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

        self.coord = [round(random.uniform(0, size-1),1) for i in range(2)]
        self.check_coor = [int(i) for i in self.coord]
        self.map = map
        self.encounter_type = encounter_type
        self.type = type
        self.size = size
        self.fitness = self.check_fitness()

    def check_fitness(self):
        
        self.check_coor = [int(i) for i in self.coord]
        fitness = 0

        # Reverse check the key to see the name of the biome

        active_biome = view_noises["terrain"]["atr_list"][(int(self.map.views["terrain"][self.check_coor[0], self.check_coor[1]])-1)]

        supposed_biome = [i for i in encounter_biomes[self.encounter_type] if self.type in encounter_biomes[self.encounter_type][i]][0]

        # Discourage from placing in the sea and check the biome of the encounter.

        if (int(self.map.views["terrain"][self.check_coor[0], self.check_coor[1]])) == 0:
            
            fitness -= 5000

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

        civ = self.map.views["civilisation"][self.check_coor[0],self.check_coor[1]]
        
        if (civ == 1) | (civ == 5):
#
            fitness -= 5000


        # check if the biome is correct

        if active_biome != supposed_biome:

            fitness -= 1000
        #
        #if type not in biomes[biome]:
#
        #    fitness -= 10
#
        #self.fitness = fitness

        return fitness


class pack:

    """
        Creates a set or a "pack" of w_encounter individuals, returns a list of individuals within
        the pack and their individual fitnesses
    """

    def __init__(self,map,type="",size=25,encounter_type=""):

        self.pack = []
        self.size = size
        
        for _ in range(size):
            ind = w_encounter(map=map,type=type,encounter_type=encounter_type)
            self.pack.append(ind)

        self.pack_coord =  [ind.coord for ind in self.pack]
        self.pack_fitness = sum(i for i in [ind.check_fitness() for ind in self.pack])


    def update_pack_fitness(self):
        self.pack_fitness = sum(i for i in [ind.check_fitness() for ind in self.pack])

        return self.pack_fitness

    def update_pack_coord(self):
        self.pack_coord =  [ind.coord for ind in self.pack]

        return self.pack_coord

class pack_population:

    """
        Population of pack of world encounters containing individuals.
    """

    def __init__(self, map, pop_size,pack_size, type="", encounter_type = ""):
        
        self.population = []
        self.gen = 1
        self.map = map
        self.timestamp = int(time.time())
        self.size = pop_size
        self.best_ind = ""
        self.pack_size = pack_size
        self.type = type
        self.encounter_type = encounter_type

        for _ in range(pop_size):

            self.population.append(pack(map,type,pack_size,encounter_type))

    def evolve(self,gens,mu_p=0.01,mutation="inversion",test=False,save=False):

        for gen in range(1,gens+1):
            
            new_pop = []

            print('\nGen', self.gen, 'evolving:')
            
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

                offspring1, offspring2 = ax_pmx(parent1, parent2)

                if test:
                    return offspring1,offspring2
                    
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
                
            best_individual = max(self.population, key=operator.attrgetter('pack_fitness'))

            self.best_ind = best_individual

            print(f'Best Individual: {best_individual.pack_fitness}')

            if save:
                picklefile = open(f'{self.timestamp}', 'wb')
                pickle.dump(self, picklefile)
                picklefile.close()
      
            self.gen += 1

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


