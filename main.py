from map_engine.map_generator import map
from encounter_manager.world_encounters import *
import pickle
from matplotlib import colors
from quest_engine.quest_generator import *
import matplotlib.pyplot as plt

nw = map()
nw.populate_map(n_locations=1024, name="terrain", relaxed=True, k=100)
nw.populate_map(n_locations=4096, name="civilisation", relaxed=True, k=250)
nw.populate_map(n_locations=1024, name="story_act", relaxed=True, k=250)
nw.populate_map(n_locations=1024, name="threat", relaxed=True, k=100)

nw.attribute_view(seed_1=24, seed_2=34,
                  map_name="terrain", view_name="terrain")
nw.attribute_view(seed_1=98, seed_2=50, map_name="civilisation",
                  view_name="civilisation", double=False)
nw.attribute_view(seed_1=34, seed_2=34, map_name="threat",
                  view_name="threat", double=False)
nw.attribute_view(seed_1=16, seed_2=16, map_name="story_act",
                  view_name="story_act", double=False)

nw.attribute_centroids("civilisation")
nw.attribute_centroids("terrain")
nw.land_mask()

with open('map_nw', 'wb') as f:
    pickle.dump(nw, f)


with open("map_nw", "rb") as f:
    nw = pickle.load(f)


encounters = w_encounter_manager(nw, [i for i in required_n_enc])
encounters.let_there_be_light()

params = {
    "gens": 100,
    "pop_size": 200,
    "mu_p": .5,
    "xo": "pmx",
    "mutation": "random_point",
    "print_it": True
}

ql = quest_library(nw,shelf_size=100,params=params)



cmap = colors.ListedColormap(
    ["blue", "white", "yellowgreen", "khaki", "lawngreen", "slategrey", "darkgreen"])
cmap_arcs = colors.ListedColormap(
    ["blue", "khaki", "khaki", "khaki", "khaki", "khaki", "khaki", "brown", "brown", "brown", "black", ])

ter = nw.views["terrain"].copy()
civ = nw.views["civilisation"].copy()
thr = nw.views["threat"].copy()
arc = nw.views["story_act"].copy()

fig, ax = plt.subplots(2, 2)
fig.set_dpi(150)
fig.set_size_inches(24, 24)

ax[0, 1].imshow(ter.T, cmap=cmap, alpha=.66)
ax[0, 1].set_title("Terrain")
ax[0, 1].scatter(lst1, lst2, color="black", s=20)

#ax[0, 1].scatter([i[0] for i in q.path], [i[1] for i in q.path], color="black", s=15)
#ax[0, 1].plot([i[0] for i in q.path], [i[1] for i in q.path], color="red",linestyle="-.",linewidth=1, alpha=.5)

ax[1, 1].imshow(civ.T, cmap=cmap_arcs, alpha=0.66)
ax[1, 1].set_title("Civilisation")
ax[1, 1].scatter(lst1, lst2, color="black", s=20)

#ax[1, 1].scatter([i[0] for i in q.path], [i[1] for i in q.path], color="black", s=15)
#ax[1, 1].plot([i[0] for i in q.path], [i[1] for i in q.path], color="red",linestyle="-.",linewidth=1, alpha=.5)

ax[1, 0].imshow(thr.T, cmap="Reds", alpha=0.66)
ax[1, 0].set_title("Threat")
ax[1, 0].scatter(lst1, lst2, color="black", s=20)

#ax[1, 0].scatter([i[0] for i in q.path], [i[1] for i in q.path], color="black", s=15)
#ax[1, 0].plot([i[0] for i in q.path], [i[1] for i in q.path], color="red",linestyle="-.",linewidth=1, alpha=.5)

ax[0, 0].imshow(arc.T, cmap="Blues", alpha=0.66)
ax[0, 0].set_title("Story Act")
ax[0, 0].scatter(lst1, lst2, color="black", s=20)

#ax[0, 0].scatter([i[0] for i in q.path], [i[1] for i in q.path], color="black", s=15)
#ax[0, 0].plot([i[0] for i in q.path], [i[1] for i in q.path], color="red",linestyle="-.",linewidth=1, alpha=.5)
