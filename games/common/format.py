###############################################################################
# Coder: Leo
# Last date modified: 1/14/2026
###############################################################################
"""This module is the format module. Right now it only contains one 
kind of formatting"""
###############################################################################


class Format:
    """This is the Format class which is used to help with formatting
    output."""

    def __init__(self):
        pass

    def newline(self):
        """This method outputs a new line made of '-' of a total of 30.
        It helps separate output to make it more clear."""
        for i in range(30):
            print("-", end='')
        print('')
