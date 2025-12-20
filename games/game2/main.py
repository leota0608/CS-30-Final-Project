import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from games.game2.human import Human
from games.game2.bot import Bot
from games.game2.deck import Deck
from games.common.GameHandler import GameHandler
import time
class Game2:
    def __init__(self):
        self.running = True
        self.result = False
        # initialise deck of cards
        self.deck = Deck()
        self.deck.initialise()
        self.deck.shuffle()
        # initialise player
        self.player_num = 3 # 3 players
        self.initialise_player(self.player_num)

    def initialise_player(self, num):
        self.player_list = []
        self.player_list.append(Human())
        for i in range(1, num):
            self.player_list.append(Bot())

    def print_rules(self):
        print("Game rules:...")

    def check_sum(self, index):
        sum = 0
        count_a = 0
        for i in self.player_list[index].handcard:
            if i == 1:
                count_a += 1
            elif i > 10:
                sum += 10
            else:
                sum += i
        if sum + count_a > 21:
            return 0 # 0: lost
        if sum + count_a == 21:
            return 1
        while count_a > 0:
            sum += 11
            count_a -= 1
            if count_a >= 0 and sum + count_a == 21:
                return 1 # 1: win
            if count_a >= 0 and sum + count_a > 21:
                return -1 # -1: continue game
        return -1


    def run(self):
        print("game2 starts")
        self.print_rules()
        print("Drawing phase:")
        # initial draw
        for i in range(self.player_num):
            if i == 0:
                print("Your turn to draw...")
                input("press any key to continue...")
                print("Drawing card...")
                time.sleep(0.7)
                self.player_list[i].add_card(self.deck.draw())
                print("Your handcard: [", end=' ')
                j = self.player_list[0].handcard[0]
                
                self.player_list[0].find_sum()
                if j == 1:
                    print('A', end = ' ')
                elif j == 11:
                    print('J', end = ' ')
                elif j == 12:
                    print('Q', end = ' ')
                elif j == 13:
                    print('K', end = ' ')
                else:
                    print(j, end = ' ')
                print(']')
            else:
                print(f"Player {i+1}'s turn")
                time.sleep(0.7)
                print(f"Player {i+1} drawing...")
                time.sleep(1.2)
                print(f"Player {i+1}'s handcard: [", end = ' ')
                self.player_list[i].add_card(self.deck.draw())
                self.player_list[i].find_sum()
                j = self.player_list[i].handcard[0]
                if j == 1:
                    print('A', end = ' ')
                elif j == 11:
                    print('J', end = ' ')
                elif j == 12:
                    print('Q', end = ' ')
                elif j == 13:
                    print('K', end = ' ')
                else:
                    print(j, end = ' ')
                print(']')
        if_draw = 0
        while self.running:
            if_draw += 1
            if if_draw == 3:
                if_draw = 0
                choice = input("Do you want to call the judge over for no one choosing to draw cards ? (y/n)")
                if choice.lower() == "y" or choice.lower() == "yes":
                    max_score = -1
                    max_index = 0
                    for i in range(0, len(self.player_list)):
                        if self.player_list[i].max_sum > max_score:
                            max_score = self.player_list[i].max_sum
                            max_index = i
                    if max_index == 0:# win
                        print("The judge came, and decided you are the winner\nReturning to lobby in 3s")
                        time.sleep(2)
                        self.running = False
                        self.result = True
                        break
                    else:# lost
                        print("The judge believes you are the problem and declared you as lost...\nReturning to lobby in 3s")
                        time.sleep(2)
                        self.running = False
                        self.result = False
                        self.alive = False
                        break

            player_alive = 0
            for i in self.player_list:
                if i.alive:
                    player_alive += 1
            if player_alive == 1:# win
                print("You win\nReturning to lobby in 3s...")
                time.sleep(2)
                self.running = False
                self.result = True
                break
            human_draw = False
            for i in range(self.player_num):
                if i == 0:
                    print("Your turn to draw...")
                    time.sleep(0.5)
                    choice = input("Do you choose to draw? (y/n)")
                    if choice.lower() == "y" or choice.lower() == "yes":
                        if_draw = 0
                        human_draw =True
                        print("Drawing card...")
                        time.sleep(1.2)
                        self.player_list[0].handcard.append(self.deck.draw())
                        print("Your current handcard: [", end=' ')
                        for j in self.player_list[0].handcard:
                            if j == 1:
                                print('A', end=' ')
                            elif j == 11:
                                print('J', end=' ')
                            elif j == 12:
                                print('Q', end=' ')
                            elif j == 13:
                                print('K', end=' ')
                            else:
                                print(j, end= ' ')
                        print(']')
                        r = self.check_sum(i)
                        self.player_list[0].find_sum()
                        if  r == 0:# lost
                            print("You lost... \nReturning to lobby in 3s...")
                            time.sleep(2)
                            self.running = False
                            self.result = False
                            self.alive = False
                            break
                        if r == 1:# win
                            print("You win by getting 21...  \nReturning to lobby in 3s...")
                            time.sleep(2)
                            self.running = False
                            self.result = True
                            break
                    else:
                        if choice.lower() == 'n' or choice.lower() == 'no':
                            pass
                        else:
                            print("Your respond is seen as a No...\nRemember to answer correctly next time...")
                        compare = True
                        for i in range(1, len(self.player_list)):
                            if self.player_list[i].alive and self.player_list[i].max_sum <= self.player_list[0].max_sum:
                                compare = False
                                break
                        if compare:
                            print("You lost...\n Everyone else choose not to draw and has a high score than you\nRemember their is no backing down\nReturning to lobby in 3s...")
                            time.sleep(2)
                            self.running = False
                            self.result = False
                            self.alive = False
                            
                elif self.player_list[i].alive:
                    print(f"Player {i+1}'s turn")
                    choice = self.player_list[i].evaluate_draw(human_draw, self.player_list, self.deck, i)
                    if choice:
                        if_draw = 0
                        time.sleep(0.7)
                        print(f"Player {i+1} drawing...")
                        time.sleep(1.2)
                        self.player_list[i].handcard.append(self.deck.draw())
                        print(f"Player {i+1}'s handcard: [", end=' ')
                        for j in self.player_list[i].handcard:
                            if j == 1:
                                print('A', end=' ')
                            elif j == 11:
                                print('J', end=' ')
                            elif j == 12:
                                print('Q', end=' ')
                            elif j == 13:
                                print('K', end=' ')
                            else:
                                print(j, end= ' ')
                        print(']')
                        r = self.check_sum(i)
                        
                        self.player_list[i].find_sum()
                        if  r == 1:# human lost
                            print(f"You lost... Player {i+1} got 21\nReturning to lobby in 3s...")
                            time.sleep(3)
                            self.running = False
                            self.result = False
                            break
                        if r == 0:# robot lost
                            print(f"Player {i+1} lost...\nRemaining player: ", end='')
                            self.player_list[i].alive = False
                            for i in range(self.player_num):
                                if self.player_list[i].alive:
                                    print(f"Player {i+1} ", end='')
                            print('')
                    else:
                        print(f"Player {i+1} choose not to draw")

                        

                        


#g = Game2()


