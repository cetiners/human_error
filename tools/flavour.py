import os
import time
import sys
import random
# To clean the screen.

os.system("clear")

# Have organic looking text.

def typing(message):
    print("")
    #print(message) # Eliminate this after testing...
    for word in message:
        time.sleep(random.choice([0.3, 0.11, 0.08, 0.07, 0.07, 0.07, 0.06, 0.06, 0.05, 0.01]))
        sys.stdout.write(word)
        sys.stdout.flush()
    time.sleep(.1)

for i in range(1):
    typing("...")
    time.sleep(0.1)
    os.system("clear")
typing("Cold")

os.system("clear")
typing("It is very cold")