from games.game1.choose import choose
from games.common.format import Format
import time
format = Format()

def print_rules(anim):
    format.newline()
    with open("games/game1/rules1.txt", 'r') as rules:
        text = rules.read()
    if not anim:
        print(text)
    else:
        space1 = 0
        space2 = 0
        newline = 0
        while space2 < len(text)-1 and space2 >= 0:
            space2 = text.find(' ', space1)
            newline = text.find("\n", space1)
            if space2 == -1:
                space2 = len(text)-1
            if newline == -1:
                newline = 666666
            if newline < space2:
                print(text[space1:newline+1], end='', flush = True)
                space1 = newline+1
            else:
                print(text[space1:space2+1], end='', flush = True)
                space1 = space2+1
            time.sleep(0.05)
    format.newline()
    input("Press any key to continue...") 

def print_card_description(anim):
    format.newline()
    with open("games/game1/rules2.txt", 'r') as rules:
        text = rules.read()
    if not anim:
        print(text)
    else:
        space1 = 0
        space2 = 0
        newline = 0
        while space2 < len(text)-1 and space2 >= 0:
            space2 = text.find(' ', space1)
            newline = text.find("\n", space1)
            if space2 == -1:
                space2 = len(text)-1
            if newline == -1:
                newline = 666666
            if newline < space2:
                print(text[space1:newline+1], end='', flush = True)
                space1 = newline+1
            else:
                print(text[space1:space2+1], end='', flush = True)
                space1 = space2+1
            time.sleep(0.05)
    format.newline()
    input("Press any key to continue...")
    

valid_choices = []
valid_choices.append("q")
valid_choices.append("w")
choice = choose("Choice: ", valid_choices)
while choice == 'q':
    print_rules(False)
    for i in range(18):
        print("\033[A\033[2K", end='')
    choice = choose("Choice: ", valid_choices)

while choice == 'w':
    print_card_description(False)
    for i in range(25):
        print("\033[A\033[2K", end='')
    choice = choose("Choice: ", valid_choices)