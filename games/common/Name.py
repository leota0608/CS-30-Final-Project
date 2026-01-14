#######################################################################
# Coder: Leo
# Last date modified: 1/14/2026
#######################################################################
''' This module defines all the functions that are needed to handle
player names. Currently it only has one function that chooses name
for bots while avoiding choosing the human player.
'''
#######################################################################

import json
import random


def select_name(user_name, num):
    """The function picks names randomly and avoid 
    picking the same name as the user name. Then, it 
    returns the list of names picked.
    user_name: the human player's name. (str)
    num: number of names needed. (int)
    """
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
