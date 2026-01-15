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
        self.lines = None
        self.loadDoc(fileName)
        self.options = ["(WORD):", "(LETTER):", "(SENTENCE):", "(NORMAL):"]

    def loadDoc(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                self.lines = lines
        except:
            print(f"Failed to load {filename}")

    @staticmethod
    def printList(list_, delay, bet=""):
        for i in range(len(list_)):
            w = list_[i]
            print(w, end="", flush=True)
            if i < len(list_) - 1:
                print(bet, end="", flush=True)
            tm.sleep(delay)

    def display(self):
        current_mode = None
        word_delay = 0
        stop = False

        for line in self.lines:
            # remove the last \n from the character
            if line[:-1] in self.options:
                current_mode = line[:-1]
            else:
                if line[:2] == "**":
                    delay = float(line[2:])
                    tm.sleep(delay)
                elif line[:2] == "$$":
                    input("Hit Enter to continue> ")
                elif line[:2] == "$%":
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
                    word_delay = float(line[1:])
                else:
                    if current_mode == "(WORD):":
                        words = line.split(' ')
                        self.printList(words, word_delay, ' ')
                    elif current_mode == "(LETTER):":
                        self.printList(line, word_delay)
                    elif current_mode == "(SENTENCE):":
                        sentences = line.split('.')
                        self.printList(sentences, word_delay)
                    elif current_mode == "(NORMAL):":
                        print(line, end="")
