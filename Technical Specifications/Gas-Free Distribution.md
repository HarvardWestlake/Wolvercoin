> Unknowns / TODO:
> A2: In function 'addStudentAllowance', need to plan and describe mechanism to verify signed and dated student transaction for each allowance added.  Did research for thsi 


 
# Technical Specification for Gas-Free Distribution
> **A1: Active Honors Topcis students only**
> Active students refers to Aug-June of the given graduation year

> Variables:
- activeStudents: Hashmap(studentWallet -> gradYear)
- activeYear: uint256 Store a list of honors topics wallet addresses
- teachers: DynArray[address, 10]
- creator: address

> Functions:
- addStudent(address, uint256 gradYear)
    - adds student address to 'activeStudents' if they don't exist
    - only can be done by teacher

- addTeacher(address)
    - adds a teacher
    - caller must be teacher or contract creator/admin

- checkIfActive(address)    returns:(bool)
    - checks if student is active

> Events:
- Wolvercoin minted
    - Log: Any time a teacher is added or removed
    - Log: When you hit your max gas reimbursed
    - Log: Every reimbursement
    - Log: 



> **A2: AUsers should be able opt to claim an allowance every 1 Day**
> Claiming allowance may incur a gas fee.
>  - Option 1: Pay back gas fee if it's under a certain amount
>  - Option 2: Trigger a script to automatically pay 
>> *Option1* - As it can rely soley on code.  The code can refund the gas fee with a user claims allowances for all students

Variables:
- studentAllowancePayout: DynArray(address, uint256)
- allowanceLastClaimDate: uint256
- allowanceClaimPeriod: uint256
- allowanceAmount: uint256

Functions: 
- addStudentAllowances(address, String[100] signedDatedAllowanceMsg)
     - checks if student is active
     - verifies signedDatedAllowanceMsg is valid
     - adds allowanceAmount to student Allowance Payout

Things not called out:
    - N/A Seems to be programmable 

 **A3: Should be free of charge**
 > However much is being spent on claiming wolvercoin should be given back to the user
 > Only students can reimburse themselves
 > It's automatic until they hit cap

 Variables:
- studentReimbursementCap: uint256
- teachers: DynArray[address, 10]


 Functions:
 - reimburseGas(address, uint256)
    - checks if student is active
    - verifies they haven't hit some cap of reimbursed wei

Log:
 - Log: When the contract runs out of gas to pay students
 - Log: When a student hits their max reimbursed
 - Log: When a grad year changes and who changes it
 
<<<<<<< HEAD
  **PART B**
 
 **B1: Distribute allowance automatically daily**
 > Only distributes to opted-in users.

> Variables
- allowanceAmount: uint256
- optedList: DynArray(address)

Functions: 
- addDailyAllowances(String[100] signedDatedAllowanceMsg)
    - goes through optedList
    - passes parameters to addStudentAllowances

 **B2: Should incur a gas fee done from a foreign account**
 
 > Variables
- chargedAccount: address


> Functions:
- chargeAccount(address)
    - deducts the gas fee amount from the allowance transaction from the account

**B3: Should only happen at Midnight PST**

> Variables:
- triggeredTime: timestamp

> Functions:
- distributeAllowances()
   - calls addDailyAllowances at the specified time

> Events:
- Wolvercoin minted
    - Log: When the clock hits triggeredTime
=======
>>>>>>> main
