import json
import random
def select_name(user_name, num):
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


    
