import random
import time
import csv
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

        self.coord = [round(random.uniform(0, size),1) for i in range(2)]
        self.check_coor = [int(i) for i in self.coord]
        self.map = map
        self.encounter_type = encounter_type
        self.type = type
        self.size = size
        self.fitness = self.check_fitness()

    def check_fitness(self):
        
        self.check_coor = [int(i) for i in self.coord]
        fitness = 0
        
        civ = self.map.views["civilisation"][self.check_coor[0],self.check_coor[1]]

        biome = view_noises["terrain"]["atr_list"][(int(self.map.views["terrain"][self.check_coor[0], self.check_coor[1]]))]
        
        if (civ == 0) | (civ != 4):

            fitness -= 1000

        biomes = encounter_biomes[self.encounter_type]
        
        if type not in biomes[biome]:

            fitness -= 1000

        self.fitness = fitness

        return fitness


class pack:

    """
        Creates a set or a "pack" of w_encounter individuals, returns a list of individuals within
        the pack and their individual fitnesses
    """

    def __init__(self,map,type="",size=25,encounter_type=""):

        self.pack = []
        
        for _ in range(size):
            ind = w_encounter(map=map,type=type,encounter_type=encounter_type)
            self.pack.append(ind)

        self.pack_coord =  [ind.coord for ind in self.pack]
        self.pack_fitness = sum(i for i in [ind.check_fitness() for ind in self.pack] if i < 0)


    def update_pack_fitness(self):
        self.pack_fitness = sum(i for i in [ind.check_fitness() for ind in self.pack] if i < 0)

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
        self.timestamp = int(time.time())

        for _ in range(pop_size):

            self.population.append(pack(map,type,pack_size,encounter_type))

    def evolve(self,gens):

        for gen in range(1,gens+1):
            
            new_pop = []
            print('\nGen', self.gen, 'evolving:')
            
            while len(new_pop) < self.size:
                
                different=False
                
                # checking if they are different parents
                while different==False:

                    if sel_type==1:
                        parent1, parent2 = fps(self), fps(self)
                    
                    parent1, parent2 = select(self), select(self)

                    if (parent1.get_model_weights()[0]==parent2.get_model_weights()[0]).all()==False:
                         # if there are differences on the first matrix then they're different (lighter check)
                        different=True
                
                
                # to assess if things are going well:
                print('Parent1:', parent1)
                print('Parent2:', parent2,'\n')
                
                # Crossover
                
                # Since our crossover functions are implemented to work with the weight arrays of matrixes, we call for each parent the
#                # get_model_weights method - so we can extract the weights without the bias values
#                
#                
#                
#                if random.random() < co_p:
#                    offspring1, offspring2 = crossover(parent1.get_model_weights(), parent2.get_model_weights()) 
#                else:
#                    offspring1, offspring2 = parent1.get_model_weights(), parent2.get_model_weights()
#                    
#                # Mutation
#                if random.random() < mu_p:
#                    offspring1 = mutate(offspring1)
#                if random.random() < mu_p:
#                    offspring2 = mutate(offspring2)
# 
#                new_pop.append(Individual(units = self.indiv_units, weights = offspring1))
#                
#                if len(new_pop) < self.size:
#                    new_pop.append(Individual(units = self.indiv_units, weights = offspring2))
# 
#            if elitism == True:
#                if self.optim == "max":
#                    least = min(new_pop, key=attrgetter("fitness"))
#                elif self.optim == "min":
#                    least = max(new_pop, key=attrgetter("fitness"))
#                    
#                new_pop.pop(new_pop.index(least))
#                new_pop.append(elite)
#
#            self.log()
#            self.individuals = new_pop
#
#            if self.optim == "max":
#                
#                best_individual = max(self, key=attrgetter("fitness"))
#
#                print(f'Best Individual: {best_individual}')
#                
#            elif self.optim == "min":
#                
#                best_individual = min(self, key=attrgetter("fitness"))
#                
#                print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')            
            self.gen += 1
        pass

    def log(self):
        
        '''
        To register the evolution process - a csv is saved with the following info for each pack:
        
        Generation | Type | Individual Fitness | Individual Coordinates
            
        This will be useful for report analysis of results
        
        '''
        
        with open(f'run_{self.timestamp}.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for i in self:
#                writer.writerow([self.gen, i.units, i.fitness, i.score])

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)})"


