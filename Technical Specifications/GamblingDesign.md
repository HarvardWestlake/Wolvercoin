#Technical Specification for the pot
> - Variables:
> -   address pot -> the pot account; will have some sha with near all or all 0s
> - Functions:
> - potTax (address account, uint256 transactionVal)
> -   Called every transaction, the sender is fed in
> -   3 and a third of a percent of transactionVal is deducted from account and added to pot

#Technical Specification for Lottery
> - Variables:
> -   uint256 tickets -> the number of tickets a given account possesses (one variable per account), in the smallest unit WC can be divided into
> -   uint256 timeSinceLastDrawing -> the number of miliseconds since last drawing
> - Functions:
> - buyTickets (address account, uint256 coin)
> -   checks that the person making the request is the account
> -   checks that the account has the amount of coin (in the smallest part that WC can be divded in) represented by coin
> -   deducts coin from account
> -   adds 2.5 * coin to the tickets of account
> - tickLottery()
> -   called every block
> -   adds the number of ms since last block to timeSinceLastDrawing
> -   if timeSinceLastDrawing exceeds 6.048e+8, call lottery()
> - lottery()
> -   traverse through all accounts, summing the number of tickets and smallest divisible units of WC
> -   generate a random number from 0 to that sum
> -   traverse through all accounts, deducting the number of tickets and smallest divisible units of WC held by each, until the the sum is zero
> -   reduce the pot size by 1/3 and add that reduction value to the current account

#Technical Specification for crash gambling
> - Goal: People can bet an amount of money, and each block the money multipler goes up by 0.1 from 0.1 to start, and also there's a 10% chance that there's a "crash" and everyone gets their original bet * the current multipler. Then another round of betting opens for one block and it repeats
> - Variables:
> -   boolean justCrashed -> record of if there was a crash the block before
> -   string[][] crashBets -> 2 rows, first row is account shas, second row is bet amounts in WC
> -   int multiplier -> represents percent multiplier (divided by ten). increases by 1 every block
> - Functions:
> - placeBet (address gambler, uint256 amount)
> -   Check that the gambler is making the request, that they have the needed WC, and that justCrashed is true.
> -   If not any of them, end
> -   If both, transact that amount of money to the pot and record the gambler and the bet in crashBets
> - withdrawBet (address gambler)
> -   Verify identity of person requesting to withdraw bet
> -   Transfer to the gambler their associated bet in crashBets * multipler / 10
> -   Remove their entry from crashBets
> - updateCrash () -> runs once per block
> -   Check if justCrashed is true. 
> -   If it is, run resetCrash().
> -   If it's false, run crashGamble().
> - crashGamble()
> -   Generate a random number from 0-1. 
> -   If it's above 0.9, set justCrashed to true.
> -   Otherwise, increase the multipler by 1.
> - resetCrash()
> -   Set justCrashed to false
> -   Set multipler to 0
> -   Clear crashBets (money not returned to gamblers still in it)
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