
import random

from matplotlib.pyplot import xcorr

from character_attributes import race_picker, race_bonus, attribute_picker, size_selector, speed_selector, class_picker, modifier, level_calculator, armor_class, starting_wealth
from states import get_karma, get_keys


class npc:
    """ 
    The class for generating npc's at t=0 of game time, attributes, abilities that are the same as the 
    player character. NPC's are created to be interacted with the player.
    """
    def __init__(self, name, map, xp=0, p_type="npc"):
        
        self.name = name
        self.ptype = p_type
        self.c_race = race_picker()
        self.c_class = class_picker()
        self.wealth = starting_wealth(self.c_class)
        self.map = map

        # Attributes
        atr = attribute_picker()
        bonus = race_bonus(self.c_race)

        self.dex = atr["dex"] + bonus.dex.values[0]
        self.str = atr["str"] + bonus.str.values[0]
        self.con = atr["con"] + bonus.con.values[0]
        self.int = atr["int"] + bonus.int.values[0]
        self.wis = atr["wis"] + bonus.wis.values[0]
        self.cha = atr["cha"] + bonus.cha.values[0]

        self.attributes = {"dex" : self.dex, "str" : self.str, "con" : self.con, "int" : self.int, "wis" : self.wis, "cha" : self.cha}

        self.mod_dex = modifier(self.dex)
        self.mod_str = modifier(self.str)
        self.mod_con = modifier(self.con)
        self.mod_int = modifier(self.int)
        self.mod_wis = modifier(self.wis)
        self.mod_cha = modifier(self.cha)

        self.mod_attributes = {"dex" : self.mod_dex, "str" : self.mod_str, "con" : self.mod_con, "int" : self.mod_int, "wis" : self.mod_wis, "cha" : self.mod_cha}

        self.size = size_selector(self.c_race)
        self.speed = speed_selector(self.c_race)
        self.xp = xp
        self.max_hp = 123
        self.hp = 150
        self.ac = armor_class()
        self.level = level_calculator(self.xp)

        # Player state:
        self.karma, self.alignment = get_karma()
        self.state = {}
        self.inventory = ["Don"]
        self.keys = get_keys()
        self.location = self.map.place_character()

        if p_type != "npc":
            #for atr in self.attrisbutes:
            #    self.state[atr] = self.attributes[atr]
            self.state["hp"] = self.hp
            self.state["xp"] = self.xp
            self.state["level"] = self.level
            self.state["karma"] = self.karma
            self.state["alignment"] = self.alignment
            self.state["wealth"] = self.wealth
            self.state["keys"] = self.keys
            self.state["inventory"] = self.inventory
            self.state["max_hp"] = self.max_hp

    def travel(self, destination, destination_name = None):

        x_1,y_1 = self.location[0], self.location[1]
        x_2,y_2 = destination[0], destination[1]

        if destination_name != None:
            self.location_name = destination_name
        else:
            self.location_name = "Unknown"

        travel_distance = (((x_2 - x_1)**2)+((y_2 - y_1)**2))**(0.5)
        
        steps = int(travel_distance) * 10
        slope = abs(y_2-y_1) / abs(x_2 - x_1)
        intercept = y_1 - (slope * x_1)
        stops = []

        x_steps = int(abs(x_2 - x_1) * 10)
        y_steps = int(abs(y_2 - y_1) * 10)

        x = x_1

        for i in range(x_steps):
            if x_1 < x_2:
                x = x + 0.1
            elif x_1 > x_2:
                x = x - 0.1        
            y = slope * x + intercept
            stops.append([float(format(x, '.2f')),float(format(y, '.2f'))])
        
        y = y_1

        for j in range(y_steps):
            if y_1 < y_2:
                y = y + 0.1
            elif y_1 > y_2:
                y = y - 0.1        
            x = (y - intercept) / slope
            stops.append([float(format(x, '.2f')),float(format(y, '.2f'))])
            stops.append([float(format(destination[0], '.2f')),float(format(destination[1], '.2f'))])
            stops.sort()


        # kontrolü stops loopundan başlatmak elzem, bütün yolu gitmiyor zira, ya da stepleri yaşat self.location'ları her seferinde çek.

        for stop in stops:
            for location in self.map.location_coordinates:
                if stop in self.map.location_coordinates[location]:
                    print(f"You encountered {location}")
                    if self.map.location_events[location]:
                        print("Get ready!")
                        self.location = stop
                        print(f"Player location: {self.location}")
                        #event_starter(self.location)
                        break

    def adjust_karma(self, points):
        self.karma = self.karma + points
        self.state["karma"] = self.karma
        self.state["alignment"] = self.alignment

    def receive_damage(self, points):
        self.hp -= points
        if self.hp <= 0:
            print("Knockdown")
        print(f"{self.name} sustains {points} damage. Current hp: {self.hp}")
        self.state["hp"] = self.hp
    
    def money_transaction(self, coins, op = "pay"):
        if op == "pay":
            if self.wealth < coins:
                print(f"You don't have the funds to pay that, you poor fuck.")
            else:
                self.wealth -= coins
                print(f"You have paid {coins} gold coins. Current balance = {self.wealth}")
        elif op == "gain":
            self.wealth += coins
            print(f"{self.name} have gained {coins} gold coins. Current balance = {self.wealth}")
        self.state["wealth"] = self.wealth

    def gain_key(self,key_no=1):
        self.keys[key_no-1] = 1
        print(f"{self.name} gained the key number {key_no}")
        self.state["keys"] = self.keys

    def heal(self, points):
        self.hp += points
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} was healed for {points} hit points, bringing then up to {self.hp}.")
        self.state["hp"] = self.hp
        self.state["max_hp"] = self.max_hp

    def gain_item(self, item = "pebble"):
        self.inventory = self.inventory.append(item)
        print(f"{self.name} added {item} to their inventory!")
        self.state["inventory"] = self.inventory

    def gain_xp(self, xp_points):
        level = self.level
        self.xp += xp_points
        self.level = level_calculator(self.xp)
        if level < self.level:
            print(f"{self.name} leveled up to level {self.level}!")
        self.state["xp"] = self.xp
        self.state["level"] = self.level

    def character_sheet(self):
        print(f"Meet {self.name}!, a {self.ptype}\n")
        print(f"Character race: {self.c_race}")
        print(f"Character class: {self.c_class}\n")
        print(f" Strength: {self.str} \n Dexterity: {self.dex} \n Constitution {self.con} \n Intelligence: {self.int} \n Wisdom: {self.wis} \n Charisma: {self.cha}")
        print(f"A {self.size} sized adventurer with a speed of {self.speed/6} feet per second.")
        print(f"{self.name} starts this adventure with {self.wealth} coins.")
        print(self.state)




