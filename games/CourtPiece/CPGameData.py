###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
"""This module contains the class CPGameData, it is imported by 
CourtPieceGame.py, and it defines all information the game-handler
adn bot has access to."""
###############################################################################


class CPGameData:
    """ CPGameData is a class that defines all information the 
    game handler and every bot need to have access to. This object 
    of this class is globally shared with both game handler and bots, 
    and it is, up to the characters and game handler to ensure 
    correct usage."""
    def __init__(self):
        # a string that represents the suit that has been chosen
        # as the trump.
        self.trump = None
        # A Player class object pointing to the king.
        self.king = None
        # index of the last player who won a round
        self.last_winner_ind = None
        # table is a list of cards played on order in every round.
        self.table = []
        # cards is a dictionary that defines the cards of every player
        # in this structure:
        # {player name: {suit: [list of cards with that suit], ...}, ...}
        self.cards = dict()
        # a dictionary in the form of
        # {player name: score, ...} that stores the player's
        # scores.
        self.scores = dict()
