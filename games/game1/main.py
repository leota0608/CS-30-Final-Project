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
        self.player.append(Human(f"player1", initial_health))
        for i in range(1, player_num):
            self.player.append(Bot(f"player{i+1}", initial_health, player_num - 1))
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
                if not self.running:
                    self.result = True
                    print("You fought to the end, there are no cards left.\nThe judeg came and decided you are the winner...")
                    break

                # take turns
                print("The round begins...")
                time.sleep(0.7)
                
                self.start_phase(i)

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
        print("Your handcards:")
        for i in range(len(self.player[num].handcards)):
            print(f"{i+1}. {self.player[num].handcards[i].name}")
    def nearly_dead(self, num):
        for i in range(len(self.player[num].handcards)):
            if self.player[num].handcards[i].name == "peach":
                
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
            print("You died...\n Returning to lobby in 3s")
            time.sleep(2)
            return
        print(f"player {num+1} died...")# enemy_num-1
        for i in range(1, len(self.player)):
            if i == num:
                continue
            self.player[i].enemy[num]["alive"] = False # update bot's prediction
        self.player[num].alive = False

    def attack(self, num):
        # attack num
        #print(f"num: {num}")# debug
        for i in range(len(self.player[num].handcards)):
            
            if self.player[num].handcards[i].name == "dodge":
                print(f"player {num+1} uses [dodge]")
                self.player[num].handcards.pop(i)

                for j in range(1, len(self.player)):
                    if j == num:
                        continue
                    self.player[j].enemy[num]["estimated_handcards"]["dodge"] -= 1 # update bot's prediction
                    if self.player[j].enemy[num]["estimated_handcards"]["dodge"] < 0:
                        print("**ERROR: function-attack-dodge<0**")

                break
        else:
            self.player[num].health -= 1

            for i in range(1, len(self.player)):
                if i == num or not self.player[i].enemy[num]["alive"]:
                    continue
                self.player[i].enemy[num]["health"] -= 1 # update bot's prediction]

            self.player[num].max_handcards -= 1
            print(f"player {num+1} loses one health point\ncurrent health: {self.player[num].health}")
            if self.player[num].health == 0:
                self.nearly_dead(num)
            

    def duel(self, num1, num2, human):# human = 1: num1 human, -1: num2 is human, 0: two AI dueling
        print("     **[DUEL]**")
        # num1
        if not human == 1:
            # AI evaluate
            print("AI should be evaluating this")
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
                        valid_choices = [str(t) for t in alive_targets]
                        choice_p = int(choose(output, valid_choices)) - 1 # 0 indexing
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
                        self.attack(choice_p)
                        act_step -= 1
                    if chosen_card.name == "peach":
                        if self.player[num].health == self.player[num].initial_health: # temporary be 4
                            print("**You are already at maximum health**")
                        else:
                            self.player[num].health += 1
                            self.player[num].max_handcards += 1
                            for i in range(1, len(self.player)):
                                if i == num or not self.player[i].enemy[num]["alive"]:
                                    continue
                                self.player[i].enemy[num]["estimated_handcards"]["peach"] -= 1 # update bot's prediction
                                self.player[i].enemy[num]["handcard_num"] -= 1
                                if self.player[i].enemy[num]["estimated_handcards"]["peach"] < 0:
                                    print("**ERROR: 2function-start_phase-peach<0**")
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
                                self.player[i].enemy[num]["equipment"]["weapen"] = chosen_card.name

                                if self.player[i].enemy[num]["estimated_handcards"][chosen_card.name] < 0:
                                    print("**ERROR: 3function-start_phase-equipment<0**")
                            self.player[num].handcards.pop(choice)
                        else:
                            equiped_card_name = self.player[num].equipment["weapen"].name
                            replace_choice = choose(f"You have already equiped {equiped_card_name}, do you want to replace it?({equiped_card_name} will be automatically discarded)")
                            if replace_choice.lower() in ['y', 'yes']:
                                self.player[num].equipment["weapen"] = chosen_card
                                print(f"You successfully equiped {chosen_card.name}")

                                for i in range(1, len(self.player)):
                                    if i == num or not self.player[i].enemy[num]["alive"]:
                                        continue
                                    self.player[i].enemy[num]["estimated_handcards"][chosen_card.name] -= 1 # update bot's prediction
                                    self.player[i].enemy[num]["handcard_num"] -= 1
                                    self.player[i].enemy[num]["equipment"]["weapen"] = chosen_card.name
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
        else:
            print(f"Player {num+1}'s turn:")
            act_step = 1
            while act_step == 1:
                # Bot move
                pass
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

game = Game1(3, 4)
game.run()


# action_step crossbow didn't check