
class Character:
    def __init__(self):
        pass

    def setGameData(self, gameData):
        self.gameData = gameData

    def provoke(self):
        """ triggers the character to return the
        next move in the game. 
        Note: The return datatype of provoke is 
        not resctrcited and it must be communicated
        between GameHandlers and the each player
        before development.
        """
        pass

    def sendMessage(self):
        """ Sends an engaging message after each move
        based on the status of the game.
        If no message exist returns None.
        """
        pass


