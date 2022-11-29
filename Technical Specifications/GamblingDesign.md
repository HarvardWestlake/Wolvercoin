##Technical Specification for Roulette 
> Variables
> - roulette: Hashmap with an integer representing the roulette slot and Boolean representing the color (true=red, false=black, or vice versa), each entry representing a slot on roulette wheel
> - betCoins: a decimal variable containing amount of WC bet
> - bet: a String input from the player saying what they're bettting (ex. even, 14, odd, high, etc)
> - win: a boolean variable, true if won, false if lost

> Functions
> >playRoulette
> - get input string from player, store into bet
> - generate random number from 1 to 36 , get 
> - if bet says even or odd, check if 

original design:
> - A classic the world around
> - Text based just like the good old days
> - In the game, a player may choose to place a bet on a single number, the color red or black, whether the number is odd or even, or if the numbers are high (19–36) or low (1–18)
> - Then a random number and color gets chosen
> - If your bet is correct (win), win however much you would, otherwise all money goes to pot