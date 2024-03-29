# Technical Specification for Exclusivity 
> **Function 1: students can use Wolvercoin to vote for initiatives; Mr. Theiss's vote can be weighted up to 15% of the total vote**: 
- Variables:
  - sum: uint256 (balance of votingAddress)
  - classSize: uint256 (number of people in class)
  - percentage: uint256 (sum / classSize * 100)
  - students: HashMap (addresses of students in this class)
  - TheissAddress: address
  - votingAddress: address
- Methods:
  - vote ()
    - if called by a student address -> deposits one coin to the votingAddress each time it is called -- remove their address from hashmap after they vote and sum = sum+1
    - if called by Mr. Theiss's address -> allow him to deposit up to 15% of classSize (use an if statement to check) and sum = sum + amount deposited by Mr. Theiss
  - tallyVotes (sum -> results: boolean)
    - calculate percentage
    - if (percentage > 50) -> return true
    - clear votingAddress
    - reset HashMap of students

> **Function 2: Only Honors topics students can have WolverCoin at full functionality**
> 
> Honors Topics students refers to both current and past students
> 
- Variables:
  - activeStudents: Hashmap(studentWallet -> gradYear)
  - activeYear: address array, store a list of honors topics wallet addresses
  - rickyCWallet: address Stores Ricky C's wallet address
  - creator: address
  - lotteryPot: uint256 Stores wolvercoin lottery pot amount
- Functions:
  - withdraw(amount: uint256 -> message: String)
    - First checks if the wallet address is Ricky C's wallet if his address exists
      - If it is his wallet, only allow 5% of the amount into his wallet and put rest into lottery pot, return "enjoy your joyful pursuit of excellence!"
    - Then, checks if wallet is Honors Topic Student
      - If student, allow full withdraw amount
      - If not, half withdraw amount and put the half into lottery pot

> **Function 3: Honors Topics Student can unanimously vote a non Honors Topics Student to be considered an honors topics student by Wolvercoin or excommunicate an Honors Topics Student from being considered one**
- Variables: 
    - topicsAddress : Array of honors topics students’ wallet addresses
- Methods:
    - addNonTopics (parameter: address of contender to be added as topics student)
        - Look at voting method from function 1
          - Use address from voting method and see current balance 
	      - If percentage from vote >= 1, then student can be added into topicsAddress array
	- removeTopics (parameter: address of contender to be removed as topics student)
	  	- Look at voting method from function 1
		    - Use address from voting method and see current balance 
		  - If percentage from vote >= 1, then student is removed from topicsAddress array
