##############################################################################
#Coder: Leo
#Last date modified: 1/14/2026
##############################################################################
"""This module is the main code for the mini game EndPhase. It imports other 
modules in EndPhase folder and is imported by the main code."""
##############################################################################
from games.common.score import *
from games.common.format import Format
from games.EndPhase.bot import Bot
from games.EndPhase.choose import choose
from games.EndPhase.human import Human
from games.EndPhase.deck import Deck
from games.EndPhase.card import Card
from games.common.GameHandler import GameHandler
import time
import json
import os
import random


class EndPhaseGame(GameHandler):
    """This class runs the entire end phase game. It has two 
    perimeters: user, which is the player object and money, which
    is the money the player gets after winning the game.
    Some important features are self.running, which is checked to 
    keep the game running and self.result, 
    which is checked by to determine did the player win or not.
    The class inherits from GameHandler class, which has game 
    information and player information
    """
    def __init__(self, user, money):
        self.money = money
        player_num = 3
        initial_health = 4 # these two can be changed
        self.user = user 
        self.running = True
        self.result = False
        self.card_nums = card_nums
        self.player = []
        self.player.append(Human(f"player1", initial_health, 0))
        for i in range(1, player_num):
            self.player.append(Bot(f"player{i+1}", initial_health, 
                                   player_num - 1, i))
        self.initialise_deck()
        self.initialise_handcards()
        self.game_rule_key = 'q'
        self.card_description_key = 'w'
        GameHandler.__init__(self, self.player, None, "End Phase")

    def run(self):
        """This method runs the whole game. It then deal with game 
        result, punishments or rewards"""
        # checks if print the game rules and card description 
        # with animation
        if self.user.name.lower() == "test":
            self.print_rules(False) # no animation
            time.sleep(0.7)
            self.print_card_description(False)
        else:
            self.print_rules(True) # need animation
            time.sleep(0.7)
            self.print_card_description(True)
        print(f"(You can review the game rules and card descriptions "
              f"by entering {self.game_rule_key} and "
                f"{self.card_description_key})")
        print("**Game starts**")
        time.sleep(0.7)
        # This while loop loops infinitely till the game ends
        while self.running:
            if self.check_win():
                self.result = True
                break
            for i in range(len(self.player)):
                if not self.player[i].alive:
                    continue
                format.newline()
                # draw cards
                print("Drawing cards...")
                time.sleep(0.7)
                self.draw_cards(i)
                for j in range(1, len(self.player)):
                    if j == i:
                        continue
                    self.player[j].enemy[i]["handcard_num"] += 2
                    # update enemy estimation
                if not self.running:
                    self.result = True
                    print("You fought to the end, there are no cards "
                          "left.\nThe judeg came and decided you are the "
                          "winner...")
                    for i in range(3, 1, -1):
                        print(f"\rReturning to lobby in {i}s")
                        time.sleep(1)
                    break
                # take turns
                print("The round begins...")
                time.sleep(0.7)    
                self.start_phase(i)
                if not self.running:
                    if not self.player[0].alive or not self.result:
                        self.result = False
                    else:
                        print("You won!")
                        self.result = True
                    break
                # discard phase
                self.discard_phase(i)
        self.handle_game_result()

    def verify_admin_mode(self, choice):
        """This is a developer mode, it helps developers quickly skip the 
        game and get results.
        choice is a string that can be admin to open admin mode"""
        # admin mode provide convenience for developers
        if choice.lower() == "admin":
            code = input("Admin code: ")
            if code == "0710":
                result = input("Win or lose(1/0):")
                if result == '1':
                    print("You win...(Admin mode)")
                    time.sleep(2)
                    self.running = False
                    self.result = True
                    return
                if result == '0':
                    print("You lost...(Admin mode)")
                    time.sleep(2)
                    self.running = False
                    self.result = False
                    self.player[0].alive = False
                    return
        
    def handle_game_result(self):
        """Is called after the game ends, and update all the player 
        information"""
        updateScore(self.result, self.user, self.money)
    
    def check_win(self):
        """Check if all other bots have died, if so, 
        the human player wins"""
        for i in range(1, len(self.player)):
            if self.player[i].alive:
                return False
        return True
    
    def initialise_deck(self):
        """Create deck of cards and randomize it."""
        deck_card = []
        for i, j in card_nums.items():
            for p in range(j):
                deck_card.append(Card(card[i]["name"], card[i]["type"]))
        self.deck = Deck(deck_card)
        self.deck.shuffle()
    
    def initialise_handcards(self):
        """Draw each player a certain amount of cards and add 
        them to their handcards."""
        for i in range(len(self.player)):
            handcards = self.deck.card_list[0:self.player[i].health]
            self.player[i].add_handcards(handcards)
            self.deck.card_list = self.deck.card_list[self.player[i].health:]
    
    def draw_cards(self, num):# 2 cards
        """This method reads an int peremeter, which is the player 
        that is drawing cards, it then draws
        2 cards and adds them to the player handcards."""
        if len(self.deck.card_list) < 2:
            self.running = False
            return 
        newly_drawn_cards = self.deck.draw(2)
        if num == 0:
            print(f"[{newly_drawn_cards[0].name},"
                  f" {newly_drawn_cards[1].name}] "
                  "newly added to your handcards")
            time.sleep(0.7)
        self.player[num].handcards.extend(newly_drawn_cards)
        for i in range(1, len(self.player)):
            if i == num or self.player[i].enemy[num] == "self":
                continue
            self.player[i].enemy[num]["handcard_num"] += 2
            
    def print_handcards(self, num):
        """This method reads the peremeter: num, and prints the 
        handcards of the player num and the other 
        player information."""
        format.newline()
        weapen_name = "Not equipped" if self.player[num].equipment['weapen']\
              is None else self.player[num].equipment['weapen'].name
        armor_name = "Not equipped" if self.player[num].equipment['armor'] \
            is None else self.player[num].equipment['armor'].name
        print(f"Your handcards:           (Review Game Rules: q)  "
              "(Review Card Descriptions: w)")
        for i in range(max(len(self.player[num].handcards), 7)):
            if i < len(self.player[num].handcards):
                card_name = f"{i+1}. {self.player[num].handcards[i].name}"
            else:
                card_name = ""
            if i == 0:
                # these code prints player information side by side
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
                output = f"| Current handcards: " + \
                    f"{len(self.player[num].handcards)}"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    output += f"Current handcards: " + \
                        f"{len(self.player[p].handcards)}"
                    while len(output)<=35+p*35:
                        output += ' '
                print(f"{card_name:<25}{output}|", end='')
            elif i == 3:
                output = f"| Max handcards: {self.player[num].health}"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    output += f"Max handcards: {self.player[p].health}"
                    while len(output)<=35+p*35:
                        output += ' '
                print(f"{card_name:<25}{output}|", end='')
            elif i == 4:
                output = "| Equipment:"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    output += f"Equipment:"
                    while len(output)<=35+p*35:
                        output += ' '
                print(f"{card_name:<25}{output}|", end='')
            elif i == 5:
                output = f"- Weapen: {weapen_name}"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    weapen_name_opp = "Not equipped" if \
                        self.player[p].equipment['weapen'] is None \
                            else self.player[p].equipment['weapen'].name
                    output += f"- Weapen: {weapen_name_opp}"
                    while len(output)<=35+p*35:
                        output += ' '
                output = output[:len(output)-4]
                print(f"{card_name:<25}|   {output}|", end='')
            elif i == 6:
                output = f"- Armor: {armor_name}"
                while len(output)<=35:
                    output += ' '
                for p in range(1, len(self.player)):
                    armor_name_opp = "Not equipped" if \
                        self.player[p].equipment['armor'] is None \
                            else self.player[p].equipment['armor'].name
                    output += f"- Armor: {armor_name_opp}"
                    while len(output)<=35+p*35:
                        output += ' '
                output = output[:len(output)-4]
                print(f"{card_name:<25}|   {output}|", end='')
            else:
                print(card_name, end='')
            print("")

    def nearly_dead(self, num):
        """This method reads the peremeter num and checks if player 
        num is really dead because of the existance of peach."""
        for i in range(len(self.player[num].handcards)):
            if self.player[num].handcards[i].name == "peach":
                # relpace player 1 with You
                print(f"player {num+1} uses a [peach] and gaines one point "
                      "of health")
                time.sleep(0.7)
                self.player[num].health = 1
                self.player[num].max_handcards = 1
                self.player[num].handcards.pop(i)
                for i in range(1, len(self.player)):
                    if i == num:
                        continue
                    self.player[i].enemy[num]["estimated_handcards"]["peach"]\
                          -= 1 # update bot's prediction
                    self.player[i].enemy[num]["handcard_num"] -= 1
                    if self.player[i].enemy[num]["estimated_handcards"]\
                        ["peach"] < 0:
                        print("**ERROR: function-nearly_dead-peach<0**")
                return
        if num == 0:
            self.result = False
            self.running = False
            self.player[num].alive = False
            print("You died...\nReturning to lobby in 3s")
            time.sleep(2)
            return
        print(f"player {num+1} died...")# enemy_num-1
        for i in range(1, len(self.player)):
            if i == num:
                continue
            # update bot's prediction
            self.player[i].enemy[num]["alive"] = False 
        self.player[num].alive = False

    def attack(self, num1, num2, human):
        """This method is the attack method.
        Explanation of the peremeters:
        all peremeters are integers
        num1: the attacking side
        num2: the player being attacked
        human = 1: player attack AI; human = 0: AI attacks AI; 
            human = -1: AI attacks human
        The method checks if the player being attacked has a dodge.
        If so, and the player is the human player, it asks if the 
        player wants to play a dodge.
        if its a bot, it plays a dodge
        if not, the player being attacked lose one health point
        """
        # Check if num2 has evasion armor equipped
        if self.player[num2].equipment["armor"] is not None and \
            self.player[num2].equipment["armor"].name == "evasion":
            # 50% chance to automatically dodge
            if random.randint(0, 1) == 0:  # 50% chance
                if num2 == 0:
                    print("Your [evasion] armor dodged the [slash]")
                else:
                    print(f"Player {num2+1}'s [evasion] armor dodged the "
                          "[slash]")
                time.sleep(1.5)
                # Check if attacker has crossblade for the crossblade effect
                if self.player[num1].equipment["weapen"] is not None and \
                self.player[num1].equipment["weapen"].name == "crossblade":
                    if human == 1:  # Player is attacker
                        choice = choose(f"Do you choose to lose one health "
                                        f"point to let Player {num2+1} lose "
                                        "one health point?(y/n): ")
                        if choice.lower() in ['y', 'yes']:
                            time.sleep(0.7)
                            # Attacker loses 1 health
                            self.player[num1].health -= 1
                            self.player[num1].max_handcards -= 1
                            for k in range(1, len(self.player)):
                                if k == num1 or not self.player[k].alive:
                                    continue
                                self.player[k].enemy[num1]["health"] -= 1
                            print(f"Your current health: "
                                  f"{self.player[num1].health}")
                            if self.player[num1].health == 0:
                                self.nearly_dead(num1)                          
                            # Target loses 1 health
                            self.player[num2].health -= 1
                            self.player[num2].max_handcards -= 1
                            for k in range(1, len(self.player)):
                                if k == num2 or not self.player[k].alive:
                                    continue
                                self.player[k].enemy[num2]["health"] -= 1
                            if num2 == 0:
                                print(f"You lose one health point\ncurrent "
                                      f"health: {self.player[num2].health}")
                            else:
                                print(f"Player {num2+1} loses one health "
                                      "point\ncurrent health: "
                                      f"{self.player[num2].health}")
                            time.sleep(0.7)
                            if self.player[num2].health == 0:
                                self.nearly_dead(num2)
                    elif human == -1 or human == 0:  # AI is attacker
                        if self.player[num1].health >= 3 or \
                            (self.player[num1].health >= 2 and 
                             self.player[num2].health == 1):
                            print(f"Player {num1+1} choose to lose 1 "
                                  "health to cause 1 damage")
                            time.sleep(0.7)
                            # Attacker loses 1 health
                            self.player[num1].health -= 1
                            self.player[num1].max_handcards -= 1
                            for k in range(1, len(self.player)):
                                if k == num1 or not self.player[k].alive:
                                    continue
                                self.player[k].enemy[num1]["health"] -= 1
                            print(f"Player {num1+1}'s current health: "
                                  f"{self.player[num1].health}")
                            if self.player[num1].health == 0:
                                self.nearly_dead(num1)                           
                            # Target loses 1 health
                            self.player[num2].health -= 1
                            self.player[num2].max_handcards -= 1
                            for k in range(1, len(self.player)):
                                if k == num2 or not self.player[k].alive:
                                    continue
                                self.player[k].enemy[num2]["health"] -= 1
                            if num2 == 0:
                                print(f"You lose one health point\ncurrent "
                                      f"health: {self.player[num2].health}")
                            else:
                                print(f"Player {num2+1} loses one health "
                                      "point\ncurrent health:"
                                      f"{self.player[num2].health}")
                            time.sleep(0.7)
                            if self.player[num2].health == 0:
                                self.nearly_dead(num2)
                return  # End attack since evasion dodged
            else:
                if num2 == 0:
                    print("Your [evasion] armor failed to dodged the [slash]")
                else:
                    print(f"Player {num2+1}'s [evasion] armor failed " 
                          "to dodged the [slash]")
                time.sleep(0.7)
        # num1 attacks num2
        lose_health = True
        if human == -1:  # AI attacks human
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
                    for i in range(len(self.player[0].handcards)):
                        if self.player[0].handcards[i].name == "dodge":
                            self.player[0].handcards.pop(i)
                            for j in range(1, len(self.player)):
                                if not self.player[j].alive:
                                    continue
                                self.player[j].enemy[0]\
                                    ["estimated_handcards"]["dodge"] -= 1
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]\
                                    ["estimated_handcards"]["dodge"] < 0:
                                    print("**ERROR: "
                                          "function-attack-dodge<0**")
                            break               
                    # Check if attacker has crossblade
                    if self.player[num1].equipment["weapen"] is not None and \
                    self.player[num1].equipment["weapen"].name ==\
                          "crossblade":
                        # AI decides whether to use crossblade effect
                        if self.player[num1].health >= 3 or \
                            (self.player[num1].health >= 2 and \
                             self.player[num2].health == 1):  
                            # AI only uses if health >= 2
                            print(f"Player {num1+1} "
                                  "choose to lose 1 health to" 
                                  " cause 1 damage.")
                            time.sleep(0.7)
                            # Attacker loses 1 health
                            self.player[num1].health -= 1
                            self.player[num1].max_handcards -= 1
                            for i in range(1, len(self.player)):
                                if i == num1 or not self.player[i].alive:
                                    continue
                                self.player[i].enemy[num1]["health"] -= 1
                            print(f"Player {num1+1}'s current health: "
                                  f"{self.player[num1].health}")
                            if self.player[num1].health == 0:
                                self.nearly_dead(num1)                     
                            # Target loses 1 health
                            self.player[num2].health -= 1
                            self.player[num2].max_handcards -= 1
                            for i in range(1, len(self.player)):
                                if i == num2 or not self.player[i].alive:
                                    continue
                                self.player[i].enemy[num2]["health"] -= 1
                            print(f"You lose one health point\ncurrent "
                                  f"health: {self.player[num2].health}")
                            time.sleep(0.7)
                            if self.player[num2].health == 0:
                                self.nearly_dead(num2)
                else:
                    print("You choose not to play a dodge and lose one "
                          "health point")                   
        elif human == 0:  # AI attacks AI
            find_dodge = -1
            for j in range(len(self.player[num2].handcards)):
                if self.player[num2].handcards[j].name == "dodge":
                    find_dodge = j
            if find_dodge == -1:
                print(f"Player {num2+1} don't have a dodge")
            else:
                for i in range(len(self.player[num2].handcards)):
                    if self.player[num2].handcards[i].name == "dodge":
                        print(f"player {num2+1} uses [dodge]")
                        self.player[num2].handcards.pop(i)

                        for j in range(1, len(self.player)):
                            if j == num2:
                                continue
                            self.player[j].enemy[num2]["estimated_handcards"]\
                                ["dodge"] -= 1
                            self.player[j].enemy[num2]["handcard_num"] -= 1
                            if self.player[j].enemy[num2]\
                                ["estimated_handcards"]["dodge"] < 0:
                                print("**ERROR: function-attack-dodge<0**")
                        lose_health = False                      
                        # Check if attacker has crossblade
                        if self.player[num1].equipment["weapen"] is not \
                            None and \
                        self.player[num1].equipment["weapen"].name \
                            == "crossblade":
                            # AI decides whether to use crossblade 
                            if self.player[num1].health >= 3 or \
                                (self.player[num1].health >= 2 and \
                                 self.player[num2].health == 1):  
                                    # AI only uses if health >= 2
                                print(f"Player {num1+1} choose to "
                                      "lose 1 health to cause 1 damage")
                                time.sleep(0.7)
                                # Attacker loses 1 health
                                self.player[num1].health -= 1
                                self.player[num1].max_handcards -= 1
                                for k in range(1, len(self.player)):
                                    if k == num1 or not self.player[k].alive:
                                        continue
                                    self.player[k].enemy[num1]["health"] -= 1
                                print(f"Player {num1+1}'s current health: "
                                      f"{self.player[num1].health}")
                                if self.player[num1].health == 0:
                                    self.nearly_dead(num1)            
                                # Target loses 1 health
                                self.player[num2].health -= 1
                                self.player[num2].max_handcards -= 1
                                for k in range(1, len(self.player)):
                                    if k == num2 or not self.player[k].alive:
                                        continue
                                    self.player[k].enemy[num2]["health"] -= 1
                                print(f"Player {num2+1} loses one health "
                                      "point\ncurrent health: "
                                      f"{self.player[num2].health}")
                                time.sleep(0.7)
                                if self.player[num2].health == 0:
                                    self.nearly_dead(num2)
                        break                     
        else:  # Player attacks AI
            for i in range(len(self.player[num2].handcards)):
                if self.player[num2].handcards[i].name == "dodge":
                    print(f"player {num2+1} uses [dodge]")
                    self.player[num2].handcards.pop(i)
                    for j in range(1, len(self.player)):
                        if j == num2:
                            continue
                        self.player[j].enemy[num2]["estimated_handcards"]\
                            ["dodge"] -= 1
                        self.player[j].enemy[num2]["handcard_num"] -= 1
                        if self.player[j].enemy[num2]["estimated_handcards"]\
                        ["dodge"] < 0:
                            print("**ERROR: function-attack-dodge<0**")
                    lose_health = False    
                    # Check if attacker (human player) has crossblade
                    if self.player[num1].equipment["weapen"] is not None \
                        and self.player[num1].equipment["weapen"].name == \
                            "crossblade":
                        choice = choose(f"Do you choose to lose one health "
                                        f"point to let Player {num2+1} lose "
                                        "one health point?(y/n): ")
                        if choice.lower() in ['y', 'yes']:
                            time.sleep(0.7)
                            # Attacker loses 1 health
                            self.player[num1].health -= 1
                            self.player[num1].max_handcards -= 1
                            for k in range(1, len(self.player)):
                                if k == num1 or not self.player[k].alive:
                                    continue
                                self.player[k].enemy[num1]["health"] -= 1
                            print(f"Your current health: "
                                  f"{self.player[num1].health}")
                            if self.player[num1].health == 0:
                                self.nearly_dead(num1)                            
                            # Target loses 1 health
                            self.player[num2].health -= 1
                            self.player[num2].max_handcards -= 1
                            for k in range(1, len(self.player)):
                                if k == num2 or not self.player[k].alive:
                                    continue
                                self.player[k].enemy[num2]["health"] -= 1
                            print(f"Player {num2+1} loses one health point\n"
                                "current health: {self.player[num2].health}")
                            time.sleep(0.7)
                            if self.player[num2].health == 0:
                                self.nearly_dead(num2)
                    break
        if lose_health:# checks if a player is nearly dead
            self.player[num2].health -= 1
            for i in range(1, len(self.player)):
                if i == num2 or not self.player[i].alive:
                    continue
                self.player[i].enemy[num2]["health"] -= 1
            self.player[num2].max_handcards -= 1
            if num2 == 0:
                player = "You"
            else:
                player = f"Player {num2+1}"
            print(f"{player} loses one health point\ncurrent health: "
                  f"{self.player[num2].health}")
            time.sleep(0.7)
            if self.player[num2].health == 0:
                self.nearly_dead(num2)

    def peach(self, num): # num: the player who uses the peach
        """
        This is the peach method, num is a integer that represents the 
        player number the method is called when the player uses a peach
        """
        target = f"Player {num+1} uses" if num != 0 else "You use"
        self.player[num].health += 1
        self.player[num].max_handcards += 1
        print(f"{target} a peach and gained one health point...")
        print(f"Current health: {self.player[num].health}")
        time.sleep(0.7)
        for i in range(1, len(self.player)):
            if i == num or not self.player[i].alive:
                continue
            self.player[i].enemy[num]["estimated_handcards"]["peach"] -= 1 
            # update bot's prediction
            self.player[i].enemy[num]["handcard_num"] -= 1
            if self.player[i].enemy[num]["estimated_handcards"]["peach"] < 0:
                print("**ERROR: 2function-peach<0**")
   
    def duel(self, num1, num2, human):
        """
        This is the duel method, it is called when one player uses duel
        Perimeters description:
        num1: the player that starts the duel
        num2: the player that is being targeted by the duel
        human = 1: num1 is human, human = -1: num2 is human, 
        human = 0: two AI dueling
        This is a recursive function, because the two players needs 
        to play slash one by one,
        so the method calls itself and switch num1 and num2 and human 
        value accordingly. 
        """
        # num1 is the initiator of duel
        # num2 is the target who needs to respond first 
        # Check if target player (num2) has slash
        find_slash = -1
        for i in range(len(self.player[num2].handcards)):
            if self.player[num2].handcards[i].name == "slash":
                find_slash = i
                break
        if num2 == 0:
            player_name = "You"
        else:
            player_name = f"Player {num2+1}"    
        print(f"{player_name}'s turn:")
        time.sleep(0.5)
        # If no slash found, player loses health and duel ends
        if find_slash == -1:
            print(f"{player_name} don't have any slashes and loses one "
                  "health point\nDuel ends")
            time.sleep(1.5)
            self.player[num2].health -= 1    
            for i in range(1, len(self.player)):
                if i == num2 or not self.player[i].alive:
                    continue
                self.player[i].enemy[num2]["health"] -= 1 
                # update bot's prediction  
            self.player[num2].max_handcards -= 1
            if self.player[num2].health == 0:
                self.nearly_dead(num2)
            return
        # Player has slash - now decide whether to play it
        play_slash = False   
        if human == -1:  # num2 is human
            choice = choose("Do you choose to play a [slash]?(y/n)",
                            ["yes", 'y', "no", 'n'])
            if choice in ['y', "yes"]:
                play_slash = True
        elif human == 1:  
            # num1 is human (but we're checking num2, so num2 is AI)
            # AI always plays slash if available
            play_slash = True
        else:  # human == 0, both are AI
            # AI always plays slash if available
            play_slash = True
        if play_slash:
            print(f"{player_name} played a [slash]")
            time.sleep(0.7)
            self.player[num2].handcards.pop(find_slash)
            for i in range(1, len(self.player)):
                if i == num2 or not self.player[i].alive:
                    continue
                self.player[i].enemy[num2]["estimated_handcards"]\
                    ["slash"] -= 1 # update bot's prediction
                self.player[i].enemy[num2]["handcard_num"] -= 1
                if self.player[i].enemy[num2]["estimated_handcards"]\
                    ["slash"] < 0:
                    print("**ERROR: function-duel-slash<0**")
            # Continue duel - now num1's turn (swap positions)
            self.duel(num2, num1, -human if human != 0 else 0)
        else:
            # Player chose not to play slash, loses health
            print(f"{player_name} chose not to play a slash and loses "
                  "one health point\nDuel ends")
            self.player[num2].health -= 1
            for i in range(1, len(self.player)):
                if i == num2 or not self.player[i].alive:
                    continue
                self.player[i].enemy[num2]["health"] -= 1 
                # update bot's prediction
            self.player[num2].max_handcards -= 1
            if self.player[num2].health == 0: 
                # checks if player is nearly dead
                self.nearly_dead(num2)

    def dismantle(self, num1, num2, human):
        """
        This is the dismantle method.
        Perimeter explanations:
        num1: the player that uses dismantle
        num2: the player being targeted at
        human = 1: human dismantle AI| -1:AI dismantle human| 
        0: two AI The method checks if num2 has negate and asks which 
        card num1 wants to dismantle
        """
        if human <= 0: # AI dismantle human or AI
            if not self.player[num2].equipment["weapen"] is None:
                if human == 0:
                    player = f"player {num2+1}"
                if human == -1:
                    player = f"you"
                print(f"The card player Player {num1+1} chose is "
                      f"[{self.player[num2].equipment['weapen'].name}]")
                print(f"[{self.player[num2].equipment['weapen'].name}] "
                      f"dismantled from {player}")
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["equipment"]["weapen"] = None
                    # update bot's prediction                    
                self.player[num2].equipment["weapen"] = None
            elif not self.player[num2].equipment["armor"] is None:
                if human == 0:
                    player = f"player {num2+1}"
                if human == -1:
                    player = f"you"
                print(f"The card player Player {num1+1} chose is "
                      "[{self.player[num2].equipment['armor'].name}]")
                print(f"[{self.player[num2].equipment['armor'].name}] "
                      "dismantled from {player}")
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["equipment"]["armor"] = None 
                    # update bot's prediction                    
                self.player[num2].equipment["armor"] = None
            else:
                random_index = random.randint(0, 
                                    len(self.player[num2].handcards)-1)
                card_choice = self.player[num2].handcards[random_index]
                print(f"The card Player {num1+1} chose is {card_choice.name}")
                print(f"[{card_choice.name}] dismantled...")
                self.player[num2].handcards.pop(random_index)
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["estimated_handcards"]\
                        [card_choice.name] -= 1 # update bot's prediction
                    self.player[i].enemy[num2]["handcard_num"] -= 1
        else: # human dismantle AI
            print(f"Player {num2 + 1} has {len(self.player[num2].handcards)} "
                   "handcards, which one do you want to dismantle?")
            valid_choice = []
            for i in range(len(self.player[num2].handcards)):
                print(f"{i+1}. [xxx]")
                valid_choice.append(str(i+1))

            weapen_name = "Not equipped" if self.player[num2].equipment\
                ['weapen'] is None else self.player[num2].\
                    equipment['weapen'].name
            armor_name = "Not equipped" if self.player[num2].\
                equipment['armor'] is None else self.player[num2].\
                    equipment['armor'].name
            print("Equipment:")
            if weapen_name != "Not equipped":
                print(f"Weapen: {int(valid_choice[-1])+1}. {weapen_name}")
                valid_choice.append(str(int(valid_choice[-1])+1))
            else:
                print(f"Weapen: {weapen_name}")
            if armor_name != "Not equipped":
                print(f"Armor: {int(valid_choice[-1])+1}. {armor_name}")
                valid_choice.append(str(int(valid_choice[-1])+1))
            else:
                print(f"Armor: {armor_name}")
            card_choice = int(choose("Choice: ", valid_choice)) 
            if card_choice == len(self.player[num2].handcards)+1 and \
                weapen_name != "Not equipped":
                print(f"[{weapen_name}] dismantled from player {num2+1}")
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["equipment"]["weapen"] = None 
                    # update bot's prediction
                self.player[num2].equipment["weapen"] = None  
                return
            elif card_choice == len(self.player[num2].handcards)+1 \
                and weapen_name == "Not equipped" or card_choice == \
                    len(self.player[num2].handcards)+2:
                print(f"[{armor_name}] dismantled from player {num2+1}")
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["equipment"]["armor"] = None 
                    # update bot's prediction
                self.player[num2].equipment["armor"] = None  
                return
            card_choice -= 1 # 0-indexed
            random_select = random.randint(0, 
                    len(self.player[num2].handcards)-1)#index
            selected_card = self.player[num2].handcards[random_select]#object
            time.sleep(0.7)
            print(f"The card you chose is [{selected_card.name}]\n"
                  f"[{selected_card.name}] discarded from player {num2+1}...")
            # add time.sleep
            self.player[num2].handcards.pop(random_select)
            # update enemy handcard
            for i in range(1, len(self.player)):
                if i == num2 or not self.player[i].alive:
                    continue
                self.player[i].enemy[num2]["estimated_handcards"]\
                    [selected_card.name] -= 1 # update bot's prediction
                self.player[i].enemy[num2]["handcard_num"] -= 1
                if self.player[i].enemy[num2]["estimated_handcards"]\
                    [selected_card.name] < 0:
                    print("**ERROR: dismantle<0**")

    def snatch(self, num1, num2, human): 
        """This is the snatch method
        Perimeters explanation:
        num1: the player who played snatch
        num2: the player who is targeted by
        human = 1: human snatch AI| -1:AI snatch human| 0: two AI 
        The method works basically the same as dismantle but it 
        adds the cards player
        num1 snatches to its handcards."""
        if human <= 0: # AI dismantle human or AI
            if not self.player[num2].equipment["weapen"] is None:
                print(f"The card player Player {num1+1} chose is "
                      f"[{self.player[num2].equipment['weapen'].name}]")
                print(f"[{self.player[num2].equipment['weapen'].name}] "
                      f"added to Player {num1+1}'s handcards")
                self.player[num1].handcards.append(self.player[num2].\
                                                   equipment["weapen"])
                for i in range(1, len(self.player)):
                    # player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["equipment"]["weapen"] = \
                        None # update bot's prediction
                for i in range(1, len(self.player)):# player[num1]
                    if i == num1 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num1]["estimated_handcards"]\
                        [self.player[num2].equipment["weapen"].name] += 1 
                    # update bot's prediction
                    self.player[i].enemy[num1]["handcard_num"] += 1      
                self.player[num2].equipment["weapen"] = None
            elif not self.player[num2].equipment["armor"] is None:
                print(f"The card player Player {num1+1} chose is "
                      f"[{self.player[num2].equipment['armor'].name}]")
                print(f"[{self.player[num2].equipment['armor'].name}] "
                      f"added to Player {num1+1}'s handcards")
                self.player[num1].handcards.append(self.player[num2].\
                                                   equipment["armor"])
                for i in range(1, len(self.player)):
                    # player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["equipment"]["armor"] = None 
                    # update bot's prediction
                for i in range(1, len(self.player)):# player[num1]
                    if i == num1 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num1]["estimated_handcards"]\
                        [self.player[num2].equipment["armor"].name] += 1 
                    # update bot's prediction
                    self.player[i].enemy[num1]["handcard_num"] += 1                
                self.player[num2].equipment["armor"] = None
            else: # human dismantle AI
                random_index = random.randint(0, len(self.player[num2].\
                                                     handcards)-1)
                card_choice = self.player[num2].handcards[random_index]
                print(f"The card Player {num1+1} chose is {card_choice.name}")
                print(f"[{card_choice.name}] added to Player {num1+1}'s "
                      "handcards")
                self.player[num1].handcards.append(card_choice)
                self.player[num2].handcards.pop(random_index)
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["estimated_handcards"]\
                        [card_choice.name] -= 1 # update bot's prediction
                    self.player[i].enemy[num2]["handcard_num"] -= 1
                for i in range(1, len(self.player)):# player[num1] gain a card
                    if i == num1 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num1]["estimated_handcards"]\
                        [card_choice.name] += 1 # update bot's prediction
                    self.player[i].enemy[num1]["handcard_num"] += 1
        else:
            print(f"Player {num2 + 1} has {len(self.player[num2].handcards)} "
                  "handcards, which one do you want to snatch?")
            valid_choice = []
            for i in range(len(self.player[num2].handcards)):
                print(f"{i+1}. [xxx]")
                valid_choice.append(str(i+1))
            weapen_name = "Not equipped" if self.player[num2].\
                equipment['weapen'] is None else self.player[num2].\
                    equipment['weapen'].name
            armor_name = "Not equipped" if self.player[num2].\
                equipment['armor'] is None else self.player[num2].\
                    equipment['armor'].name
            print("Equipment:")
            if weapen_name != "Not equipped":
                print(f"Weapen: {int(valid_choice[-1])+1}. {weapen_name}")
                valid_choice.append(str(int(valid_choice[-1])+1))
            else:
                print(f"Weapen: {weapen_name}")
            if armor_name != "Not equipped":
                print(f"Armor: {int(valid_choice[-1])+1}. {armor_name}")
                valid_choice.append(str(int(valid_choice[-1])+1))
            else:
                print(f"Armor: {armor_name}")
            card_choice = int(choose("Choice: ", valid_choice)) # 0 indexed
            if card_choice == len(self.player[num2].handcards)+1 \
                and weapen_name != "Not equipped":
                print(f"[{weapen_name}] added to you handcards")
                self.player[num1].equipment["weapen"] = \
                    self.player[num2].equipment["weapen"]
                for i in range(1, len(self.player)):# player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["equipment"]["weapen"] \
                        = None # update bot's prediction     
                for i in range(1, len(self.player)): 
                    # player[num1] gained one card
                    if i == num1 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num1]["equipment"]["weapen"] \
                        = self.player[num2].equipment["weapen"]  
                    # update bot's prediction
                self.player[num2].equipment["weapen"] = None  
                return
            elif card_choice == len(self.player[num2].handcards)+1 \
                and weapen_name == "Not equipped" or card_choice == \
                    len(self.player[num2].handcards)+2:
                print(f"[{armor_name}] added to you handcards")
                self.player[num1].equipment["armor"] = \
                    self.player[num2].equipment["armor"]
                for i in range(1, len(self.player)):
                    # player[num2] lost a card
                    if i == num2 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num2]["equipment"]["armor"] = \
                        None # update bot's prediction             
                for i in range(1, len(self.player)): 
                    # player[num1] gained one card
                    if i == num1 or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num1]["estimated_handcards"]\
                        [self.player[num2].equipment["armor"].name] += 1 \
                            # update bot's prediction
                self.player[num2].equipment["armor"] = None  
                return
            #random_select = random.randint(0, 
            # len(self.player[num2].handcards)-1)#index
            card_choice -= 1
            selected_card = self.player[num2].handcards[card_choice] #object
            time.sleep(0.7)
            print(f"The card you chose is [{selected_card.name}]\n"
                  f"[{selected_card.name}] added to your handcards")
            time.sleep(0.7)
            self.player[num1].add_handcards([selected_card])
            self.player[num2].handcards.pop(card_choice)
            # update enemy handcard
            for i in range(1, len(self.player)):# player[num2] lost a card
                if i == num2 or not self.player[i].alive:
                    continue
                self.player[i].enemy[num2]["estimated_handcards"]\
                    [selected_card.name] -= 1 # update bot's prediction
                self.player[i].enemy[num2]["handcard_num"] -= 1
                if self.player[i].enemy[num2]["estimated_handcards"]\
                    [selected_card.name] < 0:
                    print("**ERROR: snatch1<0**")
            for i in range(1, len(self.player)): 
                # player[num1] gained one card
                if i == num1 or not self.player[i].alive:
                    continue
                self.player[i].enemy[num1]["estimated_handcards"]\
                    [selected_card.name] += 1 # update bot's prediction
                self.player[i].enemy[num1]["handcard_num"] += 1
                if self.player[i].enemy[num1]["estimated_handcards"]\
                    [selected_card.name] < 0:
                    print("**ERROR: snatch2<0**")         

    def archery(self, num, human):
        """
        This is the archery method
        Perimeter explanations:
        num: the player who played  archery
        human=1: player is the card user, human = 0: AI played the card
        the method checks all players except the player who 
        played the card for dodge and negate
        """
        for i in range(0, len(self.player)):
            if i == num or not self.player[i].alive:
                continue
            if i == 0:
                find_dodge = -1 # look for dodge and negate
                find_negate = -1
                for j in range(len(self.player[0].handcards)):
                    if self.player[0].handcards[j].name == "dodge":
                        find_dodge = j
                    if self.player[0].handcards[j].name == "negate":
                        find_negate = j
                if find_dodge == -1 and find_negate == -1:
                    print("You don't have a dodge or negate, you "
                          "lose one health point...")
                    self.player[0].health -= 1
                    for j in range(1, len(self.player)):
                        if j == 0 or not self.player[j].enemy[0]["alive"]:
                            continue
                        self.player[j].enemy[0]["health"] -= 1 
                        # update bot's prediction]
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
                    output += f"{n}. pass (lose one health point)"
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
                                if j == num or not self.player[j].enemy[0]\
                                    ["alive"]:
                                    continue
                                self.player[j].enemy[0]\
                                    ["estimated_handcards"]["dodge"] -= 1 
                                # update bot's prediction
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]\
                                    ["estimated_handcards"]["dodge"] < 0:
                                    print("**ERROR: "
                                          "archery-player1-dodge<0**")
                            self.player[0].handcards.pop(find_dodge)
                        else: # must be negate
                            print("You played negate and countered archery")
                            for j in range(1, len(self.player)):
                                if j == num or not self.player[j].enemy[0]\
                                    ["alive"]:
                                    continue
                                self.player[j].enemy[0]\
                                    ["estimated_handcards"]["negate"] -= 1 
                                # update bot's prediction
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]\
                                    ["estimated_handcards"]["negate"] < 0:
                                    print("**ERROR: archery-"
                                          "player1-negate<0**")
                            self.player[0].handcards.pop(find_negate)
                    elif (choice == 2 and find_dodge*find_negate < 0) \
                        or choice == 3: # pass
                        #choice == n+1 must be pass; If the two 
                        # indexes multiply to be negative, one of 
                        # them must be -1, then choice == 2 is pass
                        print("You choose to pass and lose one health point")
                        self.player[0].health -= 1
                        for j in range(1, len(self.player)):
                            if j == 0 or not self.player[j].enemy[0]["alive"]:
                                continue
                            self.player[j].enemy[0]["health"] -= 1 
                            # update bot's prediction]
                        self.player[0].max_handcards -= 1
                        if self.player[0].health == 0:
                            self.nearly_dead(0)
                    else:#play negate
                        print("You played negate and countered archery")         
                        for j in range(1, len(self.player)):
                            if j == num or not self.player[j].enemy[0]\
                                ["alive"]:
                                continue
                            self.player[j].enemy[0]["estimated_handcards"]\
                                ["negate"] -= 1 # update bot's prediction
                            self.player[j].enemy[0]["handcard_num"] -= 1
                            if self.player[j].enemy[0]["estimated_handcards"]\
                                ["negate"] < 0:
                                print("**ERROR: archery-player1-negate<0**")
                        self.player[0].handcards.pop(find_negate)
            else:# AI
                lose_health = True
                find_negate = self.findNegate(i)
                count_dodge = self.countDodge(i)
                find_dodge = self.findDodge(i)
                if count_dodge >= 2:
                    print(f"Player {i+1} played [dodge]")
                    self.playDodge(i, find_dodge)
                    lose_health = False
                elif find_negate != -1 and self.player[i].health <= 2:
                    self.playNegate(i, find_negate)
                    print(\
                        f"Player {i+1} played [negate] to counter [archery]")
                    lose_health = False
                else:
                    if find_dodge != -1:
                        self.playDodge(i, find_dodge)
                        print(f"Player {i+1} played [dodge]")
                        lose_health = False
                    elif find_negate != -1:
                        self.playNegate(i, find_negate)
                        print(f"Player {i+1} played [negate] to counter "
                              f"[archery]")
                        lose_health = False
                if lose_health:
                    print(f"Player {i+1} doesn't have a dodge or negate "
                          "and loses one health point")
                    self.player[i].health -= 1
                    for j in range(1, len(self.player)):
                        if j == i or not self.player[j].enemy[0]["alive"]:
                            continue
                        self.player[j].enemy[i]["health"] -= 1 
                        # update bot's prediction]
                    self.player[i].max_handcards -= 1
                    if self.player[i].health == 0:
                        self.nearly_dead(i)

    def savage(self, num, human):
        """
        This is the savage method
        num is the index of the player who played the card
        human=1: player is the card user, human = 0: AI played 
        the card the method works basically the same as archery, 
        but it checks for slash instead of dodge
        """
        for i in range(0, len(self.player)):
            if i == num or not self.player[i].alive:
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
                    print("You don't have a slash or negate, you lose one "
                          "health point...")
                    self.player[0].health -= 1
                    for j in range(1, len(self.player)):
                        if j == 0 or not self.player[j].enemy[0]["alive"]:
                            continue
                        self.player[j].enemy[0]["health"] -= 1 
                        # update bot's prediction]
                    self.player[0].max_handcards -= 1
                    if self.player[0].health == 0:
                        self.nearly_dead(0)
                else:
                    n = 1
                    output = f"What do you choose to play:\n"
                    if find_slash != -1:
                        output += f"{n}. slash\n"
                        n += 1
                    if find_negate != -1:
                        output += f"{n}. negate\n"
                        n += 1
                    output += f"{n}. pass(lose one health point)"
                    n += 1
                    print(output)
                    valid_choice = []
                    for j in range(1, n):
                        valid_choice.append(str(j))
                    choice = int(choose("Choice: ", valid_choice))
                    if choice == 1:
                        if find_slash != -1: # play slash             
                            print("You played a slash")         
                            for j in range(1, len(self.player)):
                                if j == num or not self.player[j].enemy[0]\
                                    ["alive"]:
                                    continue
                                self.player[j].enemy[0]\
                                    ["estimated_handcards"]["slash"] -= 1 
                                # update bot's prediction
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]\
                                    ["estimated_handcards"]["slash"] < 0:
                                    print("**ERROR: savage-player1-slash<0**")
                            self.player[0].handcards.pop(find_slash)
                        else: # must be negate
                            print("You played negate and countered savage")         
                            for j in range(1, len(self.player)):
                                if j == num or not self.player[j].enemy[0]\
                                    ["alive"]:
                                    continue
                                self.player[j].enemy[0]\
                                    ["estimated_handcards"]["negate"] -= 1 
                                # update bot's prediction
                                self.player[j].enemy[0]["handcard_num"] -= 1
                                if self.player[j].enemy[0]\
                                    ["estimated_handcards"]["negate"] < 0:
                                    print("**ERROR: savage-player1-"
                                          "negate<0**")
                            self.player[0].handcards.pop(find_negate)
                    elif (choice == 2 and find_slash*find_negate < 0) or \
                        choice == 3: # pass
                        #choice == n+1 must be pass; 
                        # If the two indexes multiply to be negative, 
                        # one of them must be -1, then choice == 2 is pass
                        print("You choose to pass and lose one health point")
                        self.player[0].health -= 1
                        for j in range(1, len(self.player)):
                            self.player[j].enemy[0]["health"] -= 1 
                            # update bot's prediction]
                        self.player[0].max_handcards -= 1
                        if self.player[0].health == 0:
                            self.nearly_dead(0)
                    else:#play negate
                        print("You played negate and countered savage")         
                        for j in range(1, len(self.player)):
                            self.player[j].enemy[0]["estimated_handcards"]\
                            ["negate"] -= 1 # update bot's prediction
                            self.player[j].enemy[0]["handcard_num"] -= 1
                            if self.player[j].enemy[0]["estimated_handcards"]\
                            ["negate"] < 0:
                                print("**ERROR: savage-player1-negate<0**")
                        self.player[0].handcards.pop(find_negate)
            else: # AI
                lose_health = True
                find_negate = self.findNegate(i)
                count_slash = self.countSlash(i)
                find_slash = self.findSlash(i)
                if count_slash >= 2:
                    print(f"Player {i+1} played [slash]")
                    self.playSlash(i, find_slash)
                    lose_health = False
                elif find_negate != -1 and self.player[i].health <= 2:
                    self.playNegate(i, find_negate)
                    print(f"Player {i+1} played [negate] to counter [savage]")
                    lose_health = False
                else:
                    if find_slash != -1:
                        self.playSlash(i, find_slash)
                        print(f"Player {i+1} played [slash]")
                        lose_health = False
                    elif find_negate != -1:
                        self.playNegate(i, find_negate)
                        print(f"Player {i+1} played [negate] to counter "
                              f"[savage]")
                        lose_health = False
                if lose_health:
                    print(f"Player {i+1} doesn't have a slash or negate and " 
                          "loses one health point")
                    self.player[i].health -= 1
                    for j in range(1, len(self.player)):
                        if j == i or not self.player[j].enemy[0]["alive"]:
                            continue
                        self.player[j].enemy[i]["health"] -= 1 
                        # update bot's prediction]
                    self.player[i].max_handcards -= 1
                    if self.player[i].health == 0:
                        self.nearly_dead(i)
                
    def benevolence(self, num, human):
        """
        This the benevolence method
        num is the index of the player who played the card
        human is if num is human or not, is a number between 
        0 and 1
        """
        string = "You" if human != 0 else f"Player {num+1}"
        print(f"{string} drew two cards from the deck of cards...")
        self.draw_cards(num)
        if not self.running:
            self.result = True
            print("You fought to the end, there are no cards left.\n"
                  "The judge came and decided you are the winner...")
            return
        
    def negate(self):
        """
        only can be used when the player is targeted by a trick card. 
        Is considered in other methods, nothing here
        """
        pass
    
    def findDodge(self, num):
        """
        num is the index of the player being checked
        This method finds if player num has any dodge
        it returns the last index of dodge of the chosen player
        id no dodge is found, it returns -1
        """
        find_dodge = -1
        for j in range(len(self.player[num].handcards)):
            if self.player[num].handcards[j].name == "dodge":
                find_dodge = j
        return find_dodge
        
    def countDodge(self, num):
        """
        num is the index of the player being counted 
        the method counts the number of dodge the player 
        has and returns the number of dodge
        """
        count_dodge = 0
        for j in range(len(self.player[num].handcards)):
            if self.player[num].handcards[j].name == "dodge":
                count_dodge += 1
        return count_dodge
    
    def playDodge(self, num, index):
        """
        This method has two perimeters: 
        num is the index of player who played the dodge
        index if the index of the dodge in the player's handcards
        the method removes the dodge from the player's handcards and
        update robot prediction
        """
        for i in range(1, len(self.player)):                            
            if i == num or not self.player[i].alive:
                continue
            self.player[i].enemy[num]["estimated_handcards"]["dodge"] -= 1 
            # update bot's prediction
            self.player[i].enemy[num]["handcard_num"] -= 1
        self.player[num].handcards.pop(index)

    def countSlash(self, num):
        """
        This method has a perimeter num, which is the index 
        of the player being checked.
        it returns the number of slashed the player has
        """
        count_slash = 0
        for j in range(len(self.player[num].handcards)):
            if self.player[num].handcards[j].name == "slash":
                count_slash += 1
        return count_slash
    
    def findSlash(self, num):
        """
        This method finds if player num has any slashes.
        it returns th last index of slash in the players handcards.
        num is the perimeter of the index of the player
        """
        find_slash = -1
        for j in range(len(self.player[num].handcards)):
            if self.player[num].handcards[j].name == "slash":
                find_slash = j
        return find_slash
    
    def playSlash(self, num, index):
        """
        the method has two perimeters:
        num: the index of the player that played the slash
        index: the index of the slash in the list of handcards
        the method removes the slash from player nums handcards
        """
        for i in range(1, len(self.player)):                            
            if i == num or not self.player[i].alive:
                continue
            self.player[i].enemy[num]["estimated_handcards"]["slash"] -= 1 
                # update bot's prediction
            self.player[i].enemy[num]["handcard_num"] -= 1
        self.player[num].handcards.pop(index)
    
    def findNegate(self, num):
        """
        num is the index of the player being checked
        This method finds if player num has any slashed
        if there is it returns the last index of the negate card
        else it returns -1
        """
        find_negate = -1
        for j in range(len(self.player[num].handcards)):
            if self.player[num].handcards[j].name == "negate":
                find_negate = j
        return find_negate
        
    def playNegate(self, num, index):
        """
        This method has two perimeters:
        num if the index of the player that plays negate and index 
        if the index of the card in the list of handcards
        """
        for i in range(1, len(self.player)):                            
            if i == num or not self.player[i].alive:
                continue
            self.player[i].enemy[num]["estimated_handcards"]["negate"] -= 1 
            # update bot's prediction
            self.player[i].enemy[num]["handcard_num"] -= 1
        self.player[num].handcards.pop(index)

    def start_phase(self, num):
        """
        This methods deals with all the player movements in 
        start phase.
        num is a perimeter that represents the index of the player
        The method includes playing cards and calling other methods 
        function the game
        """
        if num == 0: # human's turn
            print("Your turn:")
            act_step = 1
            while True:
                if not self.running:
                    return
                self.print_handcards(num)
                print(f"Available moves:\n"
                      f"{len(self.player[num].handcards) + 1}. end turn")
                valid_choices = [str(i) for i in range(1, \
                                    len(self.player[num].handcards) + 2)]
                valid_choices.append("admin")
                valid_choices.append("q")
                valid_choices.append("w")
                choice = choose("Choice: ", valid_choices)
                while choice == 'q' or choice == 'w':
                    if choice == 'q':
                        self.print_rules(False)
                        for i in range(18):
                            print("\033[A\033[2K", end='')
                            # erase the previous line
                        choice = choose("Choice: ", valid_choices)
                    elif choice == 'w':
                        self.print_card_description(False)
                        for i in range(25):
                            print("\033[A\033[2K", end='')
                        choice = choose("Choice: ", valid_choices)
                # admin mode
                self.verify_admin_mode(choice)
                if choice == "end":
                    out = handleMidGameClose(self.player, self.money)
                    if out == True:
                        self.running = False
                        self.result = True
                        self.player[0].alive = True
                if not self.running:
                    return
                choice = int(choice)
                if choice == len(self.player[num].handcards) + 1:
                    print("Turn ended")
                    break
                choice -= 1 # 0 indexing
                chosen_card = self.player[num].handcards[choice]
                if chosen_card.type == "basic": # basic cards
                    if chosen_card.name == "slash":
                        has_crossbow = (self.player[num].\
                        equipment["weapen"] is not None and \
                            self.player[num].equipment["weapen"].name \
                                == "crossbow")
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
                        choice_p = int(choose("Choice: ", valid_choices)) - 1 
                        # 0 indexing
                        print(f"You attacked player {choice_p+1}")
                        for i in range(1, len(self.player)):                            
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                ["slash"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"]["slash"] < 0:
                                print("**ERROR: "
                                      "1function-start_phase-slash<0**")
                        self.player[num].handcards.pop(choice)
                        time.sleep(0.7)
                        self.attack(num, choice_p, 1)
                        act_step -= 1
                    if chosen_card.name == "peach":
                        if self.player[num].health == self.player[num].\
                            initial_health: # temporary be 4
                            print("**You are already at maximum health**")
                        else:
                            self.peach(num)
                            self.player[num].handcards.pop(choice)
                    if chosen_card.name == "dodge":
                        print("**You can only use [dodge] when another "
                              "player attacks you**")
                if chosen_card.type == "equipment": # equipment cards
                    if chosen_card.name in ["crossbow", "crossblade"]:
                        if self.player[num].equipment["weapen"] is None:
                            self.player[num].equipment["weapen"] = \
                                chosen_card
                            print(f"You successfully equiped "
                                  f"{chosen_card.name}")
                            for i in range(1, len(self.player)):     
                                if i == num or not self.player[i].alive:
                                    continue
                                self.player[i].enemy[num]\
                                    ["estimated_handcards"]\
                                        [chosen_card.name] -= 1 
                                # update bot's prediction
                                self.player[i].enemy[num]["handcard_num"] -= 1
                                self.player[i].enemy[num]["equipment"]\
                                    ["weapen"] = chosen_card
                                if self.player[i].enemy[num]\
                                    ["estimated_handcards"]\
                                        [chosen_card.name] < 0:
                                    print("**ERROR: 3function-start_"
                                          "phase-equipment<0**")
                            self.player[num].handcards.pop(choice)
                        else:
                            equiped_card_name = self.player[num].\
                                equipment["weapen"].name
                            replace_choice = \
                                choose(f"You have already "
                                f"equiped {equiped_card_name}, "
                                "do you want to replace"
                                f"it? y/n\n({equiped_card_name}"
                                "will be automatically "
                                "discarded)?\nChoice: ")
                            if replace_choice.lower() in ['y', 'yes']:
                                self.player[num].equipment["weapen"] = \
                                    chosen_card
                                print(f"You successfully equiped "
                                      f"{chosen_card.name}")
                                for i in range(1, len(self.player)):
                                    if i == num or not self.player[i].alive:
                                        continue
                                    self.player[i].enemy[num]\
                                        ["estimated_handcards"]\
                                            [chosen_card.name] -= 1 
                                    # update bot's prediction
                                    self.player[i].enemy[num]\
                                        ["handcard_num"] -= 1
                                    self.player[i].enemy[num]["equipment"]\
                                        ["weapen"] = chosen_card
                                    if self.player[i].enemy[num]\
                                        ["estimated_handcards"]\
                                            [chosen_card.name] < 0:
                                        print("**ERROR: 3function-"
                                              "start_phase-equipment<0**")
                                self.player[num].handcards.pop(choice)
                    elif chosen_card.name in ["evasion"]:  # armor
                        if self.player[num].equipment["armor"] is None:
                            self.player[num].equipment["armor"] = chosen_card
                            print(f"You successfully equiped "
                                  f"{chosen_card.name}")
                            for i in range(1, len(self.player)):
                                if i == num or not self.player[i].alive:
                                    continue
                                self.player[i].enemy[num]\
                                    ["estimated_handcards"]\
                                        [chosen_card.name] -= 1
                                self.player[i].enemy[num]["handcard_num"] -= 1
                                self.player[i].enemy[num]["equipment"]\
                                    ["armor"] = chosen_card
                                if self.player[i].enemy[num]\
                                    ["estimated_handcards"]\
                                        [chosen_card.name] < 0:
                                    print("**ERROR: function-"
                                          "start_phase-armor<0**")
                            self.player[num].handcards.pop(choice)
                        else:
                            equiped_armor_name = self.player[num].\
                                equipment["armor"].name
                            replace_choice = choose("You have already "
                                                    "equiped "
                                                    f"{equiped_armor_name}, "
                                                    "do you want to" 
                                                    "replace it? y/n\n"
                                                    f"({equiped_armor_name} "
                                                    "will be automatically "
                                                    "discarded)?\nChoice: ")
                            if replace_choice.lower() in ['y', 'yes']:
                                self.player[num].equipment["armor"] = \
                                    chosen_card
                                print(f"You successfully equiped "
                                      f"{chosen_card.name}")
                                for i in range(1, len(self.player)):
                                    if i == num or not self.player[i].alive:
                                        continue
                                    self.player[i].enemy[num]\
                                        ["estimated_handcards"]\
                                            [chosen_card.name] -= 1
                                    self.player[i].enemy[num]\
                                        ["handcard_num"] -= 1
                                    self.player[i].enemy[num]\
                                        ["equipment"]["armor"] = chosen_card
                                    if self.player[i].enemy[num]\
                                        ["estimated_handcards"]\
                                            [chosen_card.name] < 0:
                                        print("**ERROR: function-"
                                              "start_phase-armor<0**")
                                self.player[num].handcards.pop(choice)
                if chosen_card.type == "trick": # trick cards
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
                        player_choice = int(choose(output, \
                                        valid_choices)) - 1 # 0-indexed
                        index = self.findNegate(player_choice)
                        if  index != -1 and (self.findSlash\
                                             (player_choice) < 2 or \
                                                self.player[player_choice].\
                                                    health <= 2):
                            print\
                                (f"Player {player_choice+1} player [negate] \
                                  to counter your [duel]")
                            time.sleep(0.7)
                            self.playNegate(player_choice, index)
                        else:
                            print(f"You dueled with player {player_choice+1}")
                            time.sleep(0.7)
                            print("     **[DUEL]**")
                            self.duel(num, player_choice, 1)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                ["duel"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"]["duel"] < 0:
                                print("**ERROR: 4function-"
                                      "start_phase-duel<0**")
                        self.player[num].handcards.pop(choice)
                    if card_name == "dismantle":
                        find_handcards = 0
                        for i in range(1, len(self.player)):
                            if len(self.player[i].handcards) > 0 or \
                                self.player[i].equipment["weapen"] is \
                                    not None or \
                            self.player[i].equipment["armor"] is not None:
                                find_handcards += 1
                        if find_handcards == 0:
                            print("**There are no cards for you to snatch**")
                            time.sleep(0.7)
                        else:
                            output = "Who's card do you want to dismantle?"
                            alive_targets = []
                            for i in range(1, len(self.player)):
                                if self.player[i].alive:
                                    output += f"\n- player {i+1}"
                                    alive_targets.append(i + 1)
                            output += "\n"
                            valid_choices = [str(t) for t in alive_targets]
                            while True:
                                player_choice = int(choose(output, \
                                                           valid_choices)) - 1
                                if len(self.player[player_choice].\
                                       handcards) == 0:
                                    print(f"Player {player_choice+1} "
                                          "has 0 handcards, choose another "
                                          "player")
                                else:
                                    break
                            index = self.findNegate(player_choice)
                            if  index != -1:
                                print(f"Player {player_choice+1} used "
                                      "[negate] to counter your [dismantle]")
                                time.sleep(0.7)
                                self.playNegate(player_choice, index)
                            else:
                                self.dismantle(num, player_choice, 1)
                            for i in range(1, len(self.player)):
                                if i == num or not self.player[i].alive:
                                    continue
                                self.player[i].enemy[num]\
                                    ["estimated_handcards"]["dismantle"] \
                                        -= 1 # update bot's prediction
                                self.player[i].enemy[num]["handcard_num"] -= 1
                                if self.player[i].enemy[num]\
                                    ["estimated_handcards"]["dismantle"] < 0:
                                    print("**ERROR: start-phase-"
                                          "dismantle<0**")
                            self.player[num].handcards.pop(choice)
                    if card_name == "snatch":
                        find_handcards = 0
                        for i in range(1, len(self.player)):
                            if len(self.player[i].handcards) > 0 or \
                                self.player[i].equipment["weapen"] is \
                                    not None or \
                            self.player[i].equipment["armor"] is not None:
                                find_handcards += 1
                        if find_handcards == 0:
                            print("**There are no cards for you to snatch**")
                            time.sleep(0.7)
                        else:
                            output = "Who's card do you want to snatch?"
                            alive_targets = []
                            for i in range(1, len(self.player)):
                                if self.player[i].alive:
                                    output += f"\n- player {i+1}"
                                    alive_targets.append(i + 1)
                            output += "\n"
                            valid_choices = [str(t) for t in alive_targets] 
                            while True:
                                player_choice = int(choose(output, \
                                                           valid_choices)) - 1
                                if len(self.player[player_choice].\
                                       handcards) == 0:
                                    print(f"Player {player_choice+1} "
                                          "has 0 handcards, choose another "
                                          "player")
                                else:
                                    break
                            index = self.findNegate(player_choice)
                            if  index != -1:
                                print(f"Player {player_choice+1} used "
                                      "[negate] to counter your [snatch]")
                                time.sleep(0.7)
                                self.playNegate(player_choice, index)
                            else:
                                self.snatch(num, player_choice, 1)
                            for i in range(1, len(self.player)):
                                if i == num or not self.player[i].alive:
                                    continue
                                self.player[i].enemy[num]\
                                    ["estimated_handcards"]["snatch"] \
                                        -= 1 # update bot's prediction
                                self.player[i].enemy[num]["handcard_num"] -= 1
                                if self.player[i].enemy[num]\
                                    ["estimated_handcards"]["snatch"] < 0:
                                    print("**ERROR: start-phase-snatch<0**")
                            self.player[num].handcards.pop(choice)
                    # archery trick card
                    if card_name == "archery":
                        self.archery(num, 1)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                ["archery"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                            ["estimated_handcards"]["archery"] < 0:
                                print("**ERROR: start-phase-archery<0**")
                        self.player[num].handcards.pop(choice)
                    # savage trick card
                    if card_name == "savage":
                        self.savage(num, 1)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                ["savage"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"]["savage"] < 0:
                                print("**ERROR: start-phase-savage<0**")
                        self.player[num].handcards.pop(choice)
                    # benevolence trck card
                    if card_name == "benevolence":
                        self.benevolence(num, 1)
                        if not self.running:
                            return
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]\
                                ["estimated_handcards"]["benevolence"] \
                                    -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"]["benevolence"] < 0:
                                print("**ERROR: start-phase-benevolence<0**")
                        self.player[num].handcards.pop(choice)
                    if card_name == "negate":
                        print("**You can only use [negate] when another "
                              "player use a trick card on you**")
        else:
            print(f"Player {num+1}'s turn:")
            #initialise act_step
            self.player[num].act_step = 1
            while True:
                # Bot move
                action = self.player[num].take_move(self.player)
                if not self.running:
                    return
                if action == -1:
                    print(f"Player {num+1} end its turn...")
                    time.sleep(0.7)
                    break
                card = action["card"]
                if card.name == "slash":
                    target = f"player {action['target']+1}" if \
                        action['target'] != 0 else "you"
                    print(f"Player {num+1} attacks {target} with [slash]")
                    time.sleep(0.7)
                    if action["target"] == 0:
                        self.attack(num, action["target"], -1)
                    else:
                        self.attack(num, action["target"], 0)
                    for i in range(1, len(self.player)):
                        if i == num or not self.player[i].alive:
                            continue
                        self.player[i].enemy[num]["estimated_handcards"]\
                            [card.name] -= 1 # update bot's prediction
                        self.player[i].enemy[num]["handcard_num"] -= 1
                        self.player[i].enemy[num]["equipment"]["weapen"] \
                            = card.name
                        if self.player[i].enemy[num]["estimated_handcards"]\
                            [card.name] < 0:
                            print("**ERROR: 6function-start_phase-"
                            "AI-slash<0**")
                        self.player[num].handcards.pop(action["index"])
                if card.name == "peach":
                    self.peach(num)
                    # enemy estimation already updated in peach
                    self.player[num].handcards.pop(action["index"])
                if card.type == "equipment":
                    if card.name in ["crossbow", "crossblade"]:
                        extra = ""
                        if not self.player[num].equipment["weapen"] is None:
                            extra = \
                                f" and replaced \
                                [{self.player[num].equipment['weapen'].name}]"
                        self.player[num].equipment["weapen"] = card
                        print(f"Player {num+1} equiped [{card.name}]{extra}")
                        time.sleep(0.7)
                        for i in range(1, len(self.player)):                           
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                [card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            self.player[i].enemy[num]["equipment"]["weapen"] \
                                = card.name
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"]\
                                [card.name] < 0:
                                print("**ERROR: 6function-start_phase"
                                      "-AI-equipment<0**")
                        self.player[num].handcards.pop(action["index"])
                    elif card.name in ["evasion"]:  # armor
                        extra = ""
                        if not self.player[num].equipment["armor"] is None:
                            extra = " and replaced ["
                            + f"{self.player[num].equipment['armor'].name}]"
                        self.player[num].equipment["armor"] = card
                        print(f"Player {num+1} equiped [{card.name}]{extra}")
                        time.sleep(0.7)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                [card.name] -= 1
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            self.player[i].enemy[num]["equipment"]["armor"] \
                                = card
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"][card.name] < 0:
                                print("**ERROR: function-"
                                      "start_phase-AI-armor<0**")
                        self.player[num].handcards.pop(action["index"])
                if card.type == "trick":
                    if card.name == "savage":
                        print(f"Player {num+1} played [savage]")                        
                        time.sleep(0.7)
                        self.savage(num, 0)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                [card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 6function-"
                                      "start_phase-AI-equipment<0**")
                        self.player[num].handcards.pop(action["index"])
                    if card.name == "archery":
                        print(f"Player {num+1} played [archery]")
                        time.sleep(0.7)
                        self.archery(num, 0)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                [card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 6function-"
                                      "start_phase-AI-equipment<0**")
                        self.player[num].handcards.pop(action["index"])
                    if card.name == "benevolence":
                        print(f"Player {num+1} played [benevolence]")
                        time.sleep(0.7)
                        self.benevolence(num, 0)
                        if not self.running:
                            return
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                [card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 6function-"
                                      "start_phase-AI-benevolence<0**")
                        self.player[num].handcards.pop(action["index"])
                    if card.name == "snatch":
                        print(f"Player {num+1} played [snatch]")
                        time.sleep(0.7)
                        if action["target"] == 0:
                            index = self.findNegate(action["target"])
                            if  index != -1:
                                print(f"Player {num+1}"
                                      "choose to snatch your card")
                                time.sleep(0.7)
                                _input = choose("Do you choose to use [ne"
                                f"gate] to counter Player {num+1}'s snatch?")
                                time.sleep(0.7)
                                if _input.lower() in ['y', "yes"]:
                                    self.playNegate(0, index)
                                else:
                                    self.snatch(num, action["target"], -1)   
                            else:
                                self.snatch(num, action["target"], -1)
                        else:
                            print(f"Player {num+1} choose to snatch "
                                  f"Player {action['target']+1}'s card")
                            time.sleep(0.7)
                            index = self.findNegate(action["target"])
                            if index != -1:
                                print(f"Player {action['target']+1} "
                                    "playerd [negate] to counter "
                                        f"Player {num+1}'s snatch")
                                time.sleep(0.7)
                                self.playNegate(action["target"], index)
                            else:
                                self.snatch(num, action["target"], 0)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                [card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 7function-"
                                      "start_phase-AI-snatch<0**")
                        self.player[num].handcards.pop(action["index"])
                    if card.name == "dismantle":
                        print(f"Player {num+1} played [dismantle]")
                        time.sleep(0.7)
                        if action["target"] == 0:
                            index = self.findNegate(action["target"])
                            if index != -1:
                                print(f"Player {num+1} choose to "
                                    f"dismantle your card")
                                time.sleep(0.7)
                                _input = choose("Do you choose to use "
                                    f"[negate] to counter Player {num+1}"
                                    "'s dismantle?(y/n)")
                                if _input.lower() in ['y', "yes"]:
                                    self.playNegate(0, index)
                                else:
                                    self.dismantle(num, action["target"], -1)
                                time.sleep(0.7)
                            else:
                                self.dismantle(num, action["target"], -1)
                        else:
                            print(f"Player {num+1} choose to dismantle "
                                  f"Player {action['target']+1}'s card")
                            time.sleep(0.7)
                            index = self.findNegate(action["target"])
                            if index != -1:
                                print(f"Player {action['target']+1} "
                                    "playerd [negate] to counter Player "
                                        f"{num+1}'s snatch")
                                time.sleep(0.7)
                                self.playNegate(action["target"], index)
                            else:
                                self.dismantle(num, action["target"], 0)
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                [card.name] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"][card.name] < 0:
                                print("**ERROR: 8function-"
                                      "start_phase-AI-dismantle<0**")
                        self.player[num].handcards.pop(action["index"])
                    if card.name == "duel":
                        print(f"Player {num+1} played [duel] and challenged "
                              , end='')
                        if action["target"] == 0:
                            print("you")
                        else:
                            print(f"Player {action['target']}")
                        self.player[num].handcards.pop(action["index"])
                        for i in range(1, len(self.player)):
                            if i == num or not self.player[i].alive:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]\
                                ["duel"] -= 1 # update bot's prediction
                            self.player[i].enemy[num]["handcard_num"] -= 1
                            if self.player[i].enemy[num]\
                                ["estimated_handcards"]["duel"] < 0:
                                print("**ERROR: function-"
                                      "start_phase-duel<0**")
                        time.sleep(0.7)
                        if action["target"] == 0:
                            index = self.findNegate(action["target"])
                            if  index != -1:
                                _input = choose("Do you choose to use "
                                    "[negate] to counter "
                                    f"Player {num+1}'s duel?(y/n)")
                                if _input.lower() in ['y', "yes"]:
                                    self.playNegate(0, index)
                            else:
                                print("     **[DUEL]**")
                                self.duel(num, action["target"], -1)
                        else:
                            index = self.findNegate(action["target"])
                            if  index != -1 and (self.findSlash(action\
                                    ["target"]) < 2 or self.player[action\
                                    ["target"]].health <= 2):
                                print(f"Player {action['target']+1} "
                                    "used [negate] to counter Player"
                                    f" {num+1}'s [duel]")
                                time.sleep(0.7)
                                self.playNegate(action["target"], index)
                            else:
                                print("     **[DUEL]**")
                                self.duel(num, action["target"], 0)
            return

    def discard_phase(self, num):
        """
        num is the index of the player that is in discard phase
        This method operates the discards phase for player num.
        it checks the player health and max card nums
        """
        print("     [Discard phase]")
        time.sleep(0.7)
        if num != 0:
            # Bot decision
            if len(self.player[num].handcards) <= self.player[num].\
                max_handcards:
                print("Current number of handcards: "
                    f"{len(self.player[num].handcards)}\n"
                    "maximum number of handcards: "
                    f"{self.player[num].max_handcards}")
                print("Discard phase skipped...")
            else:
                while(len(self.player[num].handcards) > self.player[num].\
                      max_handcards):
                    discard_card_index = self.player[num].discard_card()
                    discarded_card = self.player[num].handcards\
                    [discard_card_index]
                    for i in range(1, len(self.player)):
                        if i == num or not self.player[i].alive:
                            continue
                        self.player[i].enemy[num]["estimated_handcards"]\
                            [discarded_card.name] -= 1 
                        # update bot's prediction
                        self.player[i].enemy[num]["handcard_num"] -= 1
                        if self.player[i].enemy[num]["estimated_handcards"]\
                            [discarded_card.name] < 0:
                            print("**ERROR: function-discard_phase-"
                                  "discard_card<0**")
                    self.player[num].handcards.pop(discard_card_index)
                    print(f"Player {num+1} discarded [{discarded_card.name}]")
                    time.sleep(0.7)
            return
        # human player
        if len(self.player[num].handcards) > self.player[num].max_handcards:
            while(len(self.player[num].handcards) > self.player[num].\
                  max_handcards):
                print("Current number of handcards: " 
                      f"{len(self.player[num].handcards)}\n"
                      "maximum number of handcards: "
                      f"{self.player[num].max_handcards}")
                self.print_handcards(num)
                valid_choices = [str(i) for i in range(1, \
                    len(self.player[num].handcards) + 1)]
                choice = int(choose("Discard card: ", valid_choices, "yes")) \
                    - 1 # 1-# , so -1
                discarded_card = self.player[num].handcards[choice]
                for i in range(1, len(self.player)):
                    if i == num or not self.player[i].alive:
                        continue
                    self.player[i].enemy[num]["estimated_handcards"]\
                        [discarded_card.name] -= 1 # update bot's prediction
                    self.player[i].enemy[num]["handcard_num"] -= 1
                    if self.player[i].enemy[num]["estimated_handcards"]\
                        [discarded_card.name] < 0:
                        print("**ERROR: function-discard_phase-"
                              "discard_card<0**")
                self.player[num].handcards.pop(choice)
        else:
            print("Current number of handcards: "
                  f"{len(self.player[num].handcards)}\n"
                  "maximum number of handcards: "
                  f"{self.player[num].max_handcards}")
            print("Discard phase skipped...")

    def print_rules(self, anim):
        """
        This method prints rules with r with out animation 
        according to the value fo anim,
        which is a boolean preimeter
        With animation, the rules are printed word by word
        """
        os.system("cls")
        format.newline()
        try:
            with open("games/EndPhase/rules1.txt", 'r') as rules:
                text = rules.read()
        except:
            print("Failed to open rules1.txt")
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
                    # flush prints the output instantaniously
                    space1 = newline+1
                else:
                    print(text[space1:space2+1], end='', flush = True)
                    space1 = space2+1
                time.sleep(0.05)
        format.newline()
        input("Press any key to continue...") 

    def print_card_description(self, anim):
        """This method prints out the card descriptions of all 
        types of cards.
        anim is a bool value that indicates if the description 
        needs to be printed with animation or not"""
        format.newline()
        try:
            with open("games/EndPhase/rules2.txt", 'r') as rules:
                text = rules.read()
        except:
            print("Failed to open rules2.txt")
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


format = Format()
# game = Game1(3, 4) # when commmenting this, don't forget to change 
# the import in bot.py in for find_high_value_target method
# game.run()# also comment the output of bot handcards in main.py
# this block of code opens card.json from games.EndPhase.card.json, 
# it stores the card nums and card types.
try:
    with open("games/EndPhase/card.json", 'r') as file:
        content = json.load(file)
        card = content["card"]
        card_nums = content["card nums"]
except FileNotFoundError:
    print("Failed to locate card.json")
except:
    print("Failed to load card.json")