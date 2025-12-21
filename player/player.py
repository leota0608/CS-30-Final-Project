import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import random
from datetime import date
import json
import time

class Player:
    def __init__(self):
        self.date = date.today()
        self.score = 0
        self.lost_body_parts = []
        try:
            with open("player/bodyParts.json", 'r') as content:
                data = json.load(content)
                self.bodyParts = data["bodyParts"]
                self.probability = data["probability"]
        except FileNotFoundError:
            print("We didn't find any of your body parts, you died...")
            # file not found
        except:
            print("oops, you died of a heart attack...")
            # other errors
        else:
            print("Checking body integrity...")
            time.sleep(0.7)
        finally:
            print("Personal information loading...")
            time.sleep(0.7)

    def get_name(self):
        while True:
            string = input("Write down your name: ")
            confirm = input("Is this really your name?(y/n)")
            if(confirm.lower() == "y" or confirm.lower() == "yes"):
                self.name = string
                return

    def store_player_information(self):
        # add try and except
        try:
            with open("player/playingRecord.json", 'r') as file:
                record = json.load(file)
        except FileNotFoundError:
            print("We cannot store your information, you died...") 
            time.sleep(0.7)
        except:
            print("You died from some unknown reasons...")
            time.sleep(0.7)
        else:
            print("Storing personal information...")
            time.sleep(0.7)
        total_num = record["Total Player"]
        record["Total Player"] += 1
        record[str(total_num+1)] = {"Name": self.name,
                                    "Date": str(self.date),
                                    "Score": self.score,
                                   "Game record": {"Game 1": None,# win/lose: True/False
                                                    "Game 2": None,
                                                    "Game 3": None,
                                                    "Game 4": None},
                                    "Lost body parts": []}
        with open("player/playingRecord.json", 'w') as file:
            json.dump(record, file, indent = 4)
    
    def store_game_result(self, game_num, result):
        with open("player/playingRecord.json", 'r') as file:
            record = json.load(file)
        record[str(record["Total Player"])]["Game record"][f"Game {game_num}"] = result
        with open("player/playingRecord.json", 'w') as file:
            json.dump(record, file, indent = 4)

    def update_score(self):
        with open("player/playingRecord.json", 'r') as file:
            record = json.load(file)
        for i, j in record[str(record["Total Player"])]["Game record"].items():
            if j == True:
                record[str(record["Total Player"])]["Score"] += 25
        with open("player/playingRecord.json", 'w') as file:
            json.dump(record, file, indent = 4)

    def choose_body_part(self):
        r = random.randint(1, 1000)
        for i in range(0, len(self.probability)):
            if r <= self.probability[i]:
                if self.bodyParts[i] in self.lost_body_parts:
                    self.choose_body_part()
                    break
                self.lost_body_parts.append(self.bodyParts[i])
                return self.bodyParts[i]
    
    def lose(self, body_part):
        self.lost_body_parts.append(body_part)
        with open("player/playingRecord.json", 'r') as file:
            record = json.load(file)
        record[str(record["Total Player"])]["Lost body parts"].append(body_part)
        #save
        with open("player/playingRecord.json", 'w') as file:
            json.dump(record, file, indent = 4)


def clear_all_playing_records():
    with open("player/playingRecord.json", 'w') as file:
        json.dump({"Total Player": 0}, file, indent = 4)

#clear_all_playing_records()

# p = Player()
# p.choose_body_part()