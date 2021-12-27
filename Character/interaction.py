
from dice import dice
import random

class event:
    def __init__(self, name="Interaction Name"):
        self.name = name
        self.location = random.uniform(0.1,float(32))

    def battle(self, p1, p2):

        print(f"{p1.name} and {p2.name} faces each other on {self.name}!")

        if p1.dex > p2.dex:
            faster = p1
            slower = p2
        else:
            faster = p2
            slower = p1

        turns = [faster, slower]
        round = 0 

        while True:
            attacker = turns[0]
            defender = turns[1]
            roll_to_attack = dice(20)
            attack_roll = dice(20)
            roll_to_defend = dice(20)
            round += 1

            print(f"{attacker.name} tries to hit!")

            if roll_to_attack == 20:
                print("Critical Success")
                attack_roll = attack_roll*1.5
            elif roll_to_attack == 0:
                print("Critical Failiure")
                attack_roll = attack_roll * 0.5
                attacker.receive_damage(attack_roll)

            if roll_to_attack >= roll_to_defend:
                print("Success!")
                defender.receive_damage(attack_roll)
            else:
                print(f"{defender.name} gets out of the way!")
            turns = turns[::-1]

            if p1.hp <= 0:
                winner = p2
                print(f"{p1.name} has died, {p2.name} is victorious!")
                print("Battle is over.")
                break
                
            elif p2.hp <= 0:
                winner = p1
                print(f"{p2.name} has died, {p1.name} is victorious!")
                print("Battle is over.")
                break
            print("----------------------------------------------------------------")
        winner.gain_xp(500)
        winner.money_transaction(50, op="gain")
        winner.adjust_karma(50)

    def conversation():
        pass

    def barter():
        pass

    def item_interaction():
        pass


    def quest_giver():
        pass

    def scenery():
        pass
        
    def ability_check(self, char, n_dice=1, check_type="str", advantage=False, disadvantage=False):

        modifier = char.mod_attributes[check_type]
        rolls = []

        for i in range(n_dice):
            roll = dice(20)
            if roll == 20:
                rolls.append(200)
            elif roll == 0:
                rolls.append(-100)
            else:
                rolls.append(roll + modifier)

        if advantage == True:
            return max(rolls)
        elif disadvantage == True:
            return min(rolls)
        else:
            return rolls[0]