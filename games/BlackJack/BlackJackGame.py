from games.common.BodyPartsAnim import BodyPartsAnim
from games.BlackJack.human import Human
from games.common.GameHandler import GameHandler
from games.BlackJack.bot import Bot
from games.BlackJack.deck import Deck
from games.common.GameHandler import GameHandler
from games.common.format import Format
from games.common.GameCard import printCardList
import time


class BlackJackGame(GameHandler):
    def __init__(self, player):
        self.player = player
        self.running = True
        self.result = False
        # initialise deck of cards
        self.deck = Deck()
        self.deck.initialise()
        self.deck.shuffle()
        # initialise player
        self.player_num = 3                     # 3 players, this can be changed
        self.initialise_player(self.player_num)

        GameHandler.__init__(self, self.player_list, None, "Black Jack")

    def initialise_player(self, num):
        self.player_list = []
        self.player_list.append(Human())
        for i in range(1, num):
            self.player_list.append(Bot())

    def print_rules(self, anim):
        Format().newline()
        with open("games/BlackJack/rules.txt", 'r') as rules:
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
        Format().newline()
        input("Press any key to continue...")


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
        if self.player.name.lower() == "test":
            self.print_rules(False)
        else:
            self.print_rules(True)
        print("**Enter 0 to review game rules at any time**")
        print("Drawing phase:")
        # initial draw
        for i in range(self.player_num):
            if i == 0:
                print("Your turn to draw...")
                time.sleep(0.7)
                print("Drawing card...")
                time.sleep(1.2)
                self.player_list[i].add_card(self.deck.draw())
                self.print_handcard(0)
                self.player_list[0].find_sum()
            else:
                print(f"Player {i+1}'s turn")
                time.sleep(0.7)
                print(f"Player {i+1} drawing...")
                time.sleep(1.2)
                self.player_list[i].add_card(self.deck.draw())
                self.print_handcard(i)
                self.player_list[i].find_sum()
        if_draw = 0
        while self.running:
            if_draw += 1
            if if_draw == 3:
                if_draw = 0
                choice = input("Do you want to call the judge over for no one choosing to draw cards ? (y/n)")
                while choice == '0':
                    self.print_rules(False)
                    for i in range(20):
                        print("\033[A\033[2K", end='')
                    choice = input("Do you choose to draw? (y/n)")
                if choice.lower() == "y" or choice.lower() == "yes":
                    max_score = -1
                    max_index = 0
                    for i in range(0, len(self.player_list)):
                        if not self.player_list[i].alive:
                            continue

                        if self.player_list[i].max_sum > max_score:
                            max_score = self.player_list[i].max_sum
                            max_index = i
                    if max_index == 0:# win
                        print("The judge came, and decided you are the winner")
                        for i in range(3, 1, -1):
                            print(f"\rReturning to lobby in {i}s")
                            time.sleep(2)
                        self.running = False
                        self.result = True
                        break
                    else:# lost
                        print("The judge believes you are the problem and declared you as lost...")
                        for i in range(3, 1, -1):
                            print(f"\rReturning to lobby in {i}s")
                            time.sleep(1)
                        self.running = False
                        self.result = False
                        self.alive = False
                        break

            player_alive = 0
            for i in self.player_list:
                if i.alive:
                    player_alive += 1
            if player_alive == 1:# win
                print("You win")
                for i in range(3, 1, -1):
                    print(f"\rReturning to lobby in {i}s")
                    time.sleep(1)
                self.running = False
                self.result = True
                break
            human_draw = False
            for i in range(self.player_num):
                if i == 0:
                    Format().newline()
                    print("Your turn to draw...")
                    time.sleep(0.5)
                    self.print_handcard(-1)
                    Format().newline()
                    choice = input("Do you choose to draw? (y/n)")
                    #####################################################    
                    if choice.lower() == "admin":
                        choice = input("Admin code: ")
                        if choice == "0710":
                            choice = input("Win or lose(1/0):")
                            if choice == '1':
                                print("You win...(Admin mode)")
                                time.sleep(2)
                                self.running = False
                                self.result = True
                                break
                            if choice == '0':
                                print("You lost...(Admin mode)")
                                time.sleep(2)
                                self.running = False
                                self.result = False
                                self.alive = False
                                break
                    #####################################################        
                    while choice == '0':
                        self.print_rules(False)
                        for i in range(20):
                            print("\033[A\033[2K", end='')
                        choice = input("Do you choose to draw? (y/n)")
                    
                    if choice.lower() == "y" or choice.lower() == "yes":
                        if_draw = 0
                        human_draw =True
                        print("Drawing card...")
                        time.sleep(1.2)
                        self.player_list[0].add_card(self.deck.draw())
                        self.print_handcard(0)
                        r = self.check_sum(i)
                        self.player_list[0].find_sum()
                        if  r == 0:# lost
                            print("You lost...")
                            for i in range(3, 1, -1):
                                print(f"\rReturning to lobby in {i}s")
                                time.sleep(1)
                            self.running = False
                            self.result = False
                            self.alive = False
                            break
                        if r == 1:# win
                            print("You win by getting 21...")
                            for i in range(3, 1, -1):
                                print(f"\rReturning to lobby in {i}s")
                                time.sleep(1)
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
                        self.player_list[i].add_card(self.deck.draw())
                        self.print_handcard(i)
                        r = self.check_sum(i)
                        
                        self.player_list[i].find_sum()
                        if  r == 1:# human lost
                            print(f"You lost... Player {i+1} got 21")
                            for i in range(3, 1, -1):
                                print(f"\rReturning to lobby in {i}s")
                                time.sleep(1)
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

                if not self.running:
                    break
        # end of game
        self.handle_game_result()

    def handle_game_result(self):
        if self.result:
            print(f"You successfully passed {self.name}")
            input("Press any key to proceed to next game...")
        else:
            print("You failed to pass game 2")
            time.sleep(0.7)
            print("Receive your punishment!")
            body_part = self.player.choose_body_part()
            self.player.lose(body_part)
            anim = BodyPartsAnim(self.player)
            anim.choose_body_part_anim(body_part)
            time.sleep(2)
            anim.screen_flickering_anim(body_part)
            print(f"You lost your {body_part}...")
            print("You are forced into the next game...")

    def print_handcard(self, num):
        if num == -1:
            for i in range(len(self.player_list)):
                if not self.player_list[i].alive:
                    continue
                if i == 0:
                    print("Your", end=' ')
                else:
                    print(f"Player {i+1}'s", end=' ')
                print(f"handcard:", end='')
                printCardList(self.player_list[i].handcard_display, 5)
                # for j in self.player_list[i].handcard:
                #     if j == 1:
                #         print('A', end=' ')
                #     elif j == 11:
                #         print('J', end=' ')
                #     elif j == 12:
                #         print('Q', end=' ')
                #     elif j == 13:
                #         print('K', end=' ')
                #     else:
                #         print(j, end= ' ')
                # print(']')
        else:
            if num == 0:
                print("Your", end=' ')
            else:
                print(f"Player {num+1}'s", end=' ')
            print(f"handcard: ", end='')
            
            printCardList(self.player_list[num].handcard_display, 5)
            # for j in self.player_list[num].handcard:
            #     if j == 1:
            #         print('A', end=' ')
            #     elif j == 11:
            #         print('J', end=' ')
            #     elif j == 12:
            #         print('Q', end=' ')
            #     elif j == 13:
            #         print('K', end=' ')
            #     else:
            #         print(j, end= ' ')
            # print(']')




