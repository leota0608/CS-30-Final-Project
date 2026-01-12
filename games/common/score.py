import time as tm
from games.common.BodyPartsAnim import BodyPartsAnim


def handleMidGameClose(user, money):
    print("So you want to end the game in the middle.")
    print()
    print()
    print(f"you must either pay {money} or lose a body part.")

    while True:
        choice = input("what do you wanna do>(lose or pay or exit) ").lower()
        if choice == "lose":
            anims = BodyPartsAnim()
            chosen_part = user.choose_body_part()
            anims.choose_body_part_anim(chosen_part)
            print(f"oh no, it is a {chosen_part}")
            print("we will chop it off in (3) seconds.")
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

def updateScore(result, user, money, wasTie = False):

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
        print(f"You successfully passed {user.name}")
        input("Press any key to proceed to next game...")
    user.store_game_result(3, result)