import json
import random


def select_name(user_name, num):
    """This function has perimeter of:
    user_name: the human player's name.
    num: number of names needed.
    The function picks names randomly and avoid picking the same name
    as the user name. Then, it returns the list of names picked."""
    with open("games/common/robotNames.json", "r") as f:
        names = json.load(f)["robot_names"] 
        
    if user_name in names:
        names.remove(user_name)
    selected_names = []
    for i in range(num):
        name = random.choice(names)
        selected_names.append(name)
        names.remove(name)
    return selected_names

    
