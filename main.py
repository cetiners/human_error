from map_engine.map_generator import map
from map_engine.noise import toddler
from map_engine.world_encounters import *
from map_engine.map_ga.mutation import * 
from map_engine.map_ga.crossover import * 
import pickle
from matplotlib import colors
from tools.utils import required_n_enc

nw = map()

nw.populate_map(n_locations=1024, name="terrain",relaxed=True,k=100)
nw.populate_map(n_locations=1024, name="civilisation",relaxed=True,k=100)
nw.populate_map(n_locations=1024, name="threat",relaxed=True, k=100)
#nw.populate_map(n_locations=1024, name="faction",relaxed=True, k=100)

nw.attribute_view(seed_1=24,seed_2=34,map_name="terrain",view_name="terrain")
nw.attribute_view(seed_1=40,seed_2=50,map_name="civilisation",view_name="civilisation")
nw.attribute_view(seed_1=34,seed_2=34,map_name="threat",view_name="threat",double=False)
#nw.attribute_view(seed_1=67,seed_2=89,map_name="faction",view_name="faction",double=True)

nw.attribute_centroids("terrain")
nw.land_mask()


encounters = w_encounter_manager(nw, [i for i in required_n_enc])
encounters.let_there_be_light()
