# @version ^0.3.7

interface ERC20:
    def transferFrom(asdf: address, sdlf:address, askdf: uint256) -> bool: view

ERC20Contract: public(ERC20)

event Buy:
    seller: address
    buyer: address
    price: uint256

#the amount of time that the auction will be active
duration: public(uint256)
#the seller of the auction item
seller: public(address)
#the starting price of the auction item
startPrice: public(uint256)
#the minimum price that the auction item can reach
endPrice: public(uint256)
#the time that the auction item was created & active
startDate: public(uint256)
#the final date when the auction will end no matter what
endDate: public(uint256)
#the address for the auction item NFT
NFT: public(address)


@external
def __init__(_duration: uint256, _startPrice: uint256, _endPrice: uint256, _NFT: address, Wolvercoin: address):
    assert _endPrice >= _startPrice
    self.duration = _duration
    self.startPrice = _startPrice
    self.endPrice = _endPrice
    self.NFT = _NFT
    self.seller = msg.sender
    self.startDate = block.timestamp
    self.endDate = self.startDate + self.duration
    self.ERC20Contract = ERC20(Wolvercoin)

@external
def getEndDate() -> (uint256):
    return self.endDate

@internal
def transferFrom(_from : address, _to : address, _value : uint256):
    return

@external
def _buy(buyer: address):
    self.transferFrom(buyer, self.seller, self._getPrice())
    self._endAuction()

@internal
def _getPrice() -> (uint256):
    assert self._isItemValid()
    return self.startPrice - self.duration

@internal
def _isItemValid() -> (bool):
    if self.endDate == 0:
        return False
    else:
        return True

@external
def endAuction():
    self.endDate = 0

@internal 
def _endAuction():
#   self.startDate = null
#   if block.timestamp > self.endDate:
    self.endDate = 0
#   if self.buy == False:
#       if self._getPrice() < self.endPrice:
#           self.startDate = 0
#           self.endDate =0
#       self.startDate = 0
#   else:
#       self.endDate = 0

@external
def isAuctionActive():
    assert block.timestamp>= self.startDate
    assert block.timestamp<self.endDate

@external
def getTimeRemaining() -> uint256:
    #return self.endDate - block.timestamp
    return 15
