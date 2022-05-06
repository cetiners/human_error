
from character_engine.player_character import npc
from map_manager.map_generator import map

portugal = map()

portugal.populate_map(250, name="ambush", is_event=True)

mauro = npc("Mauro",portugal,xp = 1000,p_type="player")

possible_terrains = {"Water":"#3396ff","Mountains":"#a7a7a7","Grassland":"#53e939"}
portugal.create_regions("ambush", possible_terrains, [0.2,0.3,0.5])

a = portugal.location_coordinates["ambush"][3]

mauro.travel(a)