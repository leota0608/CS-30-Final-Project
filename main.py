from games.game1.main import Game1
from games.game2.main import Game2
from games.game3.main import Game3
from games.game4.main import Game4
from player.player import Player
import random
import time
import os
# the imports assumes that there are four classes named Game1-4 in the four py files
class Game:
    def __init__(self):
        

        self.game1 = Game1()
        self.game2 = Game2(3) # 3 players
        self.game3 = Game3()
        self.game4 = Game4()
        self.player = Player()
        self.greeting()
        self.player.get_name()
        self.player.store_player_information()
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
        if(self.game1.result):
            pass
        # game2
        self.load_game_anim(2)
        self.game2.run()
        if(self.game2.result):
            print("You successfully passed game 2")
            input("Press any key to proceed to game 3...")
        else:
            print("You failed to pass game 2\nReceive your punishment!")
            
            body_part = self.player.choose_body_part()
            self.player.lose(body_part)
            self.choose_body_part_anim(body_part)
        # game3
        self.load_game_anim(3)
        self.game3.run()
        if(self.game3.result):
            pass
        # game4
        self.load_game_anim(4)
        self.game4.run()
        if(self.game4.result):
            pass

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

    def choose_body_part_anim(self, body_part):
        t = 0.3
        dt = 0.025
        last_output = None
        for i in range(32):
            choice = random.choice(self.player.bodyParts)
            while choice  == last_output:
                choice = random.choice(self.player.bodyParts)
            print(f"\rChoosing body parts: [{choice}]{' '*100}", end='', flush = True)
            last_output = choice
            time.sleep(t)
            if t < 0.05:
                dt*=-1
            t-=dt
        print(f"\rChoosing body parts: [{body_part}]{' '*100}")


game = Game()