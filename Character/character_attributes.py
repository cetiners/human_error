import random
import pandas as pd
from dice import dice

races = pd.read_csv("/Users/cetiners/Desktop/Thesis/Character/racial_stat_bonusses.csv").fillna(0)

# Amount of XP required for each rank of level
xp_to_level =  {0: 1, 300: 2, 900: 3, 2700: 4, 6500: 5, 14000: 6, 23000: 7, 34000: 8, 48000: 9, 64000: 10, 85000: 11, 100000: 12, 120000: 13, 140000: 14, 165000: 15, 195000: 16, 225000: 17, 265000: 18, 305000: 19, 355000: 20}

# Dice roll rules to determine the starting wealth of each class
wealth_dices ={'Barbarian': ['2', '4'],
                'Bard': ['5', '4'],
                'Cleric': ['5', '4'],
                'Druid': ['2', '4'],
                'Fighter': ['5', '4'],
                'Monk': ['5', '4 '],
                'Paladin': ['5', '4'],
                'Ranger': ['5', '4'],
                'Rogue': ['4', '4'],
                'Sorcerer': ['3', '4'],
                'Warlock': ['4', '4'],
                'Wizard': ['4', '4']}


def race_picker():
    # Select a random playable race
    c_race = random.choice(races.Race.to_list()[:13])
    return c_race

def race_bonus(race):
    # Pull the specific stat bonuses for a certain race.
    bonus = races[races.Race == race].iloc[:,1:-1]
    return bonus

def attribute_picker():
    # Using the budget system, randomly allocate attribute points. 
    # Each rank of attribute points has a certain cost, while the player only has access to 27 points.
    attributes = ["str","dex","con","wis","cha","int"]
    random.shuffle(attributes)
    pts_cost = {8:0,9:1,10:2,11:3,12:4,13:5,14:7,15:9}
    c_atr = {}
    pts = 27
    for atr in attributes:
        proposed = random.randint(8,15)
        cost = pts_cost[proposed]
        while cost > pts:
            proposed = random.randint(8,15)
            cost = pts_cost[proposed]
        c_atr[atr] = proposed
        pts = pts - cost

    return c_atr
    
def size_selector(race):
    # Lookup the sizes for a certain race.
    size = races[races.Race == race]["Size"]
    return size.values[0]

def speed_selector(race):
    # Lookup the speed for a certain race.
    speed = races[races.Race == race]["Speed"]
    return speed.values[0]

def class_picker():
    # Select a random class.
    classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
    return random.choice(classes)

def modifier(point):
    modifiers = {1: -5,2: -4,3: -4,4: -3,5: -3,6: -2,7: -2,8: -1,9: -1,10: 0,11: 0,12: 1,13: 1,14: 2,15: 2,16: 3,17: 3,18: 4,19: 4,20: 5,21: 5,22: 6,23: 6,24: 7,25: 7,26: 8,27: 8,28: 9,29: 9,30: 10}
    return modifiers[int(point)]

def level_calculator(xp):
    nearest_bar = max(list(filter(lambda x: xp >= x, xp_to_level.keys())))
    return xp_to_level[nearest_bar]

def armor_class():
    ac = random.randint(10, 20)
    return ac

def starting_wealth(chr_class):
    
    roll_times = wealth_dices[chr_class][0]
    roll_type = wealth_dices[chr_class][1]
    roll_sum = 0

    for i in range(int(roll_times)):
        roll_sum += dice(int(roll_type))
    return roll_sum

