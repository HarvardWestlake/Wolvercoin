//INCOMPLETE

Variables: 

duration --> uint256 
//time that dutch auction lasts
seller --> address 
//seller of the auction
startPrice --> uint256 
currentPrice --> uint256
endPrice --> uint256 
decreaseAmount --> uint256
//amount of wvc that the price decreases by
startDate --> uint256
endDate -->uint256
//(startDate + duration)
NFT --> address
contract address of NFT being auctioned off

methods:

constructor:
	Initialize all the variables
	duration --> inputed by user
	startPrice --> inputed by user
	currentPrice = startPrice
	endPrice --> inputed by user
	decreaseAmount --> inputed by user
	seller = msg.sender
	startDate = block.timestamp
	endDate = startDate + duration
	if (startingPrice ≤ endPrice) == false --> starting price is too low and needs to be increased


_buy (buyer--> address, currentPrice)
	check if buyer has enough money to buy the NFT
		sends the money from buyer
	 	sends the NFT from msg.sender to buyer

_getPrice()
  returns current price

_countdown ()
	 returns current time in place of the duration 

_quit ()
behavoir:
	ends the auction
     	update startDate to a time in the future
     	update ending date to be startDate + duration

	


