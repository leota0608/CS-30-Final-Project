from games.EndPhase.EndPhaseGame import EndPhaseGame
from games.BlackJack.BlackJackGame import BlackJackGame
from games.CourtPiece.CourtPieceGame import CourtPieceGame # game3 
from games.Hearts.HeartsGame import HeartsGame # game4
from player.player import Player
from games.EndPhase.choose import choose
from player.shop import Shop
import random
import os
import time


class Game:
    def __init__(self):
        self.player = Player()
        self.shop = Shop(self.player)
        self.greeting()
        self.player.get_name()
        self.player.store_player_information()
        # load the four games after loading player infoamtion because init in game will generate error 
        # if no player information has been stored yet
        self.game1 = EndPhaseGame(self.player) # 3 players, 4 initial health
        self.game2 = BlackJackGame(self.player) # 3 players
        self.game3 = CourtPieceGame(self.player)#, 1000)
        self.game4 = HeartsGame(self.player)#, 10000)
        self.run()
        
    def greeting(self):
        # print greetings
        print("Hello...")
        '''
        Tell the player about the story, background.
        Greet the player.
        Maybe read .json files for previous data to let the player have a general idea of the difficulty of the game.
        '''

    def run(self):
        print("Game starts")
        # game1
        self.lobby(1)
        self.load_game_anim(self.game1.name)
        self.game1.run()
        self.player.update_score()

        self.lobby(2)
        # game2
        self.load_game_anim(self.game2.name)
        self.game2.run()
        self.player.update_score()
        
        self.lobby(3)
        # game3
        self.load_game_anim(self.game3.name)
        self.game3.run()
        self.player.update_score()
        
        self.lobby(4)
        # game4
        self.load_game_anim(self.game4.name)
        self.game4.run()
        self.player.update_score()
        
    def lobby(self, num):
        choice = None
        while choice != 3:
            choice = int(choose(f"You are in the lobby...\n1. Shop\n2. Check self\n3. Proceed to game {num}\nChoice: ", ['1', '2', '3']))
            if choice == 1:
                self.shop.buy()
            elif choice == 2:
                os.system("cls")
                self.player.printBodyShape()
                time.sleep(0.7)
                input("\rpress any key to continue...")
                os.system("cls")


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


game = Game()