import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from games.common.character import Character
from games.common.format import Format
from games.game1.bot import Bot
from games.game1.choose import choose
from games.game1.human import Human
from games.game1.deck import Deck
from games.game1.card import Card
import time
import json
import random

with open("games/game1/card.json", 'r') as file:
    content = json.load(file)
    card = content["card"]
    card_nums = content["card nums"]

class Game1:
    def __init__(self, player_num, initial_health):
        self.running = True
        self.result = False
        self.card_nums = card_nums
        self.player = []
        self.player.append(Human(f"player1", initial_health, 0))
        for i in range(1, player_num):
            self.player.append(Bot(f"player{i+1}", initial_health, player_num - 1, i))
        self.initialise_deck()
        self.initialise_handcards()


    def run(self):
        print("Game1 starts")
        while self.running:
            if self.check_win():
                self.result = True
                break
            for i in range(len(self.player)):
                if not self.player[i].alive:
                    continue
                format.newline()
                # check alive theoretically, all deaths should be determined in nearly_dead before being detected here...but...
                # if self.player[i].health <= 0:
                #     print(f"Player {self.player[i].name} died...")#enemy_num-1
                #     self.nearly_dead(i)

                # draw cards
                print("Drawing cards...")
                time.sleep(0.7)
                self.draw_cards(i)

                for j in range(1, len(self.player)):
                    if j == i:
                        continue
                    self.player[j].enemy[i]["handcard_num"] += 2# update enemy estimation

                if not self.running:
                    self.result = True
                    print("You fought to the end, there are no cards left.\nThe judeg came and decided you are the winner...")
                    break

                # take turns
                print("The round begins...")
                time.sleep(0.7)
                
                self.start_phase(i)

                if not self.running:
                    if not self.player[0].alive:
                        self.result = False
                    else:
                        print("You won!")
                        self.result = True
                    break

                # discard phase
                self.discard_phase(i)
    
    def check_win(self):
        for i in range(1, len(self.player)):
            if self.player[i].alive:
                return False
        return True
    def initialise_deck(self):
        deck_card = []
        for i, j in card_nums.items():
            for p in range(j):
                deck_card.append(Card(card[i]["name"], card[i]["type"]))
        self.deck = Deck(deck_card)
        self.deck.shuffle()
    
    def initialise_handcards(self):
        for i in range(len(self.player)):
            handcards = self.deck.card_list[0:self.player[i].health]
            self.player[i].add_handcards(handcards)
            self.deck.card_list = self.deck.card_list[self.player[i].health:]
    
    def draw_cards(self, num):# 2 cards
        if len(self.deck.card_list) < 2:
            self.running = False
            return 
        newly_drawn_cards = self.deck.draw(2)
        if num == 0:
            print(f"[{newly_drawn_cards[0].name}, {newly_drawn_cards[1].name}] newly added to your handcards")
            time.sleep(0.7)
        self.player[num].handcards.extend(newly_drawn_cards)
        for i in range(1, len(self.player)):
            if i == num or self.player[i].enemy[num] == "self":
                continue
            self.player[i].enemy[num]["handcard_num"] += 2
            

    def print_handcards(self, num):
        format.newline()
        weapen_name = "Not equipped" if self.player[num].equipment['weapen'] is None else self.player[num].equipment['weapen'].name
        armor_name = "Not equipped" if self.player[num].equipment['armor'] is None else self.player[num].equipment['armor'].name
        print(f"Your handcards:")
        for i in range(len(self.player[num].handcards)):
            card_name = f"{i+1}. {self.player[num].handcards[i].name}"
            if i == 0:
                output = "| Your Info:"
                while len(output)<=35:
                        output += ' '
                for p in range(1, len(self.player)):
                    output += f"Player {p+1}:"
                    while len(output)<=35+p*35:
                        output += ' '
                print(f"{card_name:<25}{output}|", end='')
            elif i == 1:
                output = f"| Health: {self.player[num].health}"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    output += f"Health: {self.player[p].health}"
                    while len(output)<=35+p*35:
                        output += ' '
                print(f"{card_name:<25}{output}|", end='')
            elif i == 2:
                output = f"| Max handcards: {self.player[p].health}"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    output += f"Max handcards: {self.player[p].health}"
                    while len(output)<=35+p*35:
                        output += ' '
                print(f"{card_name:<25}{output}|", end='')
            elif i == 3:
                output = "| Equipment:"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    output += f"Equipment:"
                    while len(output)<=35+p*35:
                        output += ' '
                print(f"{card_name:<25}{output}|", end='')
            elif i == 4:
                output = f"- Weapen: {weapen_name}"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    weapen_name_opp = "Not equipped" if self.player[p].equipment['weapen'] is None else self.player[p].equipment['weapen'].name
                    output += f"- Weapen: {weapen_name_opp}"
                    while len(output)<=35+p*35:
                        output += ' '
                output = output[:len(output)-4]
                print(f"{card_name:<25}|   {output}|", end='')
            elif i == 5:
                output = f"- Armor: {armor_name}"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    armor_name_opp = "Not equipped" if self.player[p].equipment['armor'] is None else self.player[p].equipment['armor'].name
                    output += f"- Armor: {armor_name_opp}"
                    while len(output)<=35+p*35:
                        output += ' '
                output = output[:len(output)-4]
                print(f"{card_name:<25}|   {output}|", end='')
            else:
                print(card_name, end='')
            print("")






