// THIS HAS BEEN COPY PASTED FOR FORMATTING

#Technical Specification for Exclusivity 
> **Function 1 (INCOMPLETE): 
> - each person is allowed to deposit one coin into a designated address as a vote (people can use the deposit method?)
> - count number of coins
> - allow Mr. Theiss to deposit up to 15% of that number of coins -- use an if statement to prevent him from depositing more (? -- this should probably be changed)
> - if percentage of number of coins deposited / number of people in class > 50% -> allow the initiative to pass
> - Variables:
> - sum: counts number of coins in the designated address
> - percentage: percentage of number of coins deposited / number of people in class
> return a boolean of true or false depending on if the initiative passes
> clear the designated address
> should we create a separate coin for voting? or just use Wolvercoin?
# Techinical Specifications for Exclusivity
> **Function 2: Only Honors topics students can have WolverCoin at full functionality**
> Honors Topics students refers to both current and past students
> Variables:
- activeStudents: Hashmap(studentWallet -> gradYear)
- activeYear: uint256 Store a list of honors topics wallet addresses
- rickyCWallet: address Stores Ricky C's wallet address
- creator: address
- lotteryPot: uint256 Stores wolvercoin lottery pot amount
> Functions:
- withdraw(amount: uint256 -> message: String)
  - First checks if the wallet address is Ricky C's wallet if his address exists
    - If it is his wallet, only allow 5% of the amount into his wallet and put rest into lottery pot, return "enjoy your joyful pursuit of excellence!"
  - Then, checks if wallet is Honors Topic Student
    - If student, allow full withdraw amount
    - If not, half withdraw amount and put the half into lottery pot
