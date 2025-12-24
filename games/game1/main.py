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
        while not len(self.player) == 1:
            for i in range(len(self.player)):
                format.newline()
                # check alive
                if self.player[i].health <= 0:
                    print(f"Player {self.player[i].name} died...")#enemy_num-1
                    self.player.pop(i)
                    if len(self.player) == 1:
                        print(f"Player {self.player[0].name} win!")
                        return
                # draw cards
                print("Drawing cards...")
                time.sleep(0.7)
                self.draw_cards(i)

                # take turns
                print("The round begins...")
                time.sleep(0.7)
                
                self.start_phase(i)

                # discard phase
                self.discard_phase(i)

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
        newly_drawn_cards = self.deck.draw(2)
        if num == 0:
            print(f"[{newly_drawn_cards[0].name}, {newly_drawn_cards[1].name}] newly added to your hand cards")
            time.sleep(0.7)
        self.player[num].handcards.extend(newly_drawn_cards)

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
                    print("**ERROR: function-nearly_dead-peach<0**")

                return
        print(f"player {num+1} died...")# enemy_num-1

        del self.player[num]

    def attack(self, num):
        # attack num
        print(f"num: {num}")
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
                if i == num:
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
            print(f"{who} don't have any slashes and loses one health point")
            self.player[num1].health -= 1

            for i in range(1, len(self.player)):
                if i == num1:
                    continue
                self.player[i].enemy[num1]["health"] -= 1 # update bot's prediction]

            self.player[num1].max_handcards -= 1
            if self.player[num1].health == 0:
                self.nearly_dead(num1)
        choice = choose("Do you choose to play a [slash]?(yes/no)", ["yes", "no"])
        if choice == "yes":
            print(f"{who} player a slash")
            self.player[num1].handcards.pop(find_slash)
            
            for i in range(1, len(self.player)):
                if i == num1:
                    continue
                self.player[i].enemy[num1]["estimated_handcards"]["slash"] -= 1 # update bot's prediction
                if self.player[i].enemy[num1]["estimated_handcards"]["slash"] < 0:
                    print("**ERROR: function-duel-slash<0**")

        else:
            self.player[num1].health -= 1

            for i in range(1, len(self.player)):
                if i == num1:
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
            while act_step == 1:
                self.print_handcards(num)
                print(f"Available moves:\n{len(self.player[num].handcards) + 1}. end turn")
                valid_choices = [str(i) for i in range(1, len(self.player[num].handcards) + 2)]
                choice = int(choose("Choice: ", valid_choices))
                if choice == len(self.player[num].handcards) + 1:
                    break# shoud have auto end turn
                choice -= 1 # 0 indexing
                chosen_card = self.player[num].handcards[choice]
                if chosen_card.type == "basic":
                    if chosen_card.name == "slash":
                        if act_step == 0:
                            print("You can only play one [slash] in one turn")
                            continue
                        output = "Who do you want to attack?"
                        for i in range(1, len(self.player)):
                            output += f"\n- player {i+1}"
                        output += "\n"
                        valid_choices = [str(i) for i in range(2, len(self.player[num].handcards) + 1)]
                        choice_p = int(choose(output, valid_choices)) - 1 # 0 indexing
                        print(f"You attacked player {choice_p+1}")
                        self.player[num].handcards.pop(choice)

                        for i in range(1, len(self.player)):
                            if i == num:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["slash"] -= 1 # update bot's prediction
                            if self.player[i].enemy[num]["estimated_handcards"]["slash"] < 0:
                                print("**ERROR: 1function-start_phase-slash<0**")

                        time.sleep(0.7)
                        self.attack(choice_p)
                        act_step -= 1
                    if chosen_card.name == "peach":
                        if self.player[num].health == self.player[num].initial_health: # temporary be 4
                            print("**You are already at maximum health**")
                        else:
                            self.player[num].health += 1
                            self.player[num].handcards.pop(choice)

                            for i in range(1, len(self.player)):
                                if i == num:
                                    continue
                                self.player[i].enemy[num]["estimated_handcards"]["peach"] -= 1 # update bot's prediction
                                if self.player[i].enemy[num]["estimated_handcards"]["peach"] < 0:
                                    print("**ERROR: 2function-start_phase-peach<0**")

                    if chosen_card.name == "dodge":
                        print("**You can only use [dodge] when another player attacks you**")

                if chosen_card.type == "equipment":
                    if chosen_card.name == "crossbow" or chosen_card.name == "crossblade":
                        if self.player[num].equipment["weapen"] is None:
                            self.player[num].equipment["weapen"] = chosen_card.name
                            print(f"You successfully equiped {chosen_card.name}")
                            self.player[num].handcards.pop(choice)

                            for i in range(1, len(self.player)):
                                if i == num:
                                    continue
                                self.player[i].enemy[num]["estimated_handcards"][chosen_card.name] -= 1 # update bot's prediction
                                if self.player[i].enemy[num]["estimated_handcards"][chosen_card.name] < 0:
                                    print("**ERROR: 3function-start_phase-equipment<0**")
                    else:
                        pass # no armor has been made yet
                        
                if chosen_card.type == "trick":
                    card_name = chosen_card.name
                    if card_name == "duel":
                        output = "Who do you want to duel with?"
                        for i in range(1, len(self.player)):
                            output += f"\n- player {i+1}"
                        output += "\n"
                        valid_choices = [str(i) for i in range(2, len(self.player[num].handcards) + 1)]
                        choice = int(choose(output, valid_choices)) - 1
                        print(f"You dueled with player {num+1}")# do AI need to play all slash to win the duel?(strategy)
                        self.player[num].handcards.pop(choice)

                        for i in range(1, len(self.player)):
                            if i == num:
                                continue
                            self.player[i].enemy[num]["estimated_handcards"]["duel"] -= 1 # update bot's prediction
                            if self.player[i].enemy[num]["estimated_handcards"]["duel"] < 0:
                                print("**ERROR: 4function-start_phase-duel<0**")
                        self.duel(num, choice, 1)
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
                print(f"Current number of hand cards: {len(self.player[num].handcards)}\nmaximum number of handcards: {self.player[num].max_handcards}")
                self.print_handcards(num)
                valid_choices = [str(i) for i in range(1, len(self.player[num].handcards) + 1)]
                choice = int(choose("Discard card: ", valid_choices, "yes")) - 1 # 1-# , so -1
                discarded_card = self.player[num].handcards[choice]
                self.player[num].handcards.pop(choice)

                for i in range(1, len(self.player)):
                    if i == num:
                        continue
                    self.player[i].enemy[num]["estimated_handcards"][discarded_card] -= 1 # update bot's prediction
                    if self.player[i].enemy[num]["estimated_handcards"][discarded_card] < 0:
                        print("**ERROR: function-discard_phase-discard_card<0**")
        else:
            print(f"Current number of hand cards: {len(self.player[num].handcards)}\nmaximum number of handcards: {self.player[num].max_handcards}")
            print("Discard phase skipped...")

format = Format()

game = Game1(3, 4)
game.run()


# action_step crossbow didn't check