# if handcards < 6, armor won't be printed

















    def nearly_dead(self, num):
        for i in range(len(self.player[num].handcards)):
            if self.player[num].handcards[i].name == "peach":
                # relpace player 1 with You
                print(f"player {num+1} uses a peach and gaines one point of health")
                self.player[num].health = 1
                self.player[num].max_handcards = 1
                self.player[num].handcards.pop(i)

                for i in range(1, len(self.player)):
                    if i == num:
                        continue
                    self.player[i].enemy[num]["estimated_handcards"]["peach"] -= 1 # update bot's prediction
                    self.player[i].enemy[num]["handcard_num"] -= 1
                    if self.player[i].enemy[num]["estimated_handcards"]["peach"] < 0:
                        print("**ERROR: function-nearly_dead-peach<0**")
                return
        if num == 0:
            self.result = False
            self.running = False
            self.player[num].alive = False
            print("You died...\n Returning to lobby in 3s")
            time.sleep(2)
            return
        print(f"player {num+1} died...")# enemy_num-1
        for i in range(1, len(self.player)):
            if i == num:
                continue
            self.player[i].enemy[num]["alive"] = False # update bot's prediction
        self.player[num].alive = False

    def attack(self, num, human):# human = 1: player attack AI; human = 0: AI attacks AI; human = -1: AI attacks human
        # attack num
        #print(f"num: {num}")# debug
        lose_health = True
        if human == -1:
            find_dodge = -1
            for j in range(len(self.player[0].handcards)):
                if self.player[0].handcards[j].name == "dodge":
                    find_dodge = j
            if find_dodge == -1:
                print("You don't have a dodge, you lose one health point")
            else:
                choice = choose("Do you choose to play a dodge?(y/n)")
                if choice.lower() in ['y', "yes"]:
                    lose_health = False
                    print("You played a dodge...")
                    for i in range(len(self.player[num].handcards)):
                        if self.player[num].handcards[i].name == "dodge":
                            self.player[num].handcards.pop(i)
                            for j in range(1, len(self.player)):
                                if j == num:
                                    continue
                                self.player[j].enemy[num]["estimated_handcards"]["dodge"] -= 1 # update bot's prediction
                                self.player[j].enemy[num]["handcard_num"] -= 1
                                if self.player[j].enemy[num]["estimated_handcards"]["dodge"] < 0:
                                    print("**ERROR: function-attack-dodge<0**")
                            break
                else:
                    print("You choose not to play a dodge and lose one health point")
        elif human == 0: # AI atk AI
            find_dodge = -1
            for j in range(len(self.player[num].handcards)):
                if self.player[num].handcards[j].name == "dodge":
                    find_dodge = j
            if find_dodge == -1:
                print(f"Player {num+1} don't have a dodge")
            else:
                for i in range(len(self.player[num].handcards)):
                    if self.player[num].handcards[i].name == "dodge":
                        print(f"player {num+1} uses [dodge]")
                        self.player[num].handcards.pop(i)

                        for j in range(1, len(self.player)):
                            if j == num:
                                continue
                            self.player[j].enemy[num]["estimated_handcards"]["dodge"] -= 1 # update bot's prediction
                            self.player[j].enemy[num]["handcard_num"] -= 1
                            if self.player[j].enemy[num]["estimated_handcards"]["dodge"] < 0:
                                print("**ERROR: function-attack-dodge<0**")
                        lose_health = False
                        break
        else:
            for i in range(len(self.player[num].handcards)):
                
                if self.player[num].handcards[i].name == "dodge":
                    print(f"player {num+1} uses [dodge]")
                    self.player[num].handcards.pop(i)

                    for j in range(1, len(self.player)):
                        if j == num:
                            continue
                        self.player[j].enemy[num]["estimated_handcards"]["dodge"] -= 1 # update bot's prediction
                        self.player[j].enemy[num]["handcard_num"] -= 1
                        if self.player[j].enemy[num]["estimated_handcards"]["dodge"] < 0:
                            print("**ERROR: function-attack-dodge<0**")
                    lose_health = False
                    break

        if lose_health:
            self.player[num].health -= 1

            for i in range(1, len(self.player)):
                if i == num or not self.player[i].enemy[num]["alive"]:
                    continue
                self.player[i].enemy[num]["health"] -= 1 # update bot's prediction]

            self.player[num].max_handcards -= 1
            print(f"player {num+1} loses one health point\ncurrent health: {self.player[num].health}")
            if self.player[num].health == 0:
                self.nearly_dead(num)
            
    def peach(self, num): # num: the player who uses the peach
        target = f"Player {num+1} uses " if num != 0 else "You use"
        self.player[num].health += 1
        self.player[num].max_handcards += 1
        print(f"{target} a peach and gained one health point...")
        print(f"Current health: {self.player[num].health}")
        for i in range(1, len(self.player)):
            if i == num or not self.player[i].enemy[num]["alive"]:
                continue
            self.player[i].enemy[num]["estimated_handcards"]["peach"] -= 1 # update bot's prediction
            self.player[i].enemy[num]["handcard_num"] -= 1
            if self.player[i].enemy[num]["estimated_handcards"]["peach"] < 0:
                print("**ERROR: 2function-peach<0**")
    def duel(self, num1, num2, human):# human = 1: num1 human, -1: num2 is human, 0: two AI dueling

        # opponent first plays a slash, and then the user, maybe need adjustment

        print("     **[DUEL]**")
        # num1
        if human == 0:
            # AI evaluate
            # 2 AIs
            print("AI should be evaluating this")
            return
        if human == -1: # num2 is human
            # AI should be evaluating this
            self.duel(num2, num1, human*-1)
            return
        who = f"You " if human == 1 else f"player {num1+1} "
        print(f"Your turn:") if human == 1 else print(f"player {num1+1}'s turn:")
        find_slash = -1
        for i in range(len(self.player[num1].handcards)):
            if self.player[num1].handcards[i].name == "slash":
                find_slash = i
        if find_slash == -1:
            print(f"{who} don't have any slashes and loses one health point\nDuel ends")
            self.player[num1].health -= 1

            for i in range(1, len(self.player)):
                if i == num1 or not self.player[i].enemy[num1]["alive"]:
                    continue
                self.player[i].enemy[num1]["health"] -= 1 # update bot's prediction]

            self.player[num1].max_handcards -= 1
            if self.player[num1].health == 0:
                self.nearly_dead(num1)
            return
        choice = choose("Do you choose to play a [slash]?(yes/no)", ["yes", "no"])
        if choice == "yes":
            print(f"{who} player a slash")
            self.player[num1].handcards.pop(find_slash)
            
            for i in range(1, len(self.player)):
                if i == num1 or not self.player[i].enemy[num1]["alive"]:
                    continue
                self.player[i].enemy[num1]["estimated_handcards"]["slash"] -= 1 # update bot's prediction
                self.player[i].enemy[num1]["handcard_num"] -= 1
                if self.player[i].enemy[num1]["estimated_handcards"]["slash"] < 0:
                    print("**ERROR: function-duel-slash<0**")

        else:
            self.player[num1].health -= 1

            for i in range(1, len(self.player)):
                if i == num1 or not self.player[i].enemy[num1]["alive"]:
                    continue
                self.player[i].enemy[num1]["health"] -= 1 # update bot's prediction]
                
                
            self.player[num1].max_handcards -= 1
            print(f"{who} loses one health point\ncurrent health point: {self.player[num1].health}")
            if self.player[num1].health == 0:
                self.nearly_dead(num1)
        self.duel(num2, num1, -human)

    def dismantle(self, num1, num2, human):# human = 1: human dismantle AI| -1:AI dismantle human| 0: two AI 
        if human <= 0:
            if human == 0:
                print(f"Player {num1+1} choose to dismantle Player {num2+1}'s card")
            else:
                print(f"Player {num1+1} choose to dismantle your card")
            if not self.player[num2].equipment["weapen"] is None:
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].enemy[num2]["alive"]:
                        continue
                    self.player[i].enemy[num2]["equipment"]["weapen"] = None # update bot's prediction                    
                self.player[num2].equipment["weapen"] = None
            else:
                random_index = random.randint(0, len(self.player[num2].handcards)-1)
                card_choice = self.player[num2].handcards[random_index]
                print(f"The card Player {num1+1} chose is {card_choice.name}")
                print(f"[{card_choice.name}] dismantled...")
                self.player[num2].handcards.pop(random_index)
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].enemy[num2]["alive"]:
                        continue
                    self.player[i].enemy[num2]["estimated_handcards"][card_choice.name] -= 1 # update bot's prediction
                    self.player[i].enemy[num2]["handcard_num"] -= 1
        else:
            print(f"Player {num2 + 1} has {len(self.player[num2].handcards)} handcards, which one do you want to dismantle?")
            valid_choice = []
            for i in range(len(self.player[num2].handcards)):
                print(f"{i+1}. [xxx]")
                valid_choice.append(str(i+1))


            # add equipment card(snatch too)
            card_choice = int(choose("Choice: ", valid_choice))
            random_select = random.randint(0, len(self.player[num2].handcards)-1)#index
            selected_card = self.player[num2].handcards[random_select]#object
            time.sleep(0.7)
            print(f"The card you chose is {selected_card.name}\n{selected_card.name} discarded from player {num2+1}...")
            # add time.sleep
            self.player[num2].handcards.pop(random_select)
            # update enemy handcard
            for i in range(1, len(self.player)):
                if i == num2 or not self.player[i].enemy[num2]["alive"]:
                    continue
                self.player[i].enemy[num2]["estimated_handcards"][selected_card.name] -= 1 # update bot's prediction
                self.player[i].enemy[num2]["handcard_num"] -= 1
                if self.player[i].enemy[num2]["estimated_handcards"][selected_card.name] < 0:
                    print("**ERROR: dismantle<0**")

    def snatch(self, num1, num2, human): # human = 1: human snatch AI| -1:AI snatch human| 0: two AI 
        if human <= 0:
            if human == 0:
                print(f"Player {num1+1} choose to snatch Player {num2+1}'s card")
            else:
                print(f"Player {num1+1} choose to snatch your card")

            if not self.player[num2].equipment["weapen"] is None:
                self.player[num1].handcards.append(self.player[num2].equipment["weapen"])
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].enemy[num2]["alive"]:
                        continue
                    self.player[i].enemy[num2]["equipment"]["weapen"] = None # update bot's prediction
                for i in range(1, len(self.player)):# player[num1]
                    if i == num1 or not self.player[i].enemy[num1]["alive"]:
                        continue
                    self.player[i].enemy[num1]["estimated_handcards"][self.player[num1].equipment["weapen"]] += 1 # update bot's prediction
                    self.player[i].enemy[num1]["handcard_num"] += 1
                    
                self.player[num2].equipment["weapen"] = None
            else:
                random_index = random.randint(0, len(self.player[num2].handcards)-1)
                card_choice = self.player[num2].handcards[random_index]
                print(f"The card Player {num1+1} chose is {card_choice.name}")
                self.player[num1].handcards.append(card_choice)
                self.player[num2].handcards.pop(random_index)
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].enemy[num2]["alive"]:
                        continue
                    self.player[i].enemy[num2]["estimated_handcards"][card_choice.name] -= 1 # update bot's prediction
                    self.player[i].enemy[num2]["handcard_num"] -= 1
                for i in range(1, len(self.player)):# player[num1] gain a card
                    if i == num1 or not self.player[i].enemy[num1]["alive"]:
                        continue
                    self.player[i].enemy[num1]["estimated_handcards"][card_choice.name] += 1 # update bot's prediction
                    self.player[i].enemy[num1]["handcard_num"] += 1
        else:
            print(f"Player {num2 + 1} has {len(self.player[num2].handcards)} handcards, which one do you want to snatch?")
            valid_choice = []
            for i in range(len(self.player[num2].handcards)):
                print(f"{i+1}. [xxx]")
                valid_choice.append(str(i+1))
            card_choice = int(choose("Choice: ", valid_choice))-1 # 0 indexed
            #random_select = random.randint(0, len(self.player[num2].handcards)-1)#index
            selected_card = self.player[num2].handcards[card_choice] #object
            time.sleep(0.7)
            print(f"The card you chose is {selected_card.name}\n{selected_card.name} added to your handcards")
            # add time.sleep
            self.player[num1].add_handcards([selected_card])
            self.player[num2].handcards.pop(card_choice)
            # update enemy handcard
            for i in range(1, len(self.player)):# player[num2] lost a card
                if i == num2 or not self.player[i].enemy[num2]["alive"]:
                    continue
                self.player[i].enemy[num2]["estimated_handcards"][selected_card.name] -= 1 # update bot's prediction
                self.player[i].enemy[num2]["handcard_num"] -= 1
                if self.player[i].enemy[num2]["estimated_handcards"][selected_card.name] < 0:
                    print("**ERROR: snatch1<0**")
            
            for i in range(1, len(self.player)): # player[num1] gained one card
                if i == num1 or not self.player[i].enemy[num1]["alive"]:
                    continue
                self.player[i].enemy[num1]["estimated_handcards"][selected_card.name] += 1 # update bot's prediction
                self.player[i].enemy[num1]["handcard_num"] += 1
                if self.player[i].enemy[num1]["estimated_handcards"][selected_card.name] < 0:
                    print("**ERROR: snatch2<0**")
            
    def archery(self, num, human):# num is the index of the player who played the card, which don't need to play a dodge,
        # human=1: player is the card user, human = 0: AI playerd the card
        for i in range(0, len(self.player)):
            if i == num:
                continue
            if i == 0:
                find_dodge = -1
                find_negate = -1
                for j in range(len(self.player[0].handcards)):
                    if self.player[0].handcards[j].name == "dodge":
                        find_dodge = j
                    if self.player[0].handcards[j].name == "negate":
                        find_negate = j
                if find_dodge == -1 and find_negate == -1:
                    print("You don't have a dodge or negate, you lose one health point...")
                    self.player[0].health -= 1
                    for j in range(1, len(self.player)):
                        if j == 0 or not self.player[j].enemy[0]["alive"]:
                            continue
                        self.player[j].enemy[0]["health"] -= 1 # update bot's prediction]
                    self.player[0].max_handcards -= 1
                    if self.player[0].health == 0:
                        self.nearly_dead(0)
                else:
                    n = 1
                    output = f"What do you choose to play:\n"
                    if find_dodge != -1:
                        output += f"{n}. dodge\n"
                        n += 1
                    if find_negate != -1:
                        output += f"{n}. negate\n"
                        n += 1
                    output += f"{n+1}. pass(lose one health point)"
                    n += 1
                    print(output)
                    valid_choice = []
                    for j in range(1, n):
                        valid_choice.append(str(j))
                    choice = int(choose("Choice: ", valid_choice))
                    if choice == 1:
                        if find_dodge != -1: # play dodge             
                            print("You played a dodge")         
                            for j in range(1, len(self.player)):
                                if j == num or not self.player[j].enemy[0]["alive"]:
                                    continue
                                self.player[j].enemy[0]["estimated_handcards"]["dodge"] -= 1 # update bot's prediction
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]["estimated_handcards"]["dodge"] < 0:
                                    print("**ERROR: archery-player1-dodge<0**")
                            self.player[0].handcards.pop(find_dodge)
                        else: # must be negate
                            print("You played negate and countered archery")         
                            for j in range(1, len(self.player)):
                                if j == num or not self.player[j].enemy[0]["alive"]:
                                    continue
                                self.player[j].enemy[0]["estimated_handcards"]["negate"] -= 1 # update bot's prediction
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]["estimated_handcards"]["negate"] < 0:
                                    print("**ERROR: archery-player1-negate<0**")
                            self.player[0].handcards.pop(find_negate)
                    elif (choice == 2 and find_dodge*find_negate < 0) or choice == n+1: # pass
                        #choice == n+1 must be pass; If the two indexes multiply to be negative, one of them must be -1, then choice == 2 is pass
                        print("You choose to pass and lose one health point")
                        self.player[0].health -= 1
                        for j in range(1, len(self.player)):
                            if j == 0 or not self.player[j].enemy[0]["alive"]:
                                continue
                            self.player[j].enemy[0]["health"] -= 1 # update bot's prediction]
                        self.player[0].max_handcards -= 1
                        if self.player[0].health == 0:
                            self.nearly_dead(0)

                    else:#play negate
                        print("You played negate and countered archery")         
                        for j in range(1, len(self.player)):
                            if j == num or not self.player[j].enemy[0]["alive"]:
                                continue
                            self.player[j].enemy[0]["estimated_handcards"]["negate"] -= 1 # update bot's prediction
                            self.player[j].enemy[0]["handcard_num"] -= 1
                            if self.player[j].enemy[0]["estimated_handcards"]["negate"] < 0:
                                print("**ERROR: archery-player1-negate<0**")
                        self.player[0].handcards.pop(find_negate)
            else:
                # AI should be handling this
                pass

    def savage(self, num, human):# num is the index of the player who played the card, which don't need to play a dodge,
        # human=1: player is the card user, human = 0: AI playerd the card
        for i in range(0, len(self.player)):
            if i == num:
                continue
            if i == 0:
                find_slash = -1
                find_negate = -1
                for j in range(len(self.player[0].handcards)):
                    if self.player[0].handcards[j].name == "slash":
                        find_slash = j
                    if self.player[0].handcards[j].name == "negate":
                        find_negate = j
                if find_slash == -1 and find_negate == -1:
                    print("You don't have a slash or negate, you lose one health point...")
                    self.player[0].health -= 1
                    for j in range(1, len(self.player)):
                        if j == 0 or not self.player[j].enemy[0]["alive"]:
                            continue
                        self.player[j].enemy[0]["health"] -= 1 # update bot's prediction]
                    self.player[0].max_handcards -= 1
                    if self.player[0].health == 0:
                        self.nearly_dead(0)
                else:
                    n = 0
                    output = f"What do you choose to play:\n"
                    if find_slash != -1:
                        output += f"{n+1}. slash\n"
                        n += 1
                    if find_negate != -1:
                        output += f"{n+1}. neagte\n"
                        n += 1
                    output += f"{n}. pass(lose one health point)"
                    print(output)
                    valid_choice = []
                    for j in range(1, n+2):
                        valid_choice.append(str(j))
                    choice = int(choose("Choice: ", valid_choice))
                    if choice == 1:
                        if find_slash != -1: # play slash             
                            print("You played a slash")         
                            for j in range(1, len(self.player)):
                                if j == num or not self.player[j].enemy[0]["alive"]:
                                    continue
                                self.player[j].enemy[0]["estimated_handcards"]["slash"] -= 1 # update bot's prediction
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]["estimated_handcards"]["slash"] < 0:
                                    print("**ERROR: savage-player1-slash<0**")
                            self.player[0].handcards.pop(find_slash)
                        else: # must be negate
                            print("You played negate and countered savage")         
                            for j in range(1, len(self.player)):
                                if j == num or not self.player[j].enemy[0]["alive"]:
                                    continue
                                self.player[j].enemy[0]["estimated_handcards"]["negate"] -= 1 # update bot's prediction
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]["estimated_handcards"]["negate"] < 0:
                                    print("**ERROR: savage-player1-negate<0**")
                            self.player[0].handcards.pop(find_negate)
                    elif (choice == 2 and find_slash*find_negate < 0) or choice == n+1: # pass
                        #choice == n+1 must be pass; If the two indexes multiply to be negative, one of them must be -1, then choice == 2 is pass
                        print("You choose to pass and lose one health point")
                        self.player[0].health -= 1
                        for j in range(1, len(self.player)):
                            if j == 0 or not self.player[j].enemy[0]["alive"]:
                                continue
                            self.player[j].enemy[0]["health"] -= 1 # update bot's prediction]
                        self.player[0].max_handcards -= 1
                        if self.player[0].health == 0:
                            self.nearly_dead(0)

                    else:#play negate
                        print("You played negate and countered savage")         
                        for j in range(1, len(self.player)):
                            if j == num or not self.player[j].enemy[0]["alive"]:
                                continue
                            self.player[j].enemy[0]["estimated_handcards"]["negate"] -= 1 # update bot's prediction
                            self.player[j].enemy[0]["handcard_num"] -= 1
                            if self.player[j].enemy[0]["estimated_handcards"]["negate"] < 0:
                                print("**ERROR: savage-player1-negate<0**")
                        self.player[0].handcards.pop(find_negate)
            else:
                # AI should be handling this
                print("AI should be handling this")
                pass
    def benevolence(self, num, human):
        string = "You" if human != 0 else f"Player {num+1}"
        print(f"{string} drawed two cards from the deck of cards...")
        self.draw_cards(num)
        if not self.running:
            self.result = True
            print("You fought to the end, there are no cards left.\nThe judeg came and decided you are the winner...")
            return

        
    def negate(self):
        # need to add choice of using negate to other trick cards /\/\/\/\/\/\/\/\/\/\/\/\
        pass

    def start_phase(self, num):
        if num == 0:
            print("Your turn:")
            act_step = 1
            while True:# shouldn't exit when act_step == 0, there are other cards
                self.print_handcards(num)
                print(f"Available moves:\n{len(self.player[num].handcards) + 1}. end turn")
                valid_choices = [str(i) for i in range(1, len(self.player[num].handcards) + 2)]
                choice = int(choose("Choice: ", valid_choices))
                if choice == len(self.player[num].handcards) + 1:
                    print("Turn ended")
                    break
                choice -= 1 # 0 indexing
                chosen_card = self.player[num].handcards[choice]
                if chosen_card.type == "basic":
                    if chosen_card.name == "slash":
                        has_crossbow = (self.player[num].equipment["weapen"] is not None and self.player[num].equipment["weapen"].name == "crossbow")
                        if act_step == 0 and not has_crossbow:
                            print("You can only play one [slash] in one turn")
                            continue
                        output = "Who do you want to attack?"
                        alive_targets = []
                        for i in range(1, len(self.player)):
                            if self.player[i].alive:
                                output += f"\n- player {i+1}"
                                alive_targets.append(i + 1)
                        print(output)
                        valid_choices = [str(t) for t in alive_targets]
                        choice_p = int(choose("Choice: ", valid_choices)) - 1 # 0 indexing
                        print(f"You attacked player {choice_p+1}")

                        for i in range(1, len(self.player)):                            
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["slash"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"]["slash"] < 0:
                                print("**ERROR: 1function-start_phase-slash<0**")
                        self.player[num].handcards.pop(choice)

                        time.sleep(0.7)
                        self.attack(choice_p, 1)
                        act_step -= 1
                    if chosen_card.name == "peach":
                        if self.player[num].health == self.player[num].initial_health: # temporary be 4
                            print("**You are already at maximum health**")
                        else:
                            self.peach(num)
                            self.player[num].handcards.pop(choice)

                    if chosen_card.name == "dodge":
                        print("**You can only use [dodge] when another player attacks you**")

                if chosen_card.type == "equipment":
                    if chosen_card.name == "crossbow" or chosen_card.name == "crossblade":
                        if self.player[num].equipment["weapen"] is None:
                            self.player[num].equipment["weapen"] = chosen_card
                            print(f"You successfully equiped {chosen_card.name}")

                            for i in range(1, len(self.player)):
                                
                                if i == num or not self.player[i].enemy[num]["alive"]:
                                    continue
                                self.player[i].enemy[num]["estimated_handcards"][chosen_card.name] -= 1 # update bot's prediction
                                self.player[i].enemy[num]["handcard_num"] -= 1
                                self.player[i].enemy[num]["equipment"]["weapen"] = chosen_card

                                if self.player[i].enemy[num]["estimated_handcards"][chosen_card.name] < 0:
                                    print("**ERROR: 3function-start_phase-equipment<0**")
                            self.player[num].handcards.pop(choice)
                        else:
                            equiped_card_name = self.player[num].equipment["weapen"].name
                            replace_choice = choose(f"You have already equiped {equiped_card_name}, do you want to replace it? y/n\n({equiped_card_name} will be automatically discarded)?\nChoice: ", end='')
                            if replace_choice.lower() in ['y', 'yes']:
                                self.player[num].equipment["weapen"] = chosen_card
                                print(f"You successfully equiped {chosen_card.name}")

                                for i in range(1, len(self.player)):
                                    if i == num or not self.player[i].enemy[num]["alive"]:
                                        continue
                                    self.player[i].enemy[num]["estimated_handcards"][chosen_card.name] -= 1 # update bot's prediction
                                    self.player[i].enemy[num]["handcard_num"] -= 1
                                    self.player[i].enemy[num]["equipment"]["weapen"] = chosen_card
                                    if self.player[i].enemy[num]["estimated_handcards"][chosen_card.name] < 0:
                                        print("**ERROR: 3function-start_phase-equipment<0**")
                                self.player[num].handcards.pop(choice)
                    else:
                        pass # no armor has been made yet
                        
                if chosen_card.type == "trick":
                    card_name = chosen_card.name
                    if card_name == "duel":
                        output = "Who do you want to duel with?"
                        alive_targets = []
                        for i in range(1, len(self.player)):
                            if self.player[i].alive:
                                output += f"\n- player {i+1}"
                                alive_targets.append(i + 1)
                        output += "\n"
                        valid_choices = [str(t) for t in alive_targets]
                        player_choice = int(choose(output, valid_choices)) - 1
                        print(f"You dueled with player {player_choice+1}")# do AI need to play all slash to win the duel?(strategy)
                        

                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["duel"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"]["duel"] < 0:
                                print("**ERROR: 4function-start_phase-duel<0**")
                        self.player[num].handcards.pop(choice)
                        self.duel(num, player_choice, 1)
                    
                    if card_name == "dismantle":
                        output = "Who's card do you want to dismantle?"
                        alive_targets = []
                        for i in range(1, len(self.player)):
                            if self.player[i].alive:
                                output += f"\n- player {i+1}"
                                alive_targets.append(i + 1)
                        output += "\n"
                        valid_choices = [str(t) for t in alive_targets]
                        player_choice = int(choose(output, valid_choices)) - 1
                        self.dismantle(num, player_choice, 1)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["dismantle"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"]["dismantle"] < 0:
                                print("**ERROR: start-phase-dismantle<0**")
                        self.player[num].handcards.pop(choice)
                    
                    if card_name == "snatch":
                        output = "Who's card do you want to snatch?"
                        alive_targets = []
                        for i in range(1, len(self.player)):
                            if self.player[i].alive:
                                output += f"\n- player {i+1}"
                                alive_targets.append(i + 1)
                        output += "\n"
                        valid_choices = [str(t) for t in alive_targets]
                        player_choice = int(choose(output, valid_choices)) - 1
                        self.snatch(num, player_choice, 1)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["snatch"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"]["snatch"] < 0:
                                print("**ERROR: start-phase-snatch<0**")
                        self.player[num].handcards.pop(choice)

                    if card_name == "archery":
                        self.archery(num, 1)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["archery"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"]["archery"] < 0:
                                print("**ERROR: start-phase-archery<0**")
                        self.player[num].handcards.pop(choice)

                    if card_name == "savage":
                        self.savage(num, 1)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["savage"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"]["savage"] < 0:
                                print("**ERROR: start-phase-savage<0**")
                        self.player[num].handcards.pop(choice)

                    if card_name == "benevolence":
                        self.benevolence(num, 1)
                        if not self.running:
                            return
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["benevolence"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"]["benevolence"] < 0:
                                print("**ERROR: start-phase-benevolence<0**")
                        self.player[num].handcards.pop(choice)

                    if card_name == "negate":
                        print("**You can only use [negate] when another player use a trick card on you**")
        else:
            print(f"Player {num+1}'s turn:")
            #### for testing
            print(f"Player {num+1}'s handcard: (for testing)")
            self.print_handcards(num)
            ####
            #initialise act_step
            self.player[num].act_step = 1
            while True:
                # Bot move
                
                action = self.player[num].take_move(self.player)
                
                if action == -1:
                    print(f"Player {num+1} end its turn...")
                    time.sleep(0.7)
                    break
                card = action["card"]
                if card.name == "slash":
                    target = f"player {action['target']+1}" if action['target'] != 0 else "you"
                    print(f"Player {num+1} attacks {target} with [slash]")
                    if action["target"] == 0:
                        self.attack(action["target"], -1)
                    else:
                        self.attack(action["target"], 0)
                    for i in range(1, len(self.player)):
                        if i == num or not self.player[i].enemy[num]["alive"]:
                            continue
                        self.player[i].enemy[num]["estimated_handcards"][card.name] -= 1 # update bot's prediction
                        self.player[i].enemy[num]["handcard_num"] -= 1
                        self.player[i].enemy[num]["equipment"]["weapen"] = card.name

                        if self.player[i].enemy[num]["estimated_handcards"][card.name] < 0:
                            print("**ERROR: 6function-start_phase-AI-slash<0**")
                        self.player[num].handcards.pop(action["index"])
                if card.name == "peach":
                    self.peach(num)
                    # enemy estimation already updated in peach
                    self.player[num].handcards.pop(action["index"])
                if card.type == "equipment":
                    if card.name in ["crossbow", "crossblade"]:
                        if not self.player[num].equipment["weapen"] is None:
                            extra = f" and replaced {self.player[num].equipment['weapen']}"
                        self.player[num].equipment["weapen"] = card
                        print(f"Player {num+1} successfully equiped {card.name}{extra}")

                        for i in range(1, len(self.player)):
                            
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"][card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            self.player[i].enemy[num]["equipment"]["weapen"] = card.name

                            if self.player[i].enemy[num]["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 6function-start_phase-AI-equipment<0**")
                        self.player[num].handcards.pop(action["index"])
                    else:#armor
                        pass
                if card.type == "trick":
                    if card.name == "savage":
                        print(f"Player {num+1} played [savage]")
                        self.savage(num, 0)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"][card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 6function-start_phase-AI-equipment<0**")
                        self.player[num].handcards.pop(action["index"])

                    if card.name == "archery":
                        print(f"Player {num+1} played [archery]")
                        self.archery(num, 0)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"][card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 6function-start_phase-AI-equipment<0**")
                        self.player[num].handcards.pop(action["index"])

                    if card.name == "benevolence":
                        print(f"Player {num+1} played [benevolence]")
                        self.benevolence(num, 0)
                        if not self.running:
                            return
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"][card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 6function-start_phase-AI-benevolence<0**")
                        self.player[num].handcards.pop(action["index"])

                    if card.name == "snatch":
                        print(f"Player {num+1} played [snatch]")
                        if action["target"] == 0:
                            self.snatch(num, action["target"], -1)
                        else:
                            self.snatch(num, action["target"], 0)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"][card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 7function-start_phase-AI-snatch<0**")
                        self.player[num].handcards.pop(action["index"])
                    if card.name == "dismantle":
                        print(f"Player {num+1} played [dismantle]")
                        if action["target"] == 0:
                            self.dismantle(num, action["target"], -1)
                        else:
                            self.dismantle(num, action["target"], 0)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].enemy[num]["alive"]:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"][card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 8function-start_phase-AI-dismantle<0**")
                        self.player[num].handcards.pop(action["index"])
                        

                '''
                action:
                action["card"]: card object
                action["target"]: if -1: archery or savage, or peach
                                  else: other cards, call method "card_name"(num, target, human)
                '''
            return

    def discard_phase(self, num):
        print("     [Discard phase]")
        time.sleep(0.7)
        if not num == 0:
            # Bot decision
            return
        if len(self.player[num].handcards) > self.player[num].max_handcards:
            while(len(self.player[num].handcards) > self.player[num].max_handcards):
                print(f"Current number of handcards: {len(self.player[num].handcards)}\nmaximum number of handcards: {self.player[num].max_handcards}")
                self.print_handcards(num)
                valid_choices = [str(i) for i in range(1, len(self.player[num].handcards) + 1)]
                choice = int(choose("Discard card: ", valid_choices, "yes")) - 1 # 1-# , so -1
                discarded_card = self.player[num].handcards[choice]
                for i in range(1, len(self.player)):
                    if i == num or not self.player[i].enemy[num]["alive"]:
                        continue
                    self.player[i].enemy[num]["estimated_handcards"][discarded_card.name] -= 1 # update bot's prediction
                    self.player[i].enemy[num]["handcard_num"] -= 1
                    if self.player[i].enemy[num]["estimated_handcards"][discarded_card.name] < 0:
                        print("**ERROR: function-discard_phase-discard_card<0**")
                
                self.player[num].handcards.pop(choice)
        else:
            print(f"Current number of handcards: {len(self.player[num].handcards)}\nmaximum number of handcards: {self.player[num].max_handcards}")
            print("Discard phase skipped...")

   

format = Format()

game = Game1(3, 4) # when commmenting this, don't forget to change the import in bot.py in for find_high_value_target method
game.run()
