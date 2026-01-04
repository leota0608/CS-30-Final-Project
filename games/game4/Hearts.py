from games.common.GameHandler import GameHandler


class Hearts(GameHandler):
    def __init__(self, characters, gameData):
        super().__init__(characters, gameData)
        self.result = False

    def run(self):
        print("game4 starts")

