from games.game1.main import Game1
from games.game2.main import Game2
from games.game3.CourtPiece import CourtPiece # game3 
from games.game4.Hearts import Hearts # game4
from player.player import Player
import random
import time
import os
# the imports assumes that there are four classes named Game1-4 in the four py files
class Game:
    def __init__(self):
        self.player = Player()

        self.test_game(2) # testing

        self.greeting()
        self.player.get_name()
        self.player.store_player_information()
        # load the four games after loading player infoamtion because init in game will generate error 
        # if no player information has been stored yet
        self.game1 = Game1(self.player) # 3 players, 4 initial health
        self.game2 = Game2(self.player) # 3 players
        self.game3 = CourtPiece(self.player, 1000)
        self.game4 = Hearts(self.player, 10000)
        self.run()
        self.ending()
        
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
        self.load_game_anim(1)
        self.game1.run()

        # game2
        self.load_game_anim(2)
        self.game2.run()
        self.player.store_game_result(2, self.game2.result)
        self.player.update_score()
        # if(self.game2.result):
        #     print("You successfully passed game 2")
        #     input("Press any key to proceed to game 3...")
        # else:
        #     ############################################################### animiation example 
        #     print("You failed to pass game 2\nReceive your punishment!")
        #     body_part = self.player.choose_body_part()
        #     self.player.lose(body_part)
        #     self.choose_body_part_anim(body_part) # This part should should be dealt with in each individual game
        #     time.sleep(2)
        #     self.screen_flickering_anim(body_part)
        #     print(f"You lost your {body_part}...")
        #     print("You are forced into game 3...")
        #     ################################################################

        # game3
        self.load_game_anim(3)
        self.game3.run()
        
        # game4
        self.load_game_anim(4)
        self.game4.run()
        

    def ending(self):
        print("Goodbye, be alive")
        '''
        1. give a list of options for the player to choose:
            - start game
            - view self
            - open store
        2. after player start game, there is no stopping, differerent games will be called,
            ex: self.game1.start() 
            And the the mini game will run
            After it ends, there will be a return value of win or lost, and corresponding actions will be taken:
                - Receive awards for winning
                - Lose some random body parts
                (These two actions will be then update to the player object)
        '''

    def load_game_anim(self, num):
        load = 0
        while load < 100:
            progress = random.randint(10, 20)
            load += progress
            if load > 100:
                load = 100
            print(f"\rLoading game {num}: [{load}%]", end='', flush = True)
            time.sleep(random.randint(50, 80)/100)
        print(f"\rGame {num} successfully loaded...")


    def test_game(self, num):
        if num == 1:
            game = Game1(self.player)
        if num == 2:
            game = Game2(self.player)
        game.run()

game = Game()


