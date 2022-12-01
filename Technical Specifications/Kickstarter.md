>//Incomplete
#Technical Specification for Kickstarter Model

>Variables:
communalPrice: uint256 -> total set communal price for a public good
currentAmount: uint256 -> running amount of WVC
goodAddress: address -> address of the public good
donations: HashMap (address -> amount donated)

>Functions:
getPrice -> returns current price
checkGoal -> checks if goal is reached, then public good is achieved
donate -> contribute to public good address until price is met
withdraw -> returns amount donated to public good back into caller's address
endAuction -> reset variables and update Wolvercoin website for public goods displayed