import random

def get_karma():
    alig = "neutral"
    karma_points = random.randint(-1000,1000)
    if karma_points < -500:
        alig = "evil"
    elif (karma_points <= - 500) & (karma_points >= 500):
        alig = "neutral"
    elif karma_points > 500:
        alig = "good"
    return karma_points, alig

def get_keys():
    keys = [0 for i in range(5)]
    return keys