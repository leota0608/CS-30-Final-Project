import random
from datetime import date
import json
import time

class Player:

    HEAD_PARTS = {
        "head": 
"""
 ┌───────────┐        
?| {}       {} |?
 |    |||    |
 |  {}  |
 └───────────┘""",
        "eye": "*",
        "blind_eye": "~",
        "smile": "└─────┘",
        "sad": "┌─────┐",
    }

    BODY_ELEMNTS = {
        "main_body": 
"""
┌───────┐
|   o   |
|   o   |
|   o   |
|   o   |
└───────┘""",
        "right arm": 
"""
┌──────────┐
|          |
└──────────┘""",
        "left arm": 
"""
┌──────────┐
|          |
└──────────┘""",
        "right leg": 
"""
┌─┐
| |
| |
| |
| |
└─┘""",
        "left leg": """
┌─┐
| |
| |
| |
| |
└─┘""",
        "left hand": 
"""
=||
""", 
        "right hand": 
"""
||=""",
        "left foot": 
"""
┌─┐
___
|||""",
        "right foot": 
"""
┌─┐
___
|||""", 

    }

    def __init__(self):
        self.date = date.today()
        self.score = 0
        self.money = 1000
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

    def gain(self, body_part):
        self.lost_body_parts.remove(body_part)
        with open("player/playingRecord.json", 'r') as file:
            record = json.load(file)
        record[str(record["Total Player"])]["Lost body parts"].remove(body_part)
        #save
        with open("player/playingRecord.json", 'w') as file:
            json.dump(record, file, indent = 4)

    def indent_lines(self, text: str, spaces: int):
        padding = " " * spaces
        # Split into lines, prepend spaces, then join back
        return "\n".join(padding + line for line in text.splitlines())
    
    def removeLeadingSpace(self, lst):
        # Find first non-empty string
        start = 0
        while start < len(lst) and lst[start] == "":
            start += 1

        # Find last non-empty string
        end = len(lst) - 1
        while end >= 0 and lst[end] == "":
            end -= 1

        # Slice the list
        return lst[start:end+1] if start <= end else []

    def printBodyShape(self, missing_parts, isSad):
        # ---------- HEAD ----------
        eye = (self.HEAD_PARTS["blind_eye"]
               if "eye" in missing_parts
               else self.HEAD_PARTS["eye"])
        
        mouth = (self.HEAD_PARTS["sad"]
                 if isSad
                 else self.HEAD_PARTS["smile"])

        head = ("" if "head" in missing_parts
                else self.HEAD_PARTS["head"].format(eye, eye, mouth))

        # ---------- ARMS ----------
        left_arm = ( "" if "left arm" in missing_parts
            else self.BODY_ELEMNTS["left arm"]).split("\n")
        left_arm = self.removeLeadingSpace(left_arm)
        right_arm = ("" if "right arm" in missing_parts
            else self.BODY_ELEMNTS["right arm"]).split("\n")
        right_arm = self.removeLeadingSpace(right_arm)
        # ---------- BODY ----------
        body = self.BODY_ELEMNTS["main_body"].split("\n")
        body = self.removeLeadingSpace(body)
        # ---------- HANDS ----------
        left_hand = ("" if "left hand" in missing_parts
            else self.BODY_ELEMNTS["left hand"]).split("\n")
        left_hand = self.removeLeadingSpace(left_hand)
        right_hand = ("" if "right hand" in missing_parts
            else self.BODY_ELEMNTS["right hand"]).split("\n")
        right_hand = self.removeLeadingSpace(right_hand)
        # ---------- LEGS ----------
        left_leg = ("" if "left leg" in missing_parts
            else self.BODY_ELEMNTS["left leg"]).split("\n")
        left_leg = self.removeLeadingSpace(left_leg)
        right_leg = ("" if "right leg" in missing_parts
            else self.BODY_ELEMNTS["right leg"]).split("\n")
        right_leg = self.removeLeadingSpace(right_leg)
        # ---------- FEET ----------
        left_foot = ("" if "left foot" in missing_parts
            else self.BODY_ELEMNTS["left foot"]).split("\n")
        left_foot = self.removeLeadingSpace(left_foot)
        right_foot = ("" if "right foot" in missing_parts
            else self.BODY_ELEMNTS["right foot"]).split("\n")
        right_foot = self.removeLeadingSpace(right_foot)

        head = self.indent_lines(head, 12)
        didPrint = True

        print(head)
        body_print_list = [[left_hand, -1, 3], [left_arm, 0, 12],
                           [body, 0, 9], [right_arm, 0, 12], [right_hand, -1, 3]]
        
        # printing upper body
        while didPrint:

            didPrint = False

            for part in body_print_list:
                p = part[0]
                which = part[1]
                space = part[2]
                
                if which >= 0 and which < len(p):
                    print(p[which], end = "")
                    didPrint = True
                else:
                    print(" " * space, end = "", flush = True)
                part[1] += 1
            print()

        # printing lower body
        body_print_list = [[left_leg, 0, 3], [right_leg, 0, 3]]
        didPrint = True

        while didPrint:

            didPrint = False
            print(" " * 14, end = "")

            for part in body_print_list:
                p = part[0]
                which = part[1]
                space = part[2]

                if which >= 0 and which < len(p):
                    print(p[which], end = "")
                    print(" " * 5, end = "")
                    didPrint = True
                else:
                    print(" " * space, end = "")
                part[1] += 1
            print()

        body_print_list = [[left_foot, 0, 3], [right_foot, 0, 3]]
        didPrint = True

        while didPrint:

            didPrint = False
            print(" " * 14, end = "")

            for part in body_print_list:
                p = part[0]
                which = part[1]
                space = part[2]

                if which >= 0 and which < len(p):
                    print(p[which], end = "")
                    print(" " * 5, end = "")
                    didPrint = True
                else:
                    print(" " * space, end = "")
                part[1] += 1
            if didPrint:
                print()

    
def clear_all_playing_records():
    with open("player/playingRecord.json", 'w') as file:
        json.dump({"Total Player": 0}, file, indent = 4)
 
clear_all_playing_records()

p = Player()
# p.printBodyShape([], False)