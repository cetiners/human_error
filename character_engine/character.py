
import random
import time

from tools.flavour import typing

from matplotlib.pyplot import xcorr

from character_engine.character_attributes import race_picker, race_bonus, attribute_picker, size_selector, speed_selector, class_picker, modifier, level_calculator, armor_class, starting_wealth
from character_engine.states import get_karma, get_keys

from tools.dice import dice

import operator
import fantasynames as names


class npc:
    """ 
    The class for generating npc's at t=0 of game time, attributes, abilities that are the same as the 
    player character. NPC's are created to be interacted with the player.
    """
    def __init__(self, xp=0, p_type="npc",p_health=100):
        

        self.ptype = p_type
        self.c_race = race_picker()
        self.c_class = class_picker()
        self.wealth = starting_wealth(self.c_class)
        #self.map = map

        if "Elf" in self.c_race:
            self.name = names.elf()
        elif "Dwarf" in self.c_race:
            self.name = names.dwarf()
        elif "Halfling" in self.c_race:
            self.name = names.hobbit()
        elif "Gnome" in self.c_race:
            self.name = names.hobbit()
        elif "Human" in self.c_race:
            self.name = names.human()
        else:
            self.name = names.anglo()


        # Attributes
        atr = attribute_picker()
        bonus = race_bonus(self.c_race)

        self.dex = int(atr["dex"] + bonus.dex.values[0])
        self.str = int(atr["str"] + bonus.str.values[0])
        self.con = int(atr["con"] + bonus.con.values[0])
        self.int = int(atr["int"] + bonus.int.values[0])
        self.wis = int(atr["wis"] + bonus.wis.values[0])
        self.cha = int(atr["cha"] + bonus.cha.values[0])

        self.attributes = {"dex" : self.dex, "str" : self.str, "con" : self.con, "int" : self.int, "wis" : self.wis, "cha" : self.cha}

        self.mod_dex = int(modifier(self.dex) + self.dex)
        self.mod_str = int(modifier(self.str) + self.str)
        self.mod_con = int(modifier(self.con) + self.con)
        self.mod_int = int(modifier(self.int) + self.int)
        self.mod_wis = int(modifier(self.wis) + self.wis)
        self.mod_cha = int(modifier(self.cha) + self.cha)

        self.mod_attributes = {"dex" : self.mod_dex, "str" : self.mod_str, "con" : self.mod_con, "int" : self.mod_int, "wis" : self.mod_wis, "cha" : self.mod_cha}

        self.size = size_selector(self.c_race)
        self.speed = speed_selector(self.c_race)
        self.xp = xp
        self.max_hp = p_health
        self.hp = p_health
        self.ac = armor_class()
        self.level = level_calculator(self.xp)

        # Player state:
        self.karma, self.alignment = get_karma()
        self.state = {}
        self.inventory = ["Don"]
        self.keys = get_keys()
        #self.location = self.map.place_character()

        if p_type == "npc":
            self.wealth = random.randint(0,15)
            self.karma = random.randint(-50,+50)

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

        typing(f"{self.name} starts a journey.")

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
                    typing(f"{self.name} encounters an {location}")
                    if self.map.location_events[location]:
                        typing("Get ready!")
                        self.location = stop
                        typing(f"Player location: {self.location}")
                        self.map.event_starter(location, self)
                        break
                    break
                else:
                    continue
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

    def level_up(self,levels):
        self.level += levels
        self.state["level"] = self.level

        if self.level < 5:
            bonus = 2
        elif self.level < 9:
            bonus = 3
        elif self.level < 13:
            bonus = 4
        elif self.level < 17:
            bonus = 5
        else:
            bonus = 6

        bonus = int(bonus/len(class_attributes[self.c_class]))

        for atr in class_attributes[self.c_class]:
            if atr == "dex":
                self.mod_dex += bonus
            elif atr == "str":
                self.mod_str += bonus
            elif atr == "con":
                self.mod_con += bonus
            elif atr == "int":
                self.mod_int += bonus
            elif atr == "wis":
                self.mod_wis += bonus
            elif atr == "cha":
                self.mod_cha += bonus

        self.mod_attributes = {"dex" : self.mod_dex, "str" : self.mod_str, "con" : self.mod_con, "int" : self.mod_int, "wis" : self.mod_wis, "cha" : self.mod_cha}



    def battle(self, p2, event_name=""):
        typing(f"{self.name} and {p2.name} faces each other on {event_name}!")
        if self.dex > p2.dex:
            faster = self
            slower = p2
        else:
            faster = p2
            slower = self
        turns = [faster, slower]
        round = 0 
        while True:
            attacker = turns[0]
            defender = turns[1]
            roll_to_attack = dice(20)
            attack_roll = dice(20)
            roll_to_defend = dice(20)
            round += 1
            typing(f"{attacker.name} tries to hit!")
            if roll_to_attack == 20:
                print("Critical Success")
                attack_roll = attack_roll*1.5
            elif roll_to_attack == 0:
                print("Critical Failiure")
                attack_roll = attack_roll * 0.5
                attacker.receive_damage(attack_roll)
            if roll_to_attack >= roll_to_defend:
                print("\nSuccess!")
                defender.receive_damage(attack_roll)
            else:
                typing(f"{defender.name} gets out of the way!")
            turns = turns[::-1]
            if self.hp <= 0:
                winner = p2
                loser = self
                typing(f"{self.name} has died, {p2.name} is victorious!")
                typing("Battle is over.")
                break
            elif p2.hp <= 0:
                winner = self
                loser = p2
                typing(f"{p2.name} has died, {self.name} is victorious!")
                time.sleep(0.2)
                print("\nBattle is over.")
                break
            print("\n----------------------------------------------------------------")

        winner.gain_xp(loser.xp)
        winner.money_transaction(loser.wealth, op="gain")
        if loser.alignment == "evil":
            winner.adjust_karma(+50)
        elif loser.alignment == "good":
            winner.adjust_karma(-50)


    def character_sheet(self):
        print(f"Meet {self.name}!, a level {self.level} {self.ptype}")
        print(f"Race: {self.c_race}")
        print(f"Class: {self.c_class}")
        print(f" Strength: {self.mod_str} \n Dexterity: {self.mod_dex} \n Constitution {self.mod_con} \n Intelligence: {self.mod_int} \n Wisdom: {self.mod_wis} \n Charisma: {self.mod_cha}")
        print(f"A {self.size} sized character with a speed of {self.speed/6} feet per second.")
        print(f"Inventory: {self.wealth} coins.\n")
        print("-------------------------------------------")
        #print(self.state)


class_attributes = {
    "Fighter": ["dex","str"],
    "Rogue": ["dex"],
    "Wizard": ["int"],
    "Cleric": ["wis"],
    "Ranger": ["dex","wis"],
    "Barbarian": ["str"],
    "Monk": ["wis","dex"],
    "Paladin": ["cha","str"],
    "Druid": ["wis"],
    "Bard": ["cha"],
    "Sorcerer": ["cha"],
    "Warlock": ["cha"],
}


def select_npc(challange_type):

    char = npc()

    while max(char.mod_attributes.items(), key=operator.itemgetter(1))[0] != challange_type:
        char = npc()

    return char
    




