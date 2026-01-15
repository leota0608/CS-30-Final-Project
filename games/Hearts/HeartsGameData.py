###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
""" HeartsGameData is a class that defines all information the game handler
and every bot need to have access to. This object of this class is globally
shared with both game handler and bots, and it is up to the characters and
game handler to ensure correct usage."""
###############################################################################


class HeartsGameData:
    def __init__(self):
        # cards is a dictionary that defines the cards of every player
        # in this structure:
        # {player name: {suit: [list of cards with that suit], ...}, ...}
        self.cards = dict()
        # it is list of cards currently played.
        # table is flushed after every round.
        self.table = list()
        # a dictionary in the form of
        # {player name: score, ...} that stores the player's
        # scores.
        self.scores = dict()
        # it is the index of player that will start the game.
        # it points to the list of Player objects held by
        # game handler.
        self.starter_player = None
