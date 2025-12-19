
class GameHandler:
    
    def __init__(self, characters, gameData):
        """
        characters is a list of all the players 
        that will play the game. The acutal human player
        must alwayse be at index 0.
        """
        self.characters = characters
        self.gameData = gameData
        # provide each character access to the game data
        for self.character in self.characters:
            self.character.setGameData(gameData)

    def run(self):
        """
        execute this method and the game will start.
        """
        