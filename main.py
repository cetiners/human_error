from map_manager.map_generator import *
from genetic_algorithm import *

nw = map()

nw.populate_map(n_locations=1024, name="terrain",relaxed=True,k=100)
nw.populate_map(n_locations=1024, name="civilisation",relaxed=True,k=100)
nw.populate_map(n_locations=1024, name="threat",relaxed=True, k=100)
nw.populate_map(n_locations=1024, name="faction",relaxed=True, k=100)

nw.attribute_view(seed_1=20,seed_2=30,map_name="terrain",view_name="terrain")
nw.attribute_view(seed_1=40,seed_2=50,map_name="civilisation",view_name="civilisation")
nw.attribute_view(seed_1=34,seed_2=34,map_name="threat",view_name="threat",double=False)
nw.attribute_view(seed_1=34,seed_2=34,map_name="faction",view_name="faction",double=True)