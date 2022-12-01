#Technical Specification for the pot
> - One account which is all zeros followed by a one will handle all gambling money and will be called the pot
> - This account will receive 3 and a third percent of all transactions as a tax (2/3 of total 5% tax), which will be coded into the transact function

#Technical Specification for Lottery
> - Each account will have a "tickets" variable
> - At any time, an account may exchange one Wolvercoin for 2.5 tickets (or equivalent)
> - There will be a "last lottery drawing time" variable
> - Every time there is a lottery drawing, this variable will be updated to the current time
> - Every transaction will check if it has been a week since the last drawing, and if it has, it will run a function called "runLottery"
> - runLottery will traverse through all accounts and sum all tickets and Wolvercoin and store this number as a variable
> - Then, it will generate a random number between 0 and that sum. Then, it will traverse the accounts again, and stop when it's traversed through enough tickets / WC that it reaches the random number. Then, it will give 1/3 of whatever is stored in the pot to that account.

#Technical Specification for crash gambling
> - There will be a boolean called "justCrashed", a 2d array of accounts and bets called "crashBets", and an int called "multiplierPercent"
> - There will be a method called "placeBet", which will take in an account and a bet, record them in the crashBets array, and move the amount of WC in the bet to the pot. But if justCrash is false, it will do nothing.
> - Each block, there will be a check for if justCrashed is true, and if it is, it will be set to false the next block. multiplierPercent will also be set to 0.
> - Each block when justCrashed is false, multiplierPercent will be increased by 10. There will also be a random double between 0 and 1 generated. If it's above 0.9, set justCrashed to true, and (return bets - this part isn't finished)

#Technical Specification for Coin Flip 
> - Goal: People can bet an amount of money, and there is a 50% chance they will lose it to the gambling pot and a 50% chance the gambling pot will double their money
> - Variables:
> -   address gamblingPot -> wallet for gambling money, must be known already
> -   address gambler -> wallet that does the coin flip
> -   unit256 amount -> amount of money bet
> -   uint256 time -> time (for randomness)
> - Functions:
> - flipCoin (address gambler, uint256 amount)
> -   Check that gambler has at least needed amount of wolvercoin
> -   If they do not have enought wolvercoin, stop here
> -   Otherwise, send amount of wolvercoin to gambling pot
> -   Set time variable equal to the time
> -   Run flipResult (gambler, time)
> -   If flipResult is true, run flipPayment (gambler, amount)
> - flipResult (address gambler, unit256 time) -> bool
> -   Use the address of the gambler, the time, and a modulo two opperation to get a one or a zero with 50/50 odds
> -   If the number is zero, return false
> -   If the number is one, return true
> - flipPayment (address gambler, uint256 amount)
> -   Send 2*amount of wolvercoin from the pot wallet to the gambler wallet

##Technical Specification for Roulette 
> Variables:
> - roulette: Hashmap with an integer representing the roulette slot and Boolean representing the color (true=red, false=black, or vice versa), each entry representing a slot on roulette wheel
> - betCoins: a decimal variable containing amount of WC bet
> - bet: a String input from the player saying what they're bettting (ex. even, 14, odd, high, etc)
> - win: a boolean variable, true if won, false if lost

> Functions:
> - playRoulette
> - get input string from player, store into bet
> - generate random number from 1 to 36 , get 
> - if bet says even or odd, check if 

##Rejected Features
> Sports Betting:
> - Impossible to implement because it would require interaction with HW website and manual input of game scores
> Blackjack:
> - Difficult to implement because the user would have to interact with the blockchain over the course of many blocks as the game progresses
> - For this to be implemented, there would have to be a loop of contract -> player choice -> contract interactions
> Numerous Betting Strategies:
> - Design says to implement a list of 18 complex betting strategies for roulette
> - Difficult to implement and not necessary, so simpler version should be programmed