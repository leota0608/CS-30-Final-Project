###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026 
###############################################################################
""" Defines the supreme class for all players. It includes 
human player interfaces and bot classes. Ensure to read the 
docstring carefully and implement each method according to 
the design.
"""
###############################################################################


class Character:
    """ the parent class of all objects that play a game.
    You must implement the provoke method, as well as the different actions
    you are expected to respond to.
    """
    def __init__(self, name):
        """
        name: It is the name of the character. A unique identifier     
        in the game(string)
        """
        self.gameData = None
        self.name = name

    def setGameData(self, gameData):
        """ GameHandler will provide gameData for each
        player through this method.
        gameData: a reference to the object that represent
        all the data in the game. (Type is unknown)
        """
        self.gameData = gameData

    def provoke(self, action):
        """ triggers the character to return the
        next move in the game. 
        Note: The return datatype of provoke is 
        not restricted, and it must be communicated
        between GameHandlers and players
        before development.
        action: a parameter to notify the current player about
        the current state of the game.(string or int)
        """
        pass
