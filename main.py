###############################################################################
# Title: Death Game
# Class: CS 30
# Assignment: final project
# Coder: Leo, Amir
# Last date modified: 1/18/2025
###############################################################################
""" This is the CS 30 final project main code.
It imports the four mini-game modules and runs the game,
The code mainly includes Game class, which run the game.
"""
###############################################################################
from games.EndPhase.EndPhaseGame import EndPhaseGame
from games.BlackJack.BlackJackGame import BlackJackGame
from games.CourtPiece.CourtPieceGame import CourtPieceGame  # game3
from games.Hearts.HeartsGame import HeartsGame  # game4
from player.player import Player
from games.teller.Teller import Teller
from games.EndPhase.choose import choose
from player.shop import Shop
import random
import os
import time


class Game:
    """The game class  runs the entire game, it contains four
    mini-game objects, a shop object and ap layer object.
    It prints the rules and give instructions to player to 
    play the game."""

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
        """This method prints greetings for player"""
        self.story.display()

    def runGame(self, gameName, money):
        """This method runs one of the four games according to 
        the two perimeters:
        gameName is a string indicating the name of the game.
        money is an integer which is the maximum reward the
        player can get finishing the game. """
        print("Game starts")
        # game1
        game = self.games[gameName](self.player, money)
        self.load_game_anim(game.name)
        game.run()
        self.player.update_score()

    @staticmethod
    def printOptions(options):
        """This method prints options for the player to choose.
        options is a list of strings to be printed."""
        for i in range(len(options)):
            print(f"{i + 1}. {options[i]}")

    def printMoney(self):
        """This method outputs the money the player has and the debt
        he has to pay."""
        print("Hi, I am your acountant.")
        print("currently: ")
        print(f"your money: {self.player.money}")
        print(f"amount you must pay: {self.player.debt}")

    def handlePlayGame(self):
        """This method lets the player choose which game 
        he wants to play. After choosing, it calls runGame
        to start the game accordingly."""
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
                print("Your option is literally nonexistent.")
            else:
                if choice == "exit":
                    print("Oh, I see, you are afraid like hell!")
                    print("Going back to the lobby in (3) seconds.")
                    time.sleep(3)
                    break
                else:
                    confirm = choose(f"Are you sure you wanna play "
                                    f"{choice}?(y/n)", ["yes", 'y', "no", 'n'])
                    if confirm in ["yes", 'y']:
                        money = random.randint(2000, 6000)
                        print(f"If you win, you can get up to ${money}")
                        time.sleep(0.7)
                        self.runGame(choice, money)
                        break

    def checkEnd(self):
        """This method checks if the player has earn enough 
        money to pay his debt, or if the player got his head cut off.
        """
        if self.player.money >= self.player.debt:
            print()
            print("Wow ....")
            print("You paid off the debt.")
            print(f"you made {self.player.money} and your debt was"
                  "{self.player.debt}")
            print(f"you will keep {self.player.money - self.player.debt}")
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
            print(f"you still need to pay something like "
                  f"{self.player.debt - self.player.money}.")
            print("go on.")
            print()
            return False

    def lobby(self):
        """This method is the lobby, which is where the player goto
        after finishing a game. The player can then choose to his
        next moves."""
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
                    print("We would just kill you and then sell"
                          "your body for your debt.")
                    print("Listen, we have no sympathy we only care"
                          "about money!")
                    choice = choose("Do you really want that>(y/n)",
                                    ["yes", 'y', "no", 'n'])
                    if choice == "y":
                        print("Ok, you bastard.")
                        print("we gonna chop of everything.")
                        print("RIP")
                        time.sleep(2)
                        break
                    else:
                        print("Continue your game"
                              "and do not come here again.")

    def load_game_anim(self, name: str):
        """This methods loads the load-game animation, which a 
        percentage inside a pair of middle brackets."""
        load = 0
        while load < 100:
            progress = random.randint(10, 25)
            load += progress
            if load > 100:
                load = 100
            print(f"\rLoading {name}: [{load}%]", end='', flush=True)
            time.sleep(random.randint(50, 80) / 100)
        print(f"\r{name.capitalize()} successfully loaded...")
        time.sleep(0.7)
        print(f"\r{name.capitalize()} starts ... Good luck...")
        time.sleep(2)

    def run(self):
        """This method starts the game, greet the player, 
        read player's name and starts the game."""
        self.greeting()
        self.player.get_name()
        self.player.store_player_information()
        self.lobby()


# run the game
if __name__ == "__main__":
    game = Game()
    game.run()
