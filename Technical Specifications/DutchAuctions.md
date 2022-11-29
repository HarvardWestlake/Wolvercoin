//INCOMPLETE

Variables: 

uint256 duration --> time that dutch auction lasts
address seller --> seller of the auction
uint256 startPrice --> starting price
uint256 endPrice --> ending price
uint256 decreaseAmount --> amount of wvc that the price decreases by
uint256 startDate --> starting date
uint256 endDate --> ending date (startDate + duration)
address NFT --> contract address of NFT being auctioned off

constructor:
	Initialize all the variables
	duration --> inputed by user
	startPrice --> inputed by user
	endPrice --> inputed by user
	decreaseAmount --> inputed by user
	seller = msg.sender
	startDate = block.timestamp
	endDate = startDate + duration
	if (startingPrice ≤ endPrice) == false --> starting price is too low and needs to be increased

methods:
_buy --> transacts the NFT from msg.sender to buyer
_getPrice --> returns current price
_countdown --> returns current time in place of the duration 
