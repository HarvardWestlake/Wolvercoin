#Technical Specification for Coin Flip 
> Goal: People can bet an amount of money, and there is a 50% chance they will lose it to the gambling pot and a 50% chance the gambling pot will double their money
> Variables:
>   address gamblingPot -> wallet for gambling money, must be known already
>   address gambler -> wallet that does the coin flip
>   unit256 amount -> amount of money bet
>   uint256 time -> time (for randomness)
> Functions:
> flipCoin (address gambler, uint256 amount)
>   Check that gambler has at least needed amount of wolvercoin
>   If they do not have enought wolvercoin, stop here
>   Otherwise, send amount of wolvercoin to gambling pot
>   Set time variable equal to the time
>   Run flipResult (gambler, time)
>   If flipResult is true, run flipPayment (gambler, amount)
> flipResult (address gambler, unit256 time) -> bool
>   Use the address of the gambler, the time, and a modulo two opperation to get a one or a zero with 50/50 odds
>   If the number is zero, return false
>   If the number is one, return true
> flipPayment (address gambler, uint256 amount)
>   Send 2*amount of wolvercoin from the pot wallet to the gambler wallet
