#######################################################################
# Coder: Amir
# Last date modified: 1/15/2026 
#######################################################################
""" Defines the game handler class. Game handler allows for 
generalization of all the games so that their rules, and results
are handled the same. way.
"""
#######################################################################


class GameHandler:
    
    def __init__(self, characters, gameData, name):
        """ characters: the list of characters that will participate.
        They all inherit from Character class. (list)
        gameData: the shared data among game handler and the
                  character classes. (unknown)
        name: the name of the game.(str)
        """
        self.characters = characters
        self.gameData = gameData
        self.name = name
        # provide each character access to the game data
        for character in self.characters:
            character.setGameData(gameData)

    def run(self):
        """ execute this method and the game will start.
        This is the only method that you should call
        from any game handler.
        """
        pass
