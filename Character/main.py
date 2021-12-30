
from dice import dice
from player_character import npc
from interaction import event
from map_manager import map
import numpy as np

denizli = map()

denizli.populate_map(80, name="terrain")
denizli.populate_map(250, name="ambush", is_event=True)

ceto = npc("ceto",denizli,xp = 1000,p_type="player")

goblin = npc("goblin", denizli, xp=1, p_type="npc")

possible_terrains = {"Water":"#3396ff","Mountains":"#a7a7a7","Grassland":"#53e939"}

denizli.create_regions("ambush", possible_terrains, [0.2,0.3,0.5])

a = denizli.location_coordinates["ambush"][3]
print(a)
ceto.travel(a)