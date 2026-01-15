###############################################################################
# Coder: Amir
# Last date modified: 1/14/2026
###############################################################################
""" Creates a teller class that can narrate a story or rules of the
game to user instead of just dumping the text into the terminal."""
###############################################################################
import time as tm


class Teller:
    """
    Teller tells a story to the user based on the format
    outlined in a separate file. After constructing an object
    run the file using the "display" method.

    To specify the method of print use any of the following
    headers.
    "(WORD):"->used to print the text word by word
    "(LETTER):"->used to print the text letter by letter.
    "(SENTENCE):"->prints the text sentence by sentence.
    "(NORMAL):"->only prints the text
    All these headers except (NORMAL): must be followed by
    a number that starts with *. It specifies the delay in
    printing.

    in order to enforce the user to hit enter to continue, use
    the symbol $$ on its own line. It causes a message saying
    "Hit Enter to continue>" to be displayed.

    To ask the user if they want to continue or not use the symbol
    $% on its own line.

    You can also put delays between sentences. Use "**" followed
    by the delay number on its own line to cause a delay.

    Please look at the sample documents to see how to use this class.
    """

    def __init__(self, fileName):
        """ filename: the filename of a file that readable by the
        Teller class. It means that the file follows teller syntax. (str)
        """
        self.lines = None
        self.loadDoc(fileName)
        self.options = ["(WORD):", "(LETTER):", "(SENTENCE):", "(NORMAL):"]

    def loadDoc(self, filename):
        """ loads the file and reads it line by line.
        then stores it in "self.lines" for reading.
        filename: the name of the file to read.(str)
        """
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.lines = lines

    @staticmethod
    def printList(list_, delay, bet=""):
        """ prints a given list of strings, with a given delay
        in between printing each element. After each string element
        is printed a spacer known as bet is printed.
        list_: list of string elements. (list)
        delay: the delay between each element. (float/int)
        bet: optional argument. By default, is empty string but
        can be set other strings. (str)
        """
        for i in range(len(list_)):
            w = list_[i]
            print(w, end="", flush=True)
            if i < len(list_) - 1:
                print(bet, end="", flush=True)
            tm.sleep(delay)

    def display(self):
        """ displays the Teller file to the user. Reads
        each line individual line one by one and preforms
        the instructions.
        """
        # mode is any of
        # (WORD): print word by word
        # (LETTER): print letter by letter
        # (SENTENCE): print sentence by sentence
        # (NORMAL): print normally as a whole
        current_mode = None
        # delay between printing.
        # ex: a word_delay of 0.1 with current_mode set to (LETTER)
        # means that we print each letter one after the other every 0.1sec.
        word_delay = 0
        # should we end the teller
        stop = False

        for line in self.lines:
            # remove the last \n from the line
            if line[:-1] in self.options:
                # it a mode
                current_mode = line[:-1]
            else:
                # special string cases
                if line[:2] == "**":
                    # universal delay.
                    # places a pause in display
                    delay = float(line[2:])
                    tm.sleep(delay)
                elif line[:2] == "$$":
                    # engages the user in hitting enter.
                    input("Hit Enter to continue> ")
                elif line[:2] == "$%":
                    # asks the user if they want to quit and end display
                    while True:
                        ans = input("Do you want to continue(Y/n)> ")
                        if ans == "Y":
                            break
                        elif ans == "n":
                            stop = True
                            break
                        else:
                            print("Invalid input.")
                    if stop:
                        break
                elif line[:1] == "*":
                    # set the mode delay
                    word_delay = float(line[1:])
                else:
                    # handling modes
                    if current_mode == "(WORD):":
                        # print word by word and thus
                        # split by ' '
                        words = line.split(' ')
                        self.printList(words, word_delay, ' ')
                    elif current_mode == "(LETTER):":
                        # just pass the line since the
                        # printList will enumerate it letter by letter.
                        self.printList(line, word_delay)
                    elif current_mode == "(SENTENCE):":
                        # split by sentence.
                        sentences = line.split('.')
                        self.printList(sentences, word_delay)
                    elif current_mode == "(NORMAL):":
                        # just print it.
                        # no fancy styling!
                        print(line, end="")
