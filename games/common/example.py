"""
This is just an illustration of how to use
the GameHandler and Character classes correctly
and efficiently.
"""
from GameHandler import GameHandler

class Player:
    def __init__(self):
        self.name = ""
        self.age = 0

    def getName(self):
        self.name = input("What is your name? ")
    
    def getAge(self):
        self.age = int(input("What is your age? "))


class RPSGame(GameHandler):
    def __init__(self, characters, runs):
        GameHandler.__init__(self, characters)
        self.runs = runs
        self.gameData = []

    def run(self):
        for i in range(self.runs):

            self.gameData.append([])

            user_answer = self.characters[0].provoke()
            self.gameData[-1].append(user_answer)
            computer_answer = self.characters[1].provoke()
            self.gameData[-1].append(user_answer)

            if user_answer == "s":
                if computer_answer == 'r':
                    print("Ah, computer won")
                else:
                    print("Let's go humanity")
            
            elif user_answer == "r":
                if computer_answer == "p":
                    print("you loser!")
                else:
                    print("You won!")

            elif user_answer == "p":
                if computer_answer == "s":
                    print('AI won')
                else:
                    print("Computer Lost")

            message = self.characters[1].sendMessage()



    