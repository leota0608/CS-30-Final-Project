# CS-30-Final-Project
<br><br>
x.y.z  
x: represents the coder ID  
- Amir uses code 0  
- Leo uses code 1  
y: the version number  
z: commit number  
example:  
0.1.1 means amir committed his first commit to version 1.  
## Change Log
> 12.20  

0.3.4:
- The human logic for the game of hearts was developed.
- The game was debugged.
0.3.3:
- playing logic for robot of the game of hearts was developed.
0.3.2:
- The game of Hearts is now able to distribute cards among players
- It is also able to exchange cards with adjacent players.
0.3.1:
- The files for game of Hearts was created
- The file CPCard was renamed GameCard and moved to the common
folder.
0.2.5:
- The teller class is enabled to interrupt itself, by asking
the user a question, if they would like to continue.
- Court Piece rules were written into a file and are being
displayed to user.
0.2.4:
- The CourtPiece game had been debugged.
- Teller class had been added to print long explanations
in a interactive manner.
0.2.3:
- The game handler class had been created.
  + CourtPiece class puts all the players together
  and enforces the rules of the game.
0.2.2:
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


1.1.# 
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
>12.20  

- finish game 2
    > 12.21  
    + add the rules of the game and stored it as a `.txt` file (`rules..txt` in *game 2* folder)
    + add some animation(print rules word by word, add screen flickering when the player lost and loses a body part)
    + debug game 2 
    + `main.py` can now read results from `main.py` in *game 2* folder and update score, game results and lost body parts in `playingRecord.json` in *player* folder
    
> 12.24 1.2.3

- debug game1
- Need to be added:
    + More card operations
    + AI moves
    + Fix bugs......
> 1.2.4
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