# Alpha Testing Check List
### Summery:  
Here we have check list for every element of the game
that needs testing. Follow these guidelines to test 
the game rigorously.
____
+ Computer Player Logic Correctness:  
    Ensuring the correctness of Bot classes is a hard task as there are various different cases that can occur. To make testing easier, we would identify different cases, and computer player's expected response in return. 
    We would then construct these cases by skipping all the preliminary conditions of the game.
    We set variables manually and force each other player class to return our chosen card.
    * Black Jack(Leo):  
        - Does the bot class correctly calculate the sum of chosen cards. Add cards to
        the computer and check if the sum is correctly evaluated.
        - Does the bots draw cards exactly 20% of the time. The game delays could be removed
        and the game can be played thousand time. The response of each bot could then be
        statically evaluated. 
        - Does the computer boycott drawing when its card value is above 17. Does it draw
        otherwise. Does it correctly evaluate the chance of other players winning, and 
        choose according to the its outlined logic. 
        - Does the robot pick cards once the sum is over 21.
        - Are the robot cards printed correctly. (In the past it was observed that
        sometimes more or less cards are printed than existing in robot's deck)
        - does find_sum works in finding maximum sum of 21
    * End Phase(Leo):
        - Is the player able to play all cards 
        - Is the bot able to play all cards
        - Does the robot have a strategy to play cards
        - Does the robot play cards in start phase
        - Does the robot discard card according to the rules
        - Can human and AI, AI and AI, AI and human fully function in duel
        - Is all card changes updated and removed from enemy list of bot and handcards
        - Is the game able to end game after player died
        - Does the bot know to use peach, negate, dodge and other defensive cards in order to keep itself alive
        - Can human player equipe equipment cards and benefit from effect
        - Does the player lost after having a sum over 21
    * Court Piece(Amir):
        - Can the bot correctly identify the largest rank of card in its deck.
        Also is it able to find the smallest card of its deck.
        - Does it play a "trump" card when it does not have any suit card. When
        it plays a "trump" does it pick the smallest rank of trump card.
        - The Bot must play a random card when it does not have any of the trump cards.
        In the past it was observed that instead of a random card, no card was returned.
        - Does the Bot play a card of the suit as the first player. It is an important
        role in the court piece and must be followed as long as the computer has 
        that kind of card.
        - Is the bot deck of cards updated correctly. After drawing a card, the card
        must be taken out of the list. It should not be printed later on.
    * Hearts(Amir):
        - Does the bot prioritize, queen of spade, heart cards over other playing
        cards at the exchange phase of the game.
        - When spade is suit of the game and that someone has played a higher rank than
        queen, or when a suit is played that the computer does not have, Queen of spade is
        preferred to be drawn if exist among computer cards. The second option would be 
        a heart card. Is this logic followed by the game.
        - When starting the game, the bot class must prioritize club and diamond over
        hearts and spades to avoid getting a trick. Is this logic followed. In other
        words no heart or spade should be seen while computer has club or diamond in the start.
        - Does the robot returned None at any point of the game. Document the situation
        and find the solution. It might happen when the hearts bot cannot find a solution
        maybe because a special case was not considered.

    * General: 
        - Can player exit all four game and return to lobby
        - Does both winning condition and lost condition leads to reward and punishment
        - Can player buy lost body parts from shop
        - does shop class check if the player have enough money, and does player not have that body part
        - can main code direct player to all four games

<br>

**All requirements met.**