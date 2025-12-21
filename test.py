import os
import time
import random
body_part = "eye"
for i in range(15):
    os.system("cls")
    time.sleep(0.01)
    print('A', end='', flush = True)
    color_code="\033[91m"
    print(f"{color_code}{'a'*i}!", end='', flush = True)
    time.sleep(0.05)

os.system("cls")
print("Aaaaaaaaaaaaaaaa!")
time.sleep(1.2)
os.system("cls")
time.sleep(1.8)
output = ["It hurts...", "", f"My {body_part}!", "", f"Where is my {body_part}!", "",  "Aaaaaaaaa!", "", ""]
for i in output:
    os.system("cls")
    print(i, end='', flush = True)
    time.sleep(1.1)

print("\033[0m......")