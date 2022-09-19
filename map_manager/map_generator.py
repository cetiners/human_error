import numpy as np
import matplotlib.pyplot as plt
from pmdarima import c
from skimage.draw import polygon as ployg
from character_engine.player_character import npc
from scipy.spatial import Voronoi, voronoi_plot_2d,  cKDTree
from map_manager.map_attributer import average_cells, fill_cells, histeq, view_noises
from map_manager.lloyd_relaxation import relax, voronoi
from map_manager.noise import blurry_lines, toddler
from tools.utils import map_attribute_checker
import matplotlib.pyplot as plt
import matplotlib.colors
import random
import json



class map:

    def __init__(self, name="Map", size=1024):
        self.name = name
        self.size = size
        self.seed = 7611072

        # Initialize map with an array of zeros.
        self.coord = np.zeros((self.size,self.size),dtype="int")

        self.location_coordinates = {}
        self.location_events = {}
        self.views = {}
        self.vors = {}
        self.centroids = {}
        self.interactions = {}
         

    def place_character(self):

        # Return random a random coordinate

        return [random.uniform(0.1,float(self.size)) for i in range(2)]

    def populate_map(self, n_locations=512, name="Regions", blurred=True, is_event=False, relaxed=True,k=10, attribute_centroids=True):

        # Place centroids to be used as region centres.
        centroids = np.random.randint(0,self.size, (n_locations+2, 2))

        # Generate Voronoi regions (All points closer to one specific centroid is in a region.)

        if relaxed:

            centroids = relax(centroids,self.size,k=10)

        self.centroids[name] = centroids


        self.atr_centroids = {}

        edge_points = self.size*np.array([[-1, -1], [-1, 2], [2, -1], [2, 2]])

        new_centroids = np.vstack([centroids, edge_points])

        vor = Voronoi(new_centroids)

    # Calculate Voronoi map

        vor_map = np.zeros((self.size, self.size), dtype=np.uint32)

        for i, region in enumerate(vor.regions):
            # Skip empty regions and infinte ridge regions
            if len(region) == 0 or -1 in region: continue
            # Get polygon vertices    
            x, y = np.array([vor.vertices[i][::-1] for i in region]).T
            # Get pixels inside polygon
            rr, cc = ployg(x, y)
            # Remove pixels out of image bounds
            in_box = np.where((0 <= rr) & (rr < self.size) & (0 <= cc) & (cc < self.size))
            rr, cc = rr[in_box], cc[in_box]
            # Paint image
            vor_map[rr, cc] = i
        
        if blurred:
            self.views[name] = blurry_lines(vor_map)
            
        else:
            self.views[name] = vor_map

        self.vors[name] = vor
        self.location_coordinates[name] = vor.points
        self.location_events[name] = is_event
        
        return self.views[name]

    def attribute_view(self,double=True,seed_1=20,seed_2=30,attr_names=[],alpha=0.33, map_name="", view_name=""):

        size = self.size

        map_1 = toddler(size, 2, seed_1)
        uniform_map_1 = histeq(map_1, alpha=alpha)
        cells_1 = average_cells(self.views[map_name], uniform_map_1)
        map_1 = fill_cells(self.views[map_name], cells_1)
        map_1_range = [np.amax(map_1),np.amin(map_1)]

        if double:

            map_2 = toddler(size, 2, seed_2)
            uniform_map_2 = histeq(map_2, alpha=alpha)
            cells_2 = average_cells(self.views[map_name], uniform_map_2)
            map_2 = fill_cells(self.views[map_name], cells_2)
            map_2_range = [np.amax(map_2),np.amin(map_2)]

        else:
            map_2 = " "
            map_2_range = " "

        attributed_map = map_attribute_checker(map_1, map_2, map_1_range, map_2_range,map_name=map_name, double=double)
        self.views[view_name] = attributed_map

        return attributed_map


    def land_mask(self):
        
        seed=random.randint(1,100)
        res=2
        octaves = 15
        persistence = 0.60
        lacunarity = 2
        mask = toddler(size=1024, seed=seed,res=res, octaves = octaves, persistence = persistence, lacunarity = lacunarity,mask=True)

        for view in self.views:
            self.views[view] += 1
            self.views[view] *= mask
    
    def event_starter(self, event, player):

        if event == "ambush":
            goblin = npc("Dark figure",self,xp=20,p_health=15)
            player.battle(goblin, "Demo fight")


    def check_region(self,coordinates):
        
        points = self.vor.points
        voronoi_kdtree = cKDTree(points)
        dst, regions = voronoi_kdtree.query(coordinates)
        
        return regions

    def attribute_centroids(self,name):

        for i in view_noises[name]["atr_list"]:
            
            self.atr_centroids[i] = []

        # Check the centroids and assign them to a dictionary to later use in fitness function
        
        for i in self.centroids[name]:

            coord = [int(j) for j in i]

            if coord[0] < self.size:

                if coord[1] < self.size:
                    
                    biome = view_noises[name]["atr_list"][(int(self.views[name][coord[0], coord[1]]))]

                    self.atr_centroids[biome].append([coord[0],coord[1]])

        return print("Centroids attributed, attributes centroited")
        
    

    #def create_regions(self, name, potential_regions,region_weights=[]):
#
    #    if potential_regions == []:
    #    
    #        region_weights = [(1/len(potential_regions)) for i in range(len(potential_regions))]
    #    
    #    types = {}
    #    
    #    for i in range(0,len(self.vors[name].regions)):    
    #        types[str(self.vors[name].regions[i])] = (random.choices(list(potential_regions.keys()), weights =region_weights,k=1))[0]
#
    #    fig = voronoi_plot_2d(self.vors[name], show_vertices=False, line_colors='white',line_width=0.0, line_alpha=0.0, point_size=1)
    #    fig.set_size_inches(18.5, 10.5)
    #    
    #    for region in self.vors[name].regions:
    #        if not -1 in region:
    #            polygon = [self.vors[name].vertices[i] for i in region]
    #            plt.fill(*zip(*polygon),color=potential_regions[types[str(region)]],alpha=0.4)
    #        plt.xlim(right=0, left=self.size)
    #        plt.ylim(bottom=0, top=self.size)
    #    
    #    return types

    def print_map(self,name=""):
        cmap="inferno"
        with open('/Users/cetiners/Desktop/Thesis/human_error/tools/utils.txt') as f:
            pcolors = f.read()
            [[0, 0.1, 0.5, 0.95, 1.0], ["dodgerblue","moccasin","green","gray","white"]]
        pcolors = json.loads(pcolors)

        if name in pcolors.keys():
            cvals  = pcolors[name][0]
            colors  = pcolors[name][1]
            tuples = list(zip(cvals, colors))
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples)
        
        fig, ax = plt.subplots(1,1)
        fig.set_dpi(150)
        fig.set_size_inches(20, 14)
        ax.imshow(self.views[name],cmap)



    
