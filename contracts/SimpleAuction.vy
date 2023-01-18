# @version ^0.3.7
#Depends on ERC20 Wolvercoin contract
#Could interact with ActiveUser, NFT, PublicGoods,DutchAuction depending on implementation

#INTERFACES
interface Token:
    def getBalanceOf(_address:address) -> uint256: nonpayable
    def transferFrom(sender:address, receiver:address, val:uint256) -> bool: nonpayable
    def approve(_spender : address, _value : uint256) -> bool: nonpayable


interface NFT:
    def ownerOf(tokenID: uint256) -> address: nonpayable
    def transferFrom(_from: address, _to: address, tokenID: uint256): nonpayable

#interface ActiveUser:
#    def getIsActiveUser(potentialUser: address) -> bool: view
#    def getIsAdmin(potentialAdmin: address) -> bool: view



#Auction Item Variables and Object
struct AuctionItem:
    nftTokenID: uint256
    beneficiary: address
    auctionStart: uint256
    auctionEnd: uint256
    highestBidder: address
    highestBid: uint256
    minValue: uint256
    ended: bool
    hasBid: bool
     

#Auction structures
auctionItems: public(HashMap[uint256, AuctionItem]) #all auction item NFT IDs -> item struct
activeItems: public(DynArray[uint256,100]) #all currently active/selling item IDs
pendingReturns: public(HashMap[address,uint256]) #map of people who have bid but didn't win + their investments to return
pendingPeople: public(DynArray[address,300]) #List of people who are owed returns 
wolvercoin: Token
auctionNFT: NFT
#activeUser: ActiveUser

event AuctionFinished:
    highestBidder: address
    highestBid: uint256

#Constructor
@external
def __init__(wolvercoinAddress: address, nftAddress: address):#activeUserAddress: address
    self.wolvercoin = Token(wolvercoinAddress)
    self.auctionNFT = NFT(nftAddress)
    #self.activeUser = ActiveUser(activeUserAddress)

#Auction methods
@external
def createAuctionItem(tokenID: uint256, benef:address, start: uint256, end: uint256, minVal: uint256):
    assert end > start
    assert start >= block.timestamp
    assert block.timestamp < end
    assert self.auctionNFT.ownerOf(tokenID) == self.auctionNFT.address
    #assert self.activeUser.getIsAdmin(msg.sender)

    self.auctionNFT.transferFrom(self.auctionNFT.address,self,tokenID)#During auction NFT is owned by auction contract

    self.auctionItems[tokenID] = AuctionItem({
        nftTokenID: tokenID,
        beneficiary: benef,
        auctionStart: start,
        auctionEnd: end,
        highestBidder: msg.sender,
        highestBid:minVal,
        minValue: minVal,
        ended: False,
        hasBid: False,
    })
    self.activeItems.append(tokenID)


#Bid: if the message value is the highest so far, set variables to match current sender and value to highest bidder and bid
@external
@nonpayable
def bid(bidAmount:uint256, tokenID: uint256):
    auctionItem: AuctionItem = self.auctionItems[tokenID]
    #Conditions
    assert block.timestamp >= auctionItem.auctionStart
    assert block.timestamp < auctionItem.auctionEnd
    assert bidAmount > auctionItem.minValue
    assert bidAmount > auctionItem.highestBid
    assert self.wolvercoin.getBalanceOf(msg.sender)>=bidAmount

    #Managing wolvercoin: return to previous highest, receive *new* highest
    self.wolvercoin.transferFrom(msg.sender,self,bidAmount)
    if auctionItem.hasBid:
        self.wolvercoin.transferFrom(self,auctionItem.highestBidder,auctionItem.highestBid)

    #Assign highestBidder and highestBid to new 
    auctionItem.highestBidder = msg.sender
    auctionItem.highestBid = bidAmount
    auctionItem.hasBid = True
    assert auctionItem.hasBid == True

#endAuction: as long as time is passed auction end, end auction and disallow changes to variables
@external
def endItemAuction(tokenID: uint256):
    auctionItem: AuctionItem = self.auctionItems[tokenID]
    #Conditions
    assert block.timestamp >= auctionItem.auctionEnd
    assert auctionItem.ended == False
    auctionItem.ended = True
    self.wolvercoin.transferFrom(self,auctionItem.beneficiary, auctionItem.highestBid)
    #Transfer NFT ownership from contract to highest bidder
    self.auctionNFT.transferFrom(self,auctionItem.highestBidder,tokenID)
    self.auctionItems[tokenID] = empty(AuctionItem)

