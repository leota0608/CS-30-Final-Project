# CS-30-Final-Project
<br><br>

# Development Work
- [Code Planning](#code-planning)
- [Tasks To Be Completed](#tasks-to-be-completed)
- [Game Overview](#game-overview)
    + [Game 1](#game-1)
    + [Game 2](#game-2)
    + [Game 3](#game-3)
    + [Game 4](#game-4)
- [Coding preparation](#coding-preparation)

## Code Planning
### Main code
The main code imports the `Game` module, which then imports the four mini games and ...not finished
### Modules
- Game (the code that handles the whole gaming process)
- mini game1 ([More Information](#game-1-modules))
- mini game2 ([More Information](#game-2-modules))
- mini game3 ([More Information](#game-3-modules))
- mini game4 ([More Information](#game-4-modules))
- Store (Wish List)
- Player
- Format (a class that prints something fancy on the interface)

#### Game 1 Modules
- `Player` Module(Class): this class will include some basic moves a player would need, such as drawing cards, and data like `health`, `name` and `handcards`.
- `Bot` Module(Class): this class will be a `children class` of the Player class, having new methods like evluateing moves, making decision on it self on what card to play.
- `Format` Module: this file will include functions or classes to improve UI, such as making new lines, outputing card shapes...
- `Deck` Module(Class): this class will be stroing all the cards. It will have methods like randomizing  cards, and drawing a certain number of cards.
- `Card` Module(Class): this class have attributes like [card types](#types-of-cards) and card name
- `Choose` Module(Class): this class will handle all user inputs, including exceptions, confirmation, and checking input range.
- `Main` main file (Class): this class will run mini-game1.


#### Game 2 Modules
#### Game 3 Modules
#### Game 4 Modules

## Tasks To Be Completed


## Game Overview
The plan is to create a game including several mini games, where the player can move in the map to play different games to survive.
<hr>

### Game 1
<b>What is looks like:</b>  
Two or more people can play the game. For each turn, there are [three phases](#game-phases) for each player, and players take turns to play. The last player alive is the winner. The game requires combat, strategy, and thinking.

Initially, each player draws **`4`** cards from the deck of cards and add them to their `handcard`. Each player has an initial max health points of **`4`**. When a player's health points equal to `0`, the player loses unless the player uses a [`Peach`](#types-of-cards).
#### Game Phases
1. <b>Draw Phase</b>  
In this phase, the player in this turn draws `2` cards from the top of the deck of cards, and add them to the player's [`handcards`](#handcards).
2. <b>Action Phase</b>  
In this phase, the player in this turn can play cards to attack, heal, or use `trick cards` ([More information about types of cards](#types-of-cards)). If other player(s) got attacked, they can choose to play certain cards to defend.
3. <b>Discard Phase</b>  
In this phase, the player in this turn discards his(her) [`handcards`](#handcards) so that the number of `handcards` is equal to the player's current [`health points`](#health-points)(if number of current hand cards is greater than the player's health points).
#### Types of Cards
**Basic Cards:**  
- **`Slash`**: attack card, needs `Dodge` to deflect, if opponent player didn't dodge, the opponent lose `1` health point. It can also used in `duel` or `savage`
- **`Dodge`**: defence card, can't be used directly, can deflect `Dodge` or used in `archery`
- **`Peach`**: healing card, can be used by player in action phase to heal `1` health point or when just got killed  
  
**Equipment Cards:**  
- **`Crossbow`**: a player equipted with this weapen can use [`Slash`](#types-of-cards) infinite times in his handcard.
- **`Doubleblade`**: a player equipted with this weapen can use `Slash` as [`Dodge`](#types-of-cards) and use `Dodge` as `Slash`  
  
**Trick Cards:**
- **`Duel`**: the player who play this card chooses a target player, the target must respond first by playing a `Slash` card. If they play a `Slash`, then the player must play a Slash. This process continues until one player cannot or chooses not to play a Slash and loses **`1`** health point.  
- **`Dismantle`**: the player who play this card can remove one card from a target player's `handcard` or [`equipment area`](#equipment-area).
- **`Snatch`**: the player who play this card can take one card from a target player's `handcard` or `equipment area` and add it to the player's `handcard`.  
- **`Archery`**: when a player play this card, every player(including the player himself) needs to play an `Dodge`. Those who cannot or choose not to will loose **`1`** health point.
- **`Savage`**: when a player play this card, every player(including the player himself) needs to play an `Slash`. Those who cannot or choose not to will loose **`1`** health point.
- **`Benevolence`**: the player who play this card draws two cards from the deck of cards immediately and add them to the player's `handcard`.
- **`Negate`**: this card can be used to deflect any other `trick` card aimed at you(ex: `Duel`, `Snatch`, `Archery`, etc).

#### Handcards
A number of cards that the player held, drawn from the deck of cards.  
A player's handcard can't be seen by any other player.
#### Equipment Area
The place where players can equip their `Equipment Cards`, which doesn't take up handcard number limit at the `discard phase`.
Cards equiped in this area are targets of `Dismantle` and `Snatch`.  
<hr>

### Game 2:
Black Jack
> Briefly talk about what the game is like and some elements in it.
<hr>

### Game 3: ???
> Briefly talk about what the game is like and some elements in it.
<hr>

### Game 4: ???
> Briefly talk about what the game is like and some elements in it.

> Maybe more?
<br><br>

## Coding preparation
The classes and external files in the program will be explained as the following, taking Game 1 as an example.
### Classes

<br><br>

