# @version ^0.3.7
#Depends on ERC20 Wolvercoin contract, could interact with PublicGoods,DutchAuction in the future

interface Wolvercoin:
    def sendW(receiver:address, val: uint256) -> bool: nonpayable
    def transferW(sender:address, receiver:address, val:uint256) -> bool:nonpayable

wolvercoin: Wolvercoin
#Simple Open Auction from VyperDocs
#Auction Variables
beneficiary: public(address)
auctionStart: public(uint256)
auctionEnd: public(uint256)
highestBidder: public(address)
highestBid: public(uint256)
minValue: public(uint256)
ended: public(bool)
pendingReturns: public(HashMap[address,uint256])

event AuctionFinished:
    highestBidder: address
    highestBid: uint256

#Constructor
@external
def __init__(benef: address, start: uint256, time: uint256, _wolvC: Wolvercoin, minV: uint256):
    self.beneficiary = benef
    self.auctionStart = start
    self.auctionEnd = start + time
    assert block.timestamp < self.auctionEnd
    self.wolvercoin = _wolvC
    self.minValue = minV

#Wolvercoin methods
#SendW : interfaced method to send wolvercoin to address
@internal
def sendW(_receiver : address, _val : uint256):
    return
#TransferW : interfaced method to transfer wolvercoin from one address to another address 
@internal
def transferW(_sender:address, _receiver:address,_val:uint256):
    return

#Methods
#Bid: if the message value is the highest so far, set variables to match current sender and value to highest bidder and bid
@external
@payable
def bid():
    assert block.timestamp >= self.auctionStart
    assert block.timestamp < self.auctionEnd
    assert msg.value > self.minValue
    assert msg.value > self.highestBid
    self.pendingReturns[self.highestBidder] += self.highestBid
    self.highestBidder = msg.sender
    self.highestBid = msg.value

#Withdraw: should be able to quickly return amount from hashmap
@external
def withdraw():
    assert not self.pendingReturns[msg.sender] == 0 
    pending_amount: uint256 = self.pendingReturns[msg.sender]
    self.pendingReturns[msg.sender]=0
    self.sendW(msg.sender,pending_amount)
    #is it actually from beneficiary? might not be correct here

#endAuction: as long as time is passed auction end, end auction and disallow changes to variables
@external
def endAuction():
    assert block.timestamp >= self.auctionEnd
    assert not self.ended
    self.ended = True
    self.transferW(self.highestBidder,self.beneficiary, self.highestBid)


