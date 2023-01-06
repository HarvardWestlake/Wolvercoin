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
    name: String[50] # See PublicGoods for a similar implementation of the names
    seller: address
    startPrice: uint256
    endPrice: uint256
    startDate: uint256
    endDate: uint256
    nftTokenId: address

auctionItems: public(HashMap[String[50], AuctionItem])
erc20: ERC20WithAdminAccess
erc721: ERC721WithAdminAccess

@external
def __init__(erc20address: address, erc721address: address):
    self.erc20 = ERC20WithAdminAccess(erc20address)
    self.erc721 = ERC721WithAdminAccess(erc721address)


# To call this function, one must approve the transfer via 721
@external
def createAuctionItem(name: String[50], startPrice: uint256, endPrice: uint256, startDate: uint256, endDate: uint256, nftTokenId: address):
    assert name != ""
    assert endPrice > 0
    assert startPrice > endPrice
    assert startDate > block.timestamp
    assert endDate > startDate
    assert self.erc721.ownerOf(nftTokenId) == msg.sender

    self.auctionItems[name] = AuctionItem({
        name: name,
        seller: msg.sender,
        startPrice: startPrice,
        endPrice: endPrice,
        startDate: startDate,
        endDate: endDate,
        nftTokenId: nftTokenId
    })
    # Move the NFT to the property of this contract for safekeeping
    self.erc721._transferFrom(msg.sender, self, nftTokenId)

@external
def getPrice(name: String[50]) -> uint256:
    assert name != ""
    auctionItem: AuctionItem = self.auctionItems[name]
    assert auctionItem.name == name
    assert msg.timestamp > auctionItem.startDate
    
    if msg.timestamp > auctionItem.endDate:
        return auctionItem.endPrice

    # Linearly interpolate to find the price
    timeSinceStart: uint256 = msg.timestamp - auctionItem.startDate
    totalDuration: uint256 = auctionItem.endDate - auctionItem.startDate
    priceRange: uint256 = auctionItem.startPrice - auctionItem.endPrice
    progress: uint256 = timeSinceStart / totalDuration
    return auctionItem.endPrice + priceRange * progress

# To call this function, one must approve the monetary transfer via 20
@external
def buy(name: String[50]):
    assert name != ""
    auctionItem: AuctionItem = self.auctionItems[name]
    assert auctionItem.name == name

    assert msg.timestamp > auctionItem.startDate
    price: uint256 = self.getPrice(name)
    assert self.erc20.getBalanceOf(msg.sender) >= price

    self.erc20.transferFrom(msg.sender, auctionItem.seller, price)
    self.erc721.transferFrom(self, msg.sender, auctionItem.nftTokenId)


#region Trivial getters
@external
def getSeller(name: String[50]) -> address:
    assert name != ""
    auctionItem: AuctionItem = self.auctionItems[name]
    assert auctionItem.name == name
    return auctionItem.seller
@external
def getStartDate(name: String[50]) -> uint256:
    assert name != ""
    auctionItem: AuctionItem = self.auctionItems[name]
    assert auctionItem.name == name
    return auctionItem.startDate
@external
def getEndDate(name: String[50]) -> uint256:
    assert name != ""
    auctionItem: AuctionItem = self.auctionItems[name]
    assert auctionItem.name == name
    return auctionItem.endDate
@external
def getStartPrice(name: String[50]) -> uint256:
    assert name != ""
    auctionItem: AuctionItem = self.auctionItems[name]
    assert auctionItem.name == name
    return auctionItem.startPrice
@external
def getEndPrice(name: String[50]) -> uint256:
    assert name != ""
    auctionItem: AuctionItem = self.auctionItems[name]
    assert auctionItem.name == name
    return auctionItem.endPrice
@external
def getNFT(name: String[50]) -> address:
    assert name != ""
    auctionItem: AuctionItem = self.auctionItems[name]
    assert auctionItem.name == name
    return auctionItem.nftTokenId
#endregion
