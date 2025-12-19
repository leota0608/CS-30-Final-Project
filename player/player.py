from datetime import date
import json
import time

class Player:
    def __init__(self):
        self.name = self.get_name()
        self.date = date.today()
        self.score = 0
        try:
            with open("bodyParts.json", 'r') as content:
                self.bodyParts = json.load(content)["bodyParts"]
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
        self.store_player_information()

    def get_name(self):
        while True:
            string = input("Write down your name: ")
            confirm = input("Is this really your name?(y/n)")
            if(confirm.lower() == "y" or confirm.lower() == "yes"):
                return string

    def store_player_information(self):
        # add try and except
        with open("playingRecord.json", 'r') as file:
            record = json.load(file)
        total_num = record["Total Player"]
        record["Total Player"] += 1
        record[str(total_num+1)] = {"Name": self.name,
                                    "Date": self.date,
                                    "Score": self.score}
        with open("playingRecord.json", 'w') as file:
            json.dump(record, file, indent = 4)

player = Player()

