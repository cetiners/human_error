import numpy as np
import matplotlib.pyplot as plt
from player_character import npc
from scipy.spatial import Voronoi, voronoi_plot_2d,  cKDTree
import random


class map():

    def __init__(self, name="Map", size=1024):
        self.name = name
        self.size = int(size**0.5)
        self.coord = np.zeros((self.size,self.size),dtype="int")

        self.location_coordinates = {}
        self.location_events = {}
        self.vors = {}

        self.interactions = {}
         

    def place_character(self):
        return [random.uniform(0.1,float(self.size)) for i in range(2)]

    def populate_map(self, n_locations=10, name="Regions", is_event=False):
        centroids = [tuple([random.uniform(0.1,float(self.size)) for i in range(2)]) for i in range(n_locations)]
        centroids_rounded = [[float(format(centroid[0], '.2f')),float(format(centroid[1], '.2f'))] for centroid in centroids]
        vor = Voronoi(centroids_rounded)
        fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='black',line_width=0.5, line_alpha=0.6, point_size=1)
        fig.set_size_inches(18.5, 10.5)
        for region in vor.regions:
            if not -1 in region:
                polygon = [vor.vertices[i] for i in region]
                plt.fill(*zip(*polygon),alpha=0.4)
                plt.xlim(right=0, left=self.size)
                plt.ylim(bottom=0, top=self.size)
        self.vors[name] = vor
        self.location_coordinates[name] = vor.points
        self.location_events[name] = is_event
        return vor

    def event_starter(self, event, player):
        location = player.location

        if event == "ambush":
            goblin = npc("Grognag",self,xp=20,p_health=15)
            player.battle(goblin, "Goblin Ambush")


    def check_region(self,coordinates):
        points = self.vor.points
        voronoi_kdtree = cKDTree(points)
        dst, regions = voronoi_kdtree.query(coordinates)
        return regions

    def create_regions(self, name, potential_regions, region_weights):
        types = {}
        for i in range(0,len(self.vors[name].regions)):    
            types[str(self.vors[name].regions[i])] = (random.choices(list(potential_regions.keys()), weights =region_weights,k=1))[0]

        fig = voronoi_plot_2d(self.vors[name], show_vertices=False, line_colors='white',line_width=0.0, line_alpha=0.0, point_size=1)
        fig.set_size_inches(18.5, 10.5)
        for region in self.vors[name].regions:
            if not -1 in region:
                polygon = [self.vors[name].vertices[i] for i in region]
                plt.fill(*zip(*polygon),color=potential_regions[types[str(region)]],alpha=0.4)
            plt.xlim(right=0, left=self.size)
            plt.ylim(bottom=0, top=self.size)
        return types
        