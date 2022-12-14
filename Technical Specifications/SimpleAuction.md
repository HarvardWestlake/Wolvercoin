Technical Specifications for Simple Open Auction

### Variables:

- address : beneficiary (receives money from highest bidder)
- uint256 : auctionStart 
- uint256 : auctionEnd
- address : highestBidder
- uint256 : highestBid
- bool : ended (true at end of auction, no more changes)
- pendingReturns: HashMap[address,uint256] (keep track of refunded bids)

### Constructor:
>Inputs:
  - address : beneficiary 
  - uint256 : auctionStart
  - uint256 : biddingTime
> Functionality
- Set variables to matching inputs, set end time to start + bidding time
- Make sure auctionEnd is in the future

### Methods: 
- Bid() - payable
  - Checks if auction has started and has not ended
  - If value > highest bid, set highest bidder as sender and highest bid as msg value
- Withdraw()
  - Find amount they withdraw from pendingReturns HashMap, send them that amount
  - Set their pending return to 0
- EndAuction()
  - Check if block time has passed end of auction
  - If not already ended, end auction and send beneficiary highest bid
