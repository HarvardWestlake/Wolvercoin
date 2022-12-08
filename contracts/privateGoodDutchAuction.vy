

interface Contract:
    def _transfer()

#the amount of time that the auction will be active
duration public(uint256)
#the seller of the auction item
seller public(address)
#the starting price of the auction item
startPrice public(uint256)
#the minimum price that the auction item can reach
endPrice public(uint256)
#the time that the auction item was created & active
startDate public(uint256)
#the final date when the auction will end no matter what
endDate public(uint256)
#the address for the auction item NFT
NFT public(address)

@external
def __init__(_duration: uint256, _startPrice: uint256, _endPrice: uint256, _NFT: address):
    assert _startPrice >= _endPrice
    self.duration = _duration
    self.startPrice = _startPrice
    self.endPrice = _endPrice
    self.NFT = _NFT
    self.seller = msg.sender
    self.startDate = block.timestamp
    self.endDate = self.startDate + self.duration

@external
def _buy(buyer: address):
    Contract._transfer(self.seller, buyer, self._getPrice())
    self._endAuction()

@external
def _getPrice() -> (uint256):
    assert self._isItemValid()

@internal
def _isItemValid() -> (bool):
    if self.endDate == null:
        return False
    else:
        return True

@external
def _endAuction():
    self.endDate = null