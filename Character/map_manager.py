import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d,  cKDTree
import random


class map():

    def __init__(self, name="Map", size=1024):
        self.name = name
        self.size = int(size**0.5)
        self.coord = np.zeros((self.size,self.size),dtype="int")


    def place_character(self, character):
        self.coord[(character.location[0]-1),(character.location[1]-1)] = 1


    def populate_map(self, n_locations=10, name="Regions"):
        centroids = [tuple([random.uniform(0,self.size) for i in range(2)]) for i in range(n_locations)]
        vor = Voronoi(centroids)
        fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='black',line_width=0.5, line_alpha=0.6, point_size=1)
        fig.set_size_inches(18.5, 10.5)
        for region in vor.regions:
            if not -1 in region:
                polygon = [vor.vertices[i] for i in region]
                plt.fill(*zip(*polygon),alpha=0.4)
                plt.xlim(right=0, left=self.size)
                plt.ylim(bottom=0, top=self.size)
        self.regions = vor
        return vor

    def check_region(self,coordinates):
        points = self.regions.points
        voronoi_kdtree = cKDTree(points)
        dst, regions = voronoi_kdtree.query(coordinates)
        return regions

    def create_regions(self, potential_regions):
        types = {}
        for i in range(0,len(self.regions.regions)):    
            types[str(self.regions.regions[i])] = (random.choice(list(potential_regions.keys())))

        fig = voronoi_plot_2d(self.regions, show_vertices=False, line_colors='black',line_width=0.5, line_alpha=0.6, point_size=1)
        fig.set_size_inches(18.5, 10.5)
        for region in self.regions.regions:
            if not -1 in region:
                polygon = [self.regions.vertices[i] for i in region]
                plt.fill(*zip(*polygon),color=potential_regions[types[str(region)]],alpha=0.4)
            plt.xlim(right=0, left=self.size)
            plt.ylim(bottom=0, top=self.size)
        return types