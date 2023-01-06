# @version ^0.3.7

interface ERC20:
    def transferFrom(asdf: address, sdlf:address, askdf: uint256) -> bool: view
    def transfer(add: address, val: uint256) -> bool: view

nft: public(ERC20)
nftId: public(uint256)

seller: public(address)
startingPrice: public(uint256)
startAt: public(uint256)
expiresAt: public(uint256)
discountRate: public(uint256)
DURATION: public(uint256)

@external
@payable
def __init__(_startingPrice: uint256, _discountRate: uint256, _nft: address, _nftId: uint256, _duration: uint256):
    self.DURATION = _duration
    self.seller = msg.sender
    self.startingPrice = _startingPrice
    self.startAt = block.timestamp
    self.expiresAt = block.timestamp + self.DURATION
    self.discountRate = _discountRate

    assert _startingPrice >= _discountRate * self.DURATION

    self.nft = ERC20(_nft)
    self.nftId = _nftId

@internal
def getPrice() -> (uint256):
    timeElapsed: uint256 = block.timestamp - self.startAt
    discount: uint256 = self.discountRate * timeElapsed
    return self.startingPrice - discount

@internal
def kill(ad: address):
    selfdestruct(ad)

@external
@payable
def buy():
    assert block.timestamp < self.expiresAt

    price: uint256 = self.getPrice()
    assert msg.value >= price

    self.nft.transferFrom(self.seller, msg.sender, self.nftId)
    refund: uint256 = msg.value - price
    if (refund > 0):
        buyer: address = msg.sender
        self.nft.transfer(buyer, refund)
    self.kill(self.seller)