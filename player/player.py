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
        "main body": 
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
        self.money = 0
        self.debth = 0
        self.lost_body_parts = []
        try:
            with open("player/PlayerStarterData.json", 'r') as content:
                data = json.load(content)
                self.bodyParts = data["bodyParts"]
                self.probability = data["probability"]
                self.money = data["current money"]
                self.debth = data["debth"]
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

    def indentLines(self, text: str, spaces: int):
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
    
    def printPlayerMessage(self, isSad):
        print(f"my name is {self.name}")
        if isSad:
            print("I am not feeling good.")
            print("I have lost", end = "")
            for part in self.lost_body_parts:
                print(", " + part, end="")
            print(".")
            print("you know ", end = "", flush = True)
            time.sleep(1)
            print("it hurts so much.")
            print("please help me.")
            print("please ...")
        else:
            print("I am very happy little kid.")
            print("Let's crush this game.")

    def addMoney(self, add):
        self.money += add

    def printBodyShape(self):
        missing_parts = self.lost_body_parts
        isSad = len(self.lost_body_parts) != 0
        """
        """
        def printBodyAcross(first, body_print_list, bet):
            """
            Prints the body line by line.
            first: number of spaces printed before each line.
            body_print_list: a prepared list of configured parts.
            See the comments below for more information regarding this
            parameter.
            bet: number of spaces printed after each line
            """
            # would be False when fully printed
            didPrint = True
            while didPrint:
                didPrint = False
                print(" " * first, end="")

                for part in body_print_list:
                    p = part[0]     # configured body part
                    which = part[1]     # current print index
                    space = part[2]     # number of placeholder spaces

                    # check if current index is inbound
                    if 0 <= which < len(p):
                        print(p[which], end="")
                        print(" " * bet, end="")
                        didPrint = True
                    else:

                        print(" " * space, end="")
                        print(" " * bet, end="")
                    part[1] += 1
                print()     # advance the print marker to the next line

        def configurePart(element):
            """
            It checks if the given element had been
            removed. If so it splits it into several lines otherwise
            returns empty string.
            Removed all leading spaces from front and end of all the
            lines.
            element: the name of the body part.(str)
            """
            lines = ("" if element in missing_parts
                        else self.BODY_ELEMNTS[element]).split("\n")
            return self.removeLeadingSpace(lines)
        
        # Prepration phase before printing.
        # ---------- HEAD ----------
        # check if any of the facial elements where removed!
        eye = (self.HEAD_PARTS["blind_eye"]
               if "eye" in missing_parts
               else self.HEAD_PARTS["eye"])
        mouth = (self.HEAD_PARTS["sad"]
                 if isSad
                 else self.HEAD_PARTS["smile"])
        head = ("" if "head" in missing_parts
                else self.HEAD_PARTS["head"].format(eye, eye, mouth))
        # ---------- ARMS ----------
        # check if elements of hands where removed.
        # replacing it with empty string instead.
        left_arm = configurePart("left arm")
        right_arm = configurePart("right arm")
        # ---------- BODY ----------
        body = configurePart("main body")
        # ---------- HANDS ----------
        left_hand = configurePart("left hand")
        right_hand = configurePart("right hand")
        # ---------- LEGS ----------
        left_leg = configurePart("left leg")
        right_leg = configurePart("right leg")
        # ---------- FEET ----------
        left_foot = configurePart("left foot")
        right_foot = configurePart("right foot")

        # printing body elements
        head = self.indentLines(head, 12)   # indent each line 12 spaces
        print(head)
        # Note: follow these guidelines to create a prepared body
        # print list.
        # printing list prepares each round of body parts
        # for printing.
        # [configured body part, current_line_index, replacement_spaces]
        # configuted body part:
        # refers to the list of lines the body part has.
        # current_line_index:
        # the current index that should be removed.
        # Note: if the index is out of bounds, it will only
        # be advanced and instead " " * replacement_spaces
        # will be printed until a inbound index is reached.
        # replacement_spaces:
        # number of spaces to be printed when there is body element
        # line to print. 
        body_print_list = [[left_hand, -1, 3], [left_arm, 0, 12],
                           [body, 0, 9], [right_arm, 0, 12],
                           [right_hand, -1, 3]]
        # printing upper body
        printBodyAcross(0, body_print_list, 0)
        # printing lower body
        body_print_list = [[left_leg, 0, 3], [right_leg, 0, 3]]
        printBodyAcross(14, body_print_list, 5)
        # printing the feet
        body_print_list = [[left_foot, 0, 3], [right_foot, 0, 3]]
        printBodyAcross(14, body_print_list, 5)

        self.printPlayerMessage(isSad)


def clear_all_playing_records():
    with open("player/playingRecord.json", 'w') as file:
        json.dump({"Total Player": 0}, file, indent=4)


clear_all_playing_records()