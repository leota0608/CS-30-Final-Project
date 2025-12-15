# CS-30-Final-Project
**Contributors: `Leo`, `Amir`**  
  
**Table of Contents:**
- [Program Purpose](#program-purpose)
- [Story Line](#story-line)
- [Program Theme](#program-theme)
- [Example Catch Phrases](#example-catch-phrases)
- [Target Users](#target-users)
- [Must Have List](#must-have-list)
- [Wish List](#wish-list)




## Program Purpose
This program is designed to demostrate the programming concepts of CS 30, including `data structures`, `external files`, `libraries`, and `object-oriented programming`.
<br><br>

## Story Line
Main Character participates in a trial with no money. He must pass all `4` different games to win the final prize.
But before that, danger awaits him. Every game he loses will comes with a price, and it will be a random choice of any of his body parts.(If his head was accidently chosen, then good luck! Let's see if he can still play with no head. ^_^) 
<br><br>

## Program Theme
The program will consist of two general scenes, the map which the player will be in to choose the `4` games, and the differnet scenes in every mini-game. 
<br><br>

## Example Catch Phrases
```python
# opening external files
try:
    with open("ExampleFile1", 'r') as file1:
        pass
except FileNotFoundError:
    print("ExampleFile1 not found!")
except:
    print("Unknown error occurs!")
else:
    print("ExampleFile1 successfully opened!")
finally:
    print("There's an attempt to open ExampleFile1...")
```
<br><br>

## Target Users
People who love excitement...

<br><br>

## Must Have List 
1. At least four fully functioning games
2. A menu: Wall of Fame, a way for the player to check their missing body parts
3. A list of human body parts to randomly choose when the player lose a game
4. The lost body parts affects how the player play the game
5. Use `.json` or `.txt` file to store the players' information

## Wish List
1. Print the cards the player has using charactor art(better UI), possibly use file to store the shape of the cards and load them
2. Add more games
3. Add a store to sell robot to help the player if them lose an important body part
4. Add a timer for how long the player can think in their turn
5. Add a ranking(wall of fame) for all players who had play the games
