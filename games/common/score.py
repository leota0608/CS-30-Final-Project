###############################################################################
# Coder: Amir
# Last date modified: 1/15/2026
###############################################################################
""" Defines the functionality needed for scoring the player. Currently,
we have only two functions that one allows for mid-game close down and
scoring and the other scores the player at the very end.
"""
###############################################################################
import time as tm
from games.common.BodyPartsAnim import BodyPartsAnim


def handleMidGameClose(user, money):
    """ If the player choose to end a game, they either have
    to pay or lose a body part. Call this function once local
    game handling is over to score the player.
    user: the player.(Player)
    money: amount of money to buy freedom.(int)
    """
    print("So you want to end the game in the middle.")
    print()
    print()
    print(f"you must either pay {money} or lose a body part.")

    while True:
        choice = input("what do you wanna do>(lose or pay or exit) ").lower()
        if choice == "lose":
            # choose a body part and show its animation.
            anims = BodyPartsAnim(user)
            chosen_part = user.choose_body_part()
            anims.choose_body_part_anim(chosen_part)
            print(f"oh no, it is a {chosen_part}")
            print("we will chop it off in (3) seconds.")
            # show chop of animation.
            tm.sleep(3)
            anims.screen_flickering_anim(chosen_part)
            print("we move on ...")
            return True
        elif choice == "pay":
            if user.money >= money:
                user.addMoney(-money)
            print("you bought your freedom.")
            print("we move on ...")
            return True
        elif choice == "exit":
            return None
        else:
            print("invalid option")


def updateScore(result, user, money, wasTie=False):
    """ Once the game is over we will score the player.
    If the player has won we give them money otherwise
    a body part is lost.
    result: True or False indicating weather player won.(bool)
    user: actual player object. (Player)
    money: money to give to player if they won.(int)
    wasTie: optional and by default false.
            Set True of a tie occurred.(bool)
    """
    anims = BodyPartsAnim(user)
    if not result:
        print("oh no oh no .... noo nooo")
        print(f"you lost player {user.name}!")
        tm.sleep(2)
        print("you miserable idiot, you loser, you ... ")
        print("get your punishment ... ha ha ha ha ha ...")
        tm.sleep(2)
        if wasTie:
            print("yeah")
            print("even when it was tie. ha ha ha")
        tm.sleep(2)
        # preparing body part choosing animation
        chosen_part = user.choose_body_part()
        anims.choose_body_part_anim(chosen_part)
        print(f"oh no, it is a {chosen_part}")
        print("we will chop it off in (3) seconds.")
        tm.sleep(3)
        anims.screen_flickering_anim(chosen_part)
        print("we move on ...")
        user.lose(chosen_part)
    else:
        user.addMoney(money)
        print(f"You successfully passed, {user.name}!")
        input("Press any key to proceed to next game...")
    user.store_game_result(3, result)
