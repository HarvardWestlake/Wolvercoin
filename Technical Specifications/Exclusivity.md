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
