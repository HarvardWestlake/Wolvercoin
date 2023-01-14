# @version ^0.3.7

interface IERC721:
    def transferFrom(_from: address, _to: address, _NFTID: uint256) -> bool: view
    
interface Token:
    def transfer(add: address, val: uint256) -> bool: view


nft: public(IERC721)
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

    self.nft = IERC721(_nft)
    self.nftId = _nftId


@external
def getDURATION() -> (uint256):
    return self.DURATION


@external
def getSeller() -> (address):
    return self.seller


@external
def getStartingPrice() -> (uint256):
    return self.startingPrice


@external
def getStartAt() -> (uint256):
    return self.startAt


@external
def getExpiresAt() -> (uint256):
    return self.expiresAt


@external
def getDiscountRate() -> (uint256):
    return self.discountRate


@external
def getNftId() -> (uint256):
    return self.nftId


@external
def getNft() -> (Token):
    return self.nft


@internal
def _getPrice() -> (uint256):
    timeElapsed: uint256 = block.timestamp - self.startAt
    discount: uint256 = self.discountRate * timeElapsed
    return self.startingPrice - discount


@external
def getPrice() -> (uint256):
    return self._getPrice()


@external
@payable
def buy():
    assert block.timestamp <= self.expiresAt

    price: uint256 = self._getPrice()
    assert msg.value >= price

    self.nft.transferFrom(self.seller, msg.sender, self.nftId)
    refund: uint256 = msg.value - price
    if (refund > 0):
        buyer: address = msg.sender
        Token(msg.sender).transfer(buyer, refund)
    selfdestruct(self.seller)