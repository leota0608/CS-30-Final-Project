
class Character:
    def __init__(self, name):
        self.gameData = None
        self.name = name

    def setGameData(self, gameData):
        """ GameHander will provide gameData for each
        player through this method.
        """
        self.gameData = gameData

    def provoke(self, action):
        """ triggers the character to return the
        next move in the game. 
        Note: The return datatype of provoke is 
        not resctrcited and it must be communicated
        between GameHandlers and the each player
        before development.
        """
        pass
