### Variables:

- uint256 duration --> time that dutch auction lasts 
- address seller --> seller of the auction 
- uint256 startPrice --> starting price 
- uint256 endPrice --> ending price 
- uint256 startDate --> starting date 
- uint256 endDate --> ending date (startDate + duration) 
- address NFT --> contract address of NFT being auctioned off 

> Price is not stored; it is dynamically calculated based on the current time and the startPrice, endPrice, startDate, and endDate. 

### Constructor:
- Initialize all the variables 
- duration --> inputed by user 
- startPrice --> inputed by user 
- endPrice --> inputed by user 
- seller = msg.sender 
- startDate = block.timestamp 
- endDate = startDate + duration 
- if (startingPrice ≤ endPrice) == false --> starting price is too - low and needs to be increased 

### Methods:
- _buy --> transacts the NFT from msg.sender to buyer, ends auction - by setting dates to null. Needs to pass certain price and date - checks to make sure auction is still valid! 
- _getPrice --> returns current price 
- _countdown --> returns current time in place of the duration 
- _endAuction --> sets dates to null, price to null, signaling that - auction is over. This only happens when the price goes below the - endPrice without _buy being executed or if _buy is not executed - before the endDate 
    


