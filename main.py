from games.game1.main import Game1
from games.game2.main import Game2
from games.game3.main import Game3
from games.game4.main import Game4
# the imports assumes that there are four classes named Game1-4 in the four py files
class Game:
    def __init__(self):
        self.game1 = Game1()
        self.game2 = Game2()
        self.game3 = Game3()
        self.game4 = Game4()
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
        self.game1.run()
        if(self.game1.result):
            pass
        # game2
        self.game2.run()
        if(self.game2.result):
            pass
        # game3
        self.game3.run()
        if(self.game3.result):
            pass
        # game4
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


game = Game()
game.greeting()
game.run()
game.ending()