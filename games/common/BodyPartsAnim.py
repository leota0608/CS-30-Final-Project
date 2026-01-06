import os
import time
import random
class BodyPartsAnim:
    def __init__(self, player):
        self.player = player
    def choose_body_part_anim(self, body_part):
        t = 0.3
        dt = 0.025
        last_output = None
        for i in range(32):
            choice = random.choice(self.player.bodyParts)
            while choice  == last_output:
                choice = random.choice(self.player.bodyParts)
            print(f"\rChoosing body parts: [{choice}]{' '*100}", end='', flush = True)
            last_output = choice
            time.sleep(t)
            if t < 0.05:
                dt*=-1
            t-=dt
        print(f"\rChoosing body parts: [{body_part}]{' '*100}")

    def screen_flickering_anim(self, body_part):
        for i in range(15):
            os.system("cls")
            time.sleep(0.01)
            print('A', end='', flush = True)
            color_code="\033[91m"
            print(f"{color_code}{'a'*i}!", end='', flush = True)
            time.sleep(0.05)

        os.system("cls")
        print("Aaaaaaaaaaaaaaaa!")
        time.sleep(1.2)
        os.system("cls")
        time.sleep(1.8)
        output = ["It hurts...", "", f"My {body_part}!", "", f"Where is my {body_part}!", "",  "Aaaaaaaaa!", "", ""]
        for i in output:
            os.system("cls")
            print(i, end='', flush = True)
            time.sleep(1.1)

        print("\033[0m", end='')
        for i in range(2):
            for j in range(1, 4):
                print(f"\r{'.'*j}", end='', flush = True)
                time.sleep(0.7)
            os.system("cls")
            time.sleep(0.7)
        os.system("cls")