
<h3>Variables:</h3>

uint256 duration --> time that dutch auction lasts <br>
address seller --> seller of the auction <br>
uint256 startPrice --> starting price <br>
uint256 endPrice --> ending price <br>
uint256 decreaseAmount --> amount of wvc that the price decreases by <br>
uint256 startDate --> starting date <br>
uint256 endDate --> ending date (startDate + duration) <br>
address NFT --> contract address of NFT being auctioned off <br>

<h3>Constructor:</h3>
	Initialize all the variables <br>
	duration --> inputed by user <br>
	startPrice --> inputed by user <br>
	endPrice --> inputed by user <br>
	decreaseAmount --> inputed by user <br>
	seller = msg.sender <br>
	startDate = block.timestamp <br>
	endDate = startDate + duration <br>
	if (startingPrice ≤ endPrice) == false --> starting price is too low and needs to be increased <br>

<h3>Methods:</h3>
_buy --> transacts the NFT from msg.sender to buyer, ends auction by setting dates to null. Needs to pass certain price and date checks to make sure auction is still valid! <br>
_getPrice --> returns current price <br>
_countdown --> returns current time in place of the duration <br>
_endAuction --> sets dates to null, price to null, signaling that auction is over. This only happens when the price goes below the endPrice without _buy being executed or if _buy is not executed before the endDate <br>
    


