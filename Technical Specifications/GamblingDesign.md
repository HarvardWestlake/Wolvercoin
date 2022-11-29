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
> - 