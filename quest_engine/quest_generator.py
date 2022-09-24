#   
# dex: Stealth, Steal, 
# str
# con
# int
# wis 
# cha
#   
#   
#   
#   

class quest:
    """
    Class that holds attributes of a single quest.

    Attributes:
        map (str): The map the quest is on.
        quest_type (str): The attributes quest focuses on, origin of the challange.
        difficulty (int): The difficulty level of the quest.
        arc (str): The overall game arc that the quest belongs to.
        quest_steps (int): The number of keys and locks in the quest.
        quest_radius (int): Total distance needed to travel for the quest.
        fitness (int): The fitness of the quest.
    """
    
    def __init__(self, map, quest_type, difficulty, arc, quest_steps, quest_radius):

        self.map = map
        self.quest_type = quest_type
        self.dif = difficulty
        self.steps = quest_steps
        self.arc = arc
        self.radius = quest_radius

        self.fitness = self.check_fitness()

    def check_fitness(self):
        return 0

    def __str__(self):
        return f"{self.quest_type} {self.dif} {self.arc} {self.steps}"
    
    def __repr__(self):
        return f"{self.quest_type} {self.dif} {self.arc} {self.steps}"