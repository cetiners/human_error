import random

def dice(type):
    potential_outcomes = [score+1 for score in range(type)]
    roll = random.choice(potential_outcomes)
    return roll