###############################################################################
#Title: Death Game
#Class: CS 30
#Assignment: final project
#Coder: Leo, Amir
#Last date modified: 6/18/2025
###############################################################################
'''
This is the CS 30 final project main code.
It imports the four mini game modules and runs the game,
The code mainly includes Game class, which run the game.
'''
###############################################################################
from games.EndPhase.EndPhaseGame import EndPhaseGame
from games.BlackJack.BlackJackGame import BlackJackGame
from games.CourtPiece.CourtPieceGame import CourtPieceGame # game3 
from games.Hearts.HeartsGame import HeartsGame # game4
from player.player import Player
from games.teller.Teller import Teller
from games.EndPhase.choose import choose
from player.shop import Shop
import random
import os
import time


class Game:
    def __init__(self):
        self.player = Player()
        self.shop = Shop(self.player)
        self.story = Teller("gameStory.txt")

        self.lobby_options = ["body shop", "check self",
                              "check money", "play game",
                              "leave arcade"]
        self.play_game_options = ["End Phase", "Black Jack",
                                  "Court Piece", "Hearts",
                                  "exit"]

        self.games = {"End Phase": EndPhaseGame,
                      "Black Jack": BlackJackGame,
                      "Court Piece": CourtPieceGame,
                      "Hearts": HeartsGame}

    def greeting(self):
        # print greetings
        self.story.display()
    
    def runGame(self, gameName, money):
        print("Game starts")
        # game1
        game = self.games[gameName](self.player, money)
        self.load_game_anim(game.name)
        game.run()
        self.player.update_score()

    def printOptions(self, options):
        for i in range(len(options)):
            print(f"{i + 1}. {options[i]}")

    def printMoney(self):
        print("Hi, I am your ecountant.")
        print("currently: ")
        print(f"your money: {self.player.money}")
        print(f"amount you must pay: {self.player.debth}")

    def handlePlayGame(self):
        print("ok, soo you wanna play a game ...")
        time.sleep(1)
        print()

        self.printOptions(self.play_game_options)
        
        while True:
            choice = input("Which game do you wanna play> ")
            try:
                choice = self.play_game_options[int(choice) - 1]
            except (TypeError, ValueError):
                print("You must enter a number idiot. Sorry for the language.")
            except IndexError:
                print("Your option is literaly nonexistent.")
            else:
                if choice == "exit":
                    print("Oh, I see, you are afraid like hell!")
                    print("Going back to the lobby in (3) seconds.")
                    time.sleep(3)
                    break
                else:
                    confirm = choose(f"Are you sure you wanna play {choice}?(y/n)", ["yes", 'y', "no", 'n'])
                    if confirm in ["yes", 'y']:
                        money = random.randint(2000, 6000)
                        print(f"If you win, you can get up tp ${money}")
                        time.sleep(0.7)
                        self.runGame(choice, money)
                        break

    def checkEnd(self):
        if self.player.money >= self.player.debth:
            print()
            print("Wow ....")
            print("You paid off the denth.")
            print(f"you made {self.player.money} and your denth was {self.player.debth}")
            print(f"you will keep {self.player.money - self.player.debth}")
            print("Congrats anyway, you bought your life.")
            print("Now get out ...")
            time.sleep(2)
            print()
            return True
        elif "head" in self.player.lost_body_parts:
            print()
            print("ehhhhhhhhhhhh")
            print("you lost your big ugly head.")
            print("you are now a dead pumpkin.")
            print("RIP")
            time.sleep(2)
            print("we are going to take out all of your parts and sell them!")
            return True
        else:
            print(f"you still need to pay something like {self.player.debth - self.player.money}.")
            print("go on.")
            print()
            return False

    def lobby(self):
        while True:
            self.printOptions(self.lobby_options)
            print()
            choice = input("do something(choose the number)> ")
            try:
                choice = self.lobby_options[int(choice) - 1]
            except (TypeError, ValueError):
                print("Error: Hey enter a number for your choice.")
            except IndexError:
                print("Error: Listen, this choice does exist, out of bounds.")
            else:
                if choice == "body shop":
                    os.system("cls")
                    self.shop.buy()
                    os.system("cls")
                elif choice == "check self":
                    os.system("cls")
                    self.player.printBodyShape()
                    time.sleep(0.7)
                    input("\rpress any key to continue...")
                    os.system("cls")
                elif choice == "check money":
                    self.printMoney()
                    input("\rpress any key to continue...")
                elif choice == "play game":
                    os.system("cls")
                    self.handlePlayGame()
                    os.system("cls")
                    if self.checkEnd():
                        break
                elif choice == "leave arcade":
                    print("you have not still paid your money.")
                    time.sleep(2)
                    print("We would just kill you and then sell your body for your debt.")
                    print("Listen, we have no sympathy we only care about money!")
                    choice = choose("Do you really want that>(y/n)", ["yes", 'y', "no", 'n'])
                    if choice == "y":
                        print("Ok, you bastard.")
                        print("we gonna chop of everything.")
                        print("RIP")
                        time.sleep(2)
                        break
                    else:
                        print("contiue your game and do not come here again.")

                    
    def load_game_anim(self, name: str):
        load = 0
        while load < 100:
            progress = random.randint(10, 25)
            load += progress
            if load > 100:
                load = 100
            print(f"\rLoading {name}: [{load}%]", end='', flush = True)
            time.sleep(random.randint(50, 80)/100)
        print(f"\r{name.capitalize()} successfully loaded...")
        time.sleep(0.7)
        print(f"\r{name.capitalize()} starts ... Good luck...")
        time.sleep(2)

    def run(self):
        self.greeting()
        self.player.get_name()
        self.player.store_player_information()
        self.lobby()

if __name__ == "__main__":
    game = Game()
    game.run()