# CS-30-Final-Project
<br><br>
x.y.z  
x: represents the coder ID  
- Amir uses code 0  
- Leo uses code 1  
y: the version number  
z: commit number  
example:  
+ 0.1.1 means amir committed his first commit to version 1.  
## Change Log

+ 0.4.6 and 0.4.6.2:
 - comments were added.
 - delays were adjusted.
 - A bug in hearts human player, were choosing a wrong card
   resulted in removal of cards solved.
+ 0.4.5:
 - comments were added extensively.
+ 0.4.4:
  - added a file to check which classes and functions are missing
  docstring.
  - removed test files.
  - a file that contains missing docstring classes and methods was added.
+ 0.4.3.6:
  - All files now have header of length 79.
  - A code to this automatically was written.
+ 0.4.3.5:
  - commented game handler file.
+ 0.4.3.4:
- comments for teller and score were added.
+ 0.4.3.3:
- comments and documents were fully added to game of Court Piece
+ 0.4.3.2:
 - comments and documents were fully added to the game of Hearts
+ 0.4.3.1:
 - Added comments to modules in the common folder.
+ 0.4.2.4:
 - spelling mistakes in the main corrected.
+ 0.4.2.2 and 0.4.2.3:
- the bug that multiple body parts was printed solved.

+ 0.4.2.1:
- Games are now able to add and lose moeny to the player
+ 0.4.1.3:
- the games are given the ability to show the flickering message after chopping off
  body parts.
+ 0.4.1.2:
 - a method to print the player's condition was addded.
 - Note: There was bug were body parts were added twice to the self.lost_body_parts
+ 0.4.1.1:
 - the method for printing player was debugged.
 - comments was addded to imrpove its readability
 - The feedbacks from Mrs.Lyn were added to be addressed in the game.  
+ 0.3.10:
  - a method to print the player had been added.
+ 0.3.9:
  - the games are named by their real name.
  - all the packages are renamed accordingly.
+ 0.3.8:  
  - the ability to print cards had been added.  
+ 0.3.7:  
  - changed the game 3 and game 4 to only take user as parameter.  
+ 0.3.6:  
  - Problem with vscode that it cannot find the modules is solved.
  - the Teller class printing everything in statements is solved by
  flushing the stdout buffer earlier before escape characters.  
+ 0.3.5:  
  - Rules of the game of Hearts had been written.  
+ 0.3.4:  
  - The human logic for the game of hearts was developed.  
  - The game was debugged.
+ 0.3.3:  
  - playing logic for robot of the game of hearts was developed.   
+ 0.3.2:  
  - The game of Hearts is now able to distribute cards among players
  - It is also able to exchange cards with adjacent players.  
+ 0.3.1:  
  - The files for game of Hearts was created
  - The file CPCard was renamed GameCard and moved to the common
  folder.  
+ 0.2.5:  
  - The teller class is enabled to interrupt itself, by asking 
  the user a question, if they would like to continue.  
  - Court Piece rules were written into a file and are being
  displayed to user.  
+ 0.2.4:  
  - The CourtPiece game had been debugged.  
  - Teller class had been added to print long explanations
  in a interactive manner.  
+ 0.2.3:  
  - The game handler class had been created.
    + CourtPiece class puts all the players together
    and enforces the rules of the game.  
+ 0.2.2:  
  - Created a class named CPHumanPlayer that represents 
  the human-player of the CourtPiece.
    + The class has the ability to directly ask the user.
    + User responses are check to make sure are all correct.
  - Created a class named CPBot that ensures that represents all
  bots that play courtPiece.
    + logic has been built into it.
  - CPCard class has been created to modularity represent the card
  games in Court Piece.
    + Use operator overloading to make comparisons and use in logic
    statements easier.  

0.2.1:  
- Based on experiments after making games, the framework
was fixed and improved  

0.1.1:  
- a framework was developed for the games to ensure all games
would follow the same order.
- An example with Rock Paper Scissor Shoot was written to
demonstrate the use of this framework.  

> 12.20 1.1.# 
- finish *player* folder
    + bodyParts.json
    + player.py
    + playingRecord.json
- finish `main.py` in main folder
    + can now import all other four mini-games
    + creat four objects inside `Game` class
    + can run the four games inside folder
    + import `player.py` from *player* folder
    + creat a player object to read player information, store player information and store playing record

> 12.21  
- finish game 2
  + add the rules of the game and stored it as a `.txt` file (`rules..txt` in *game 2* folder)
  + add some animation(print rules word by word, add screen flickering when the player lost and loses a body part)
  + debug game 2 
  + `main.py` can now read results from `main.py` in *game 2* folder and update score, game results and lost body parts in `playingRecord.json` in *player* folder
    
> 12.24   
+ 1.2.3
  - debug game1
  - Need to be added:
      + More card operations
      + AI moves
      + Fix bugs......
+ 1.2.4
  - Add [dismantle] trick card to game1/main.py. Fix naming in game1/card.json

> 12.25 1.2.5
- add trick card: [snatch],
- refine handcard output format(print out opponent information)

> 12.26 1.2.6
- Add trick card: archery, savage, benevolence, negate. 
- Add some card description in game1/card.json.
- Debug...

> 12.27 1.2.7
- Initially complete game1
- Made some simple AI strategies, the game can now run a full cycle without crashing and can be called by main main.py. 
- There are still tons of bugs needed to be fixed and more AI strategies need to be implemented. 
- duel doesn't work
- Debug...

> 12.30 1.2.8
- Improve bot's decision making
- Debug...

> 12.31 1.2.9
- Add playing strategy of savage, archery, dismantle and snatch of bot.
- Debug...

> 1.4 1.2.10
- create rule.txt(not finished)
- finish bot playing strategy
- add new armor [evasion]
- fix bug in duel method in main.py
- added [crossblade] effect
- debug

> 1.5 1.3.3
- update [negate] effect to all trick cards
- fix bugs: ex. checking None when bot equipping armor and weapen

> 1.6 1.3.3.1 - 1.3.3.4
- add gitignore
- create random name selector for robots to use in common

> 1.7  
+ 1.3.4
-fix admin mode bug
  - the code can now run for game 1 and 2 without crashing(if there are no bugs within game1 and game2)
+ 1.3.5
  - add print handcards to game2
+ 1.3.5
  - Fix bug in game2 of outputting cards number
+ 1.3.7
  -Fixed small bugs in game1 and game2
  -Add rules printing to game 1
  -Improve the two games on UI

> 1.8 1.4.1
- create shop.py and update shop
> 1.10 1.4.1.2
- finish shop
> 1.11 1.4.3
- General improvement on format, fixed some bugs
> 1.12 1.4.4
- add some descriptions for code
> 1.13 
- 1.4.5
  - add all kinds of coments for End Phase Game
- 1.4.6
  - update alphatest.md

>1.15 - 1.18 
- 1.4.7 - 1.4.15
  + Fix PEP8 and general optimization


---
To do list: 1/5/2026
1. move bodypart animation to common (done 1.3.2)
2. lose body parts in every game, not in main(done for **game1** and **game2** 1.3.2)
3. make palyer object a peremeter for all 4 games(only use player object for peremeters), set the other peremeters inside games(done for **game1** and **game2** 1.3.2)
4. make text files for actual cards
5. make a name database of names for robots in common (done 1.3.2)


Future:
1. maybe put rules in Teller class
---
