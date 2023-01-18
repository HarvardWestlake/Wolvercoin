# @version ^0.3.7

# vyper.interfaces.ERC20 does not include the mint and burn functions so we make our own interface
interface ERC20WithAdminAccess:
    def getBalanceOf(_address: address) -> uint256: nonpayable
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: nonpayable
    def approve(_spender : address, _value : uint256) -> bool: nonpayable

interface ERC721WithAdminAccess:
    def ownerOf(_tokenId: uint256) -> address: nonpayable
    def transferFrom(_from: address, _to: address, _tokenId: uint256): nonpayable

struct AuctionItem:
    nftTokenId: uint256
    seller: address
    startPrice: uint256
    endPrice: uint256
    startDate: uint256
    endDate: uint256

auctionItems: public(HashMap[uint256, AuctionItem]) # A map of nftTokenId to AuctionItem
auctionItemsArr: public(DynArray[uint256, 100]) # A list of the nftTokenIds of all the auction items currently active
erc20: ERC20WithAdminAccess
erc721: ERC721WithAdminAccess

@external
def __init__(erc20address: address, erc721address: address):
    self.erc20 = ERC20WithAdminAccess(erc20address)
    self.erc721 = ERC721WithAdminAccess(erc721address)

@internal
def findIndexOfItemInItemsArr(nftTokenId: uint256) -> int256:
    for i in range(100):
        if self.auctionItemsArr[i] == nftTokenId:
            return i
    return -1

# To call this function, one must approve the transfer via 721
@external
def createAuctionItem(startPrice: uint256, endPrice: uint256, startDate: uint256, endDate: uint256, nftTokenId: uint256):
    assert endPrice > 0
    assert startPrice > endPrice
    assert startDate >= block.timestamp
    assert endDate > startDate
    assert self.erc721.ownerOf(nftTokenId) == msg.sender

    # Move the NFT to the property of this contract for safekeeping
    self.erc721.transferFrom(msg.sender, self, nftTokenId)
    
    self.auctionItems[nftTokenId] = AuctionItem({
        nftTokenId: nftTokenId,
        seller: msg.sender,
        startPrice: startPrice,
        endPrice: endPrice,
        startDate: startDate,
        endDate: endDate
    })
    self.auctionItemsArr.append(nftTokenId)

@internal
def _getPrice(nftTokenId: uint256) -> uint256:
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId
    assert block.timestamp >= auctionItem.startDate
    
    if block.timestamp >= auctionItem.endDate:
        return auctionItem.endPrice

    # Linearly interpolate to find the price
    timeSinceStart: uint256 = block.timestamp - auctionItem.startDate
    totalDuration: uint256 = auctionItem.endDate - auctionItem.startDate
    priceRange: uint256 = auctionItem.startPrice - auctionItem.endPrice
    progress: decimal = convert(timeSinceStart, decimal) / convert(totalDuration, decimal)
    return convert(convert(auctionItem.startPrice, decimal) - convert(priceRange, decimal) * progress, uint256)

@external
def getPrice(nftTokenId: uint256) -> uint256:
    return self._getPrice(nftTokenId)

# To call this function, one must approve the monetary transfer via 20
@external
def buy(nftTokenId: uint256):
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId

    assert block.timestamp > auctionItem.startDate
    price: uint256 = self._getPrice(nftTokenId)
    assert self.erc20.getBalanceOf(msg.sender) >= price

    self.erc20.transferFrom(msg.sender, auctionItem.seller, price)
    self.erc721.transferFrom(self, msg.sender, auctionItem.nftTokenId)

    self.auctionItems[nftTokenId] = empty(AuctionItem)
    i: int256 = self.findIndexOfItemInItemsArr(nftTokenId)
    if i != -1:
        self.auctionItemsArr[i] = self.auctionItemsArr[len(self.auctionItemsArr) - 1] # Make the last element take the one you want to remove's place...
        self.auctionItemsArr.pop() # ...and then remove the last element

@external
def getActiveAuctionItems() -> DynArray[uint256, 100]:
    return self.auctionItemsArr

@external
def _countdown(nftTokenId: uint256) -> uint256:
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId

    assert block.timestamp > auctionItem.startDate
    
    if block.timestamp <= auctionItem.endDate:
        return auctionItem.endDate-block.timestamp
    else:
        return 0
    
    

@external
def endAuction(nftTokenId: uint256):
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId
    auctionItem.endDate = 0

#region Trivial getters
@external
def getSeller(nftTokenId: uint256) -> address:
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId
    return auctionItem.seller
@external
def getStartDate(nftTokenId: uint256) -> uint256:
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId
    return auctionItem.startDate
@external
def getEndDate(nftTokenId: uint256) -> uint256:
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId
    return auctionItem.endDate
@external
def getStartPrice(nftTokenId: uint256) -> uint256:
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId
    return auctionItem.startPrice
@external
def getEndPrice(nftTokenId: uint256) -> uint256:
    auctionItem: AuctionItem = self.auctionItems[nftTokenId]
    assert auctionItem.nftTokenId == nftTokenId
    return auctionItem.endPrice

#endregion
