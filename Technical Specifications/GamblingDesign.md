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