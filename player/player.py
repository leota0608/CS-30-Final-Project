###############################################################################
# Coder: Leo
# Last date modified: 1/14/2026
###############################################################################
"""This module is the player module. It contains the Player class, 
which stores all information of the player"""
###############################################################################
import random
from datetime import date
import json
import time


class Player:
    """This class is the player class, which has all the information
    of the player and stores them in an external file.
    It also prints all the body parts of the player as well as reads 
    player name, store date, score, money, lost body parts, result of 
    each game."""
    # These are the body parts to be printed
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
        "sad": "┌─────┐"
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
|||"""}

    def __init__(self):
        self.date = date.today()
        self.score = 0
        self.money = 0
        self.debt = 0
        self.lost_body_parts = []
        try:  # read player information from previously stored file
            with open("player/PlayerStarterData.json", 'r') as content:
                data = json.load(content)
                self.bodyParts = data["bodyParts"]
                self.probability = data["probability"]
                self.money = data["current money"]
                self.debt = data["debt"]
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
        """This method lets the player input their name and 
        store them in self.name"""
        while True:
            string = input("Write down your name: ")
            confirm = input("Is this really your name?(y/n)")
            if (confirm.lower() == "y" or confirm.lower() == "yes"):
                self.name = string
                return

    def store_player_information(self):
        """This method stores player information in an 
        external file."""
        # Add player information to existing records
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
        record[str(total_num + 1)] = {"Name": self.name,
                                      "Date": str(self.date),
                                      "Score": self.score,
                                      "Game record": {"Game 1": None,
                                                      # win/lose: True/False
                                                      "Game 2": None,
                                                      "Game 3": None,
                                                      "Game 4": None},
                                      "Lost body parts": []}
        try:
            with open("player/playingRecord.json", 'w') as file:
                json.dump(record, file, indent=4)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json")
        except:
            print("Failed to open playingRecord.json for some "
                  "unknown reason.")

    def store_game_result(self, game_num, result):
        """This method stores game result of each game after the
        player finishes it."""
        # store information in playingRecord.json
        try:
            with open("player/playingRecord.json", 'r') as file:
                record = json.load(file)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json")
        except:
            print("Failed to open playingRecord.json")
        record[str(record["Total Player"])]["Game record"]\
            [f"Game {game_num}"] = result
        try:
            with open("player/playingRecord.json", 'w') as file:
                json.dump(record, file, indent=4)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json")
        except:
            print("Failed to open playingRecord.json "
                  "for some unknown reason")

    def update_score(self):
        """This method update the score of the player according to
        the game results."""
        # update score in playingRecord.json
        try:
            with open("player/playingRecord.json", 'r') as file:
                record = json.load(file)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json for some "
                "unknown reason")
        except:
            print("Failed to open playingRecord.json")
        for i, j in record[str(record["Total Player"])]["Game record"]. \
                items():
            if j == True:
                record[str(record["Total Player"])]["Score"] += 25
        try:
            with open("player/playingRecord.json", 'w') as file:
                json.dump(record, file, indent=4)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json")
        except:
            print("Failed to open playingRecord.json\
                  for some unknown reason")

    def choose_body_part(self):
        """This method chooses a body part from the player
        randomly and returns the body part, which is a string"""
        r = random.randint(1, 1000)
        for i in range(0, len(self.probability)):
            if r <= self.probability[i]:
                if self.bodyParts[i] in self.lost_body_parts:
                    self.choose_body_part()
                    break
                return self.bodyParts[i]

    def lose(self, body_part):
        """This method removes the players body part and update 
        it to playingRecord.json.
        body_part is a string perimeter"""
        self.lost_body_parts.append(body_part)
        try:
            with open("player/playingRecord.json", 'r') as file:
                record = json.load(file)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json")
        except:
            print("Failed to open playingRecord.json\
                  for some unknown reason")
        record[str(record["Total Player"])]["Lost body parts"]. \
            append(body_part)
        # save changes to playerRecord.json
        try:
            with open("player/playingRecord.json", 'w') as file:
                json.dump(record, file, indent=4)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json")
        except:
            print("Failed to open playingRecord.json for some "
                  "unknown reason")

    def gain(self, body_part):
        """This method adds a body part to the player and update
        any other changes"""
        self.lost_body_parts.remove(body_part)
        try:
            with open("player/playingRecord.json", 'r') as file:
                record = json.load(file)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json")
        except:
            print("Failed to open playingRecord.json\
                  for some unknown reason")
        record[str(record["Total Player"])]["Lost body parts"]. \
            remove(body_part)
        # save changes to playingRecord.json
        try:
            with open("player/playingRecord.json", 'w') as file:
                json.dump(record, file, indent=4)
        except FileNotFoundError:
            print("Failed to locate playingRecord.json")
        except:
            print("Failed to open playingRecord.json\
                  for some unknown reason")

    @staticmethod
    def indentLines(text: str, spaces):
        """This method makes indentations for printing body
        parts.
        text: a string that represents a body part.
              contains split lines. (str)
        spaces: number of spaces to add.(int)"""
        padding = " " * spaces
        return "\n".join(padding + line for line in text.splitlines())

    @staticmethod
    def removeLeadingSpace(lst):
        """ removes leading spaces from the list.
        it removes both from the end and beginning.
        lst: a list of strings.(list)
        ex:
        input: ["", "", "ddd", "dddd", " ", "ddd", " ", " "]
        output: ["ddd", "dddd", " ", "ddd"]
        """
        # Find first non-empty string
        start = 0
        while start < len(lst) and lst[start] == "":
            start += 1
        # Find last non-empty string
        end = len(lst) - 1
        while end >= 0 and lst[end] == "":
            end -= 1
        # Slice the list
        return lst[start:end + 1] if start <= end else []

    def printPlayerMessage(self, isSad):
        """ prints a message describing player's
        situation.
        isSad: true or false, weather they are sad or not.(bool)
        """
        print(f"my name is {self.name}")
        if isSad:
            print("I am not feeling good.")
            print("I have lost", end="")
            for part in self.lost_body_parts:
                print(", " + part, end="")
            print(".")
            print("you know ", end="", flush=True)
            time.sleep(1)
            print("it hurts so much.")
            print("please help me.")
            print("please ...")
        else:
            print("I am very happy little kid.")
            print("Let's crush this game.")

    def addMoney(self, add):
        """ adds money to the current player.
        """
        self.money += add

    def printBodyShape(self):
        """ prints the shape of the player's
        body.
        """
        missing_parts = self.lost_body_parts
        isSad = len(self.lost_body_parts) != 0
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
                    p = part[0]  # configured body part
                    which = part[1]  # current print index
                    space = part[2]  # number of placeholder spaces

                    # check if current index is inbound
                    if 0 <= which < len(p):
                        print(p[which], end="")
                        print(" " * bet, end="")
                        didPrint = True
                    else:
                        print(" " * space, end="")
                        print(" " * bet, end="")
                    part[1] += 1
                print()  # advance the print marker to the next line

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
        # Preparation phase before printing.
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
        head = self.indentLines(head, 12)  # indent each line 12 spaces
        print(head)
        # Note: follow these guidelines to create a prepared body
        # print list.
        # printing list prepares each round of body parts
        # for printing.
        # [configured body part, current_line_index, replacement_spaces]
        # configured body part:
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


# This function clears all playing records if there are too much
def clear_all_playing_records():
    """ clears playing records.
    """
    try:
        with open("player/playingRecord.json", 'w') as file:
            json.dump({"Total Player": 0}, file, indent=4)
    except FileNotFoundError:
        print("Failed to locate playingRecord.json")
    except:
        print("Failed to open playingRecord.json for some\
              unknown reason")


clear_all_playing_records()
