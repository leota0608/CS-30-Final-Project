import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from CourtPiece import CourtPiece

game = CourtPiece(CourtPiece.QUADRUPLE_PLAY, ["Ali", "Bagher", "Karim", "Mossa"])
game.run()